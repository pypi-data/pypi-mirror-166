import abc
import os
import inspect
import logging
from typing import Dict, List, Optional, Tuple, Union
from collections import defaultdict

import copy
import time
# import nni
import recstudio.eval as eval
import torch
import torch.optim as optim
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
import torch.multiprocessing as mp
from recstudio.model import init, basemodel, loss_func
from recstudio.utils import callbacks
from recstudio.utils.utils import color_dict, seed_everything, parser_yaml, get_model
from recstudio.data.dataset import (MFDataset, CombinedLoaders)


class Recommender(torch.nn.Module, abc.ABC):
    def __init__(self, config: Dict = None, **kwargs):
        super(Recommender, self).__init__()
        if config is not None:
            self.config = config
        else:
            self.config = parser_yaml(os.path.join(os.path.dirname(__file__), "basemodel.yaml"))

        if self.config['seed'] is not None:
            seed_everything(self.config['seed'], workers=True)

        # self.fields = self.config['use_fields']
        self.embed_dim = self.config['embed_dim']

        self.logger = logging.getLogger('recstudio')

        self.logged_metrics = {}

        if 'retriever' in kwargs:
            assert isinstance(kwargs['retriever'], basemodel.BaseRetriever), \
                "sampler must be recstudio.model.basemodel.BaseRetriever"
            self.retriever = kwargs['retriever']
        else:
            self.retriever = None

        if "loss" in kwargs:
            assert isinstance(kwargs['loss'], loss_func.FullScoreLoss) or \
                isinstance(kwargs['loss'], loss_func.PairwiseLoss) or \
                isinstance(kwargs['loss'], loss_func.PointwiseLoss), \
                "loss should be one of: [recstudio.loss_func.FullScoreLoss, \
                recstudio.loss_func.PairwiseLoss, recstudio.loss_func.PointWiseLoss]"
            self.loss_fn = kwargs['loss']
        else:
            self.loss_fn = self._get_loss_func()

        self.ckpt_path = None

    @staticmethod
    def add_model_specific_args(parent_parser):
        parent_parser.add_argument_group('Recommender')
        parent_parser.add_argument("--learning_rate", type=float, default=0.001, help='learning rate')
        parent_parser.add_argument("--learner", type=str, default="adam", help='optimization algorithm')
        parent_parser.add_argument('--weight_decay', type=float, default=0, help='weight decay coefficient')
        parent_parser.add_argument('--epochs', type=int, default=50, help='training epochs')
        parent_parser.add_argument('--batch_size', type=int, default=256, help='training batch size')
        parent_parser.add_argument('--eval_batch_size', type=int, default=128, help='evaluation batch size')
        parent_parser.add_argument('--embed_dim', type=int, default=64, help='embedding dimension')
        parent_parser.add_argument('--gpu', type=int, action='append', default=None, help='gpu number')
        return parent_parser

    def _add_modules(self, train_data):
        pass

    def _set_data_field(self, data):
        pass

    def _init_model(self, train_data):
        self._set_data_field(train_data) #TODO(@AngusHuang17): to be considered in a better way
        self.fields = train_data.use_field
        self.frating = train_data.frating
        assert self.frating in self.fields, 'rating field is required.'
        train_data.drop_feat(self.fields)
        # if self.fields is not None:
        #     assert self.frating in self.fields, 'rating field is required.'
        #     train_data.drop_feat(self.fields)
        # else:
        #     self.fields = set(f for f in train_data.field2type) # 需要去除time吗？

        self.item_feat = train_data.item_feat
        self.item_fields = set(train_data.item_feat.fields).intersection(self.fields)
        self.neg_count = self.config['negative_count']



    def fit(
        self,
        train_data: MFDataset,
        val_data: Optional[MFDataset] = None,
        run_mode='light',
        config: Dict = None,
        **kwargs
    ) -> None:
        r"""
        Fit the model with train data.
        """
        # self.set_device(self.config['gpu'])
        torch.set_num_threads(self.config['num_threads'])

        if config is not None:
            self.config.update(config)

        if kwargs is not None:
            self.config.update(kwargs)

        self._init_model(train_data)

        self._init_parameter()

        # config callback
        self.run_mode = run_mode
        self.val_check = val_data is not None and self.config['val_metrics'] is not None
        if val_data is not None:
            val_data.use_field = train_data.use_field
        if self.val_check:
            self.val_metric = next(iter(self.config['val_metrics'])) \
                if isinstance(self.config['val_metrics'], list) \
                else self.config['val_metrics']
            cutoffs = self.config['cutoff'] \
                if isinstance(self.config['cutoff'], list) \
                else [self.config['cutoff']]
            if len(eval.get_rank_metrics(self.val_metric)) > 0:
                self.val_metric += '@' + str(cutoffs[0])
        # logger = TensorBoardLogger(save_dir=save_dir, name="tensorboard")
        self.callback = self._get_callback()
        self.logger.info('save_dir:' + self.callback.save_dir)
        # refresh_rate = 0 if run_mode in ['light', 'tune'] else 1

        self.logger.info(self)

        self._accelerate()

        if self.config['accelerator'] == 'ddp':
            mp.spawn(self.parallel_training, args=(self.world_size, train_data, val_data),
                     nprocs=self.world_size, join=True)
        else:
            self.trainloaders = self._get_train_loaders(train_data)

            if val_data:
                val_loader = val_data.eval_loader(
                    batch_size=self.config['eval_batch_size'],
                    num_workers=self.config['num_workers'])
            else:
                val_loader = None
            self.optimizers = self._get_optimizers()
            self.fit_loop(val_loader)

    def parallel_training(self, rank, world_size, train_data, val_data):
        dist.init_process_group("nccl", rank=rank, world_size=world_size)

        self.trainloaders = self._get_train_loaders(train_data, ddp=True)

        if val_data:
            val_loader = val_data.eval_loader(
                batch_size=self.config['eval_batch_size'],
                num_workers=self.config['num_workers'], ddp=True)
        else:
            val_loader = None
        self.device = self.device_list[rank]
        self = self.to(self.device)
        self = DDP(self, device_ids=[self.device], output_device=self.device).module
        self.optimizers = self._get_optimizers()
        # self.
        self.fit_loop(val_loader)
        dist.destroy_process_group()

        # mp.spawn(parallel_training, args=(self.world_size,), \
        #     nprocs=self.world_size, join=True)

    def evaluate(self, test_data, verbose=True, **kwargs) -> Dict:
        r""" Predict for test data.

        Args:
            test_data(recstudio.data.Dataset): The dataset of test data, which is generated by RecStudio.

            verbose(bool, optimal): whether to show the detailed information.

        Returns:
            dict: dict of metrics. The key is the name of metrics.
        """
        if 'config' in kwargs:
            self.config.update(kwargs['config'])

        test_data.drop_feat(self.fields)
        test_loader = test_data.eval_loader(batch_size=self.config['eval_batch_size'],
                                            num_workers=self.config['num_workers'])
        output = {}
        self.load_checkpoint(os.path.join(self.config['save_path'], self.ckpt_path)) # bug to fix 应该支持使用保存的模型进行评测
        self.eval()
        output_list = self.test_epoch(test_loader)
        output.update(self.test_epoch_end(output_list))
        if self.run_mode == 'tune':
            output['default'] = output[self.val_metric]
            # nni.report_final_result(output)
        if verbose:
            self.logger.info(color_dict(output, self.run_mode == 'tune'))
        # return output

    def predict(self, batch, k, *args, **kwargs):
        pass

    @abc.abstractmethod
    def forward(self, batch):
        pass

    def _get_callback(self):
        save_dir = self.config['save_path']
        if self.val_check:
            return callbacks.EarlyStopping(self, self.val_metric, save_dir=save_dir, \
                patience=self.config['early_stop_patience'], mode=self.config['early_stop_mode'])
        else:
            return callbacks.SaveLastCallback(self, save_dir=save_dir)

    def current_epoch_trainloaders(self, nepoch) -> Tuple:
        r"""
        Returns:
            list or dict or Dataloader : the train loaders used in the current epoch
            bool : whether to combine the train loaders or use them alternately in one epoch.
        """
        # use nepoch to config current trainloaders
        combine = False
        return self.trainloaders, combine

    def current_epoch_optimizers(self, nepoch) -> List:
        # use nepoch to config current optimizers
        return self.optimizers

    @abc.abstractmethod
    def build_index(self):
        pass

    @abc.abstractmethod
    def training_step(self, batch):
        pass

    @abc.abstractmethod
    def validation_step(self, batch):
        pass

    @abc.abstractmethod
    def test_step(self, batch):
        pass


    def training_epoch_end(self, output_list):
        output_list = [output_list] if not isinstance(output_list, list) else output_list
        for outputs in output_list:
            if isinstance(outputs, List):
                loss_metric = {'train_'+ k: torch.hstack([e[k] for e in outputs]).mean() for k in outputs[0]}
            elif isinstance(outputs, torch.Tensor):
                loss_metric = {'train_loss': outputs.item()}
            elif isinstance(outputs, Dict):
                loss_metric = {'train_'+k : v for k, v in outputs}
            self.log_dict(loss_metric)

        if self.val_check and self.run_mode == 'tune':
            metric = self.logged_metrics[self.val_metric]
            # nni.report_intermediate_result(metric)
        # TODO: only print when rank=0
        if self.run_mode in ['light', 'tune'] or self.val_check:
            self.logger.info(color_dict(self.logged_metrics, self.run_mode == 'tune'))
        else:
            self.logger.info('\n'+color_dict(self.logged_metrics, self.run_mode == 'tune'))

    def validation_epoch_end(self, outputs):
        val_metric = self.config['val_metrics'] if isinstance(self.config['val_metrics'], list) \
            else [self.config['val_metrics']]
        cutoffs = self.config['cutoff'] if isinstance(self.config['cutoff'], list) \
            else [self.config.setdefault('cutoff', None)]
        val_metric = [f'{m}@{cutoff}' if len(eval.get_rank_metrics(m)) > 0 \
            else m for cutoff in cutoffs[:1] for m in val_metric]
        if isinstance(outputs[0][0], List):
            out = self._test_epoch_end(outputs)
            out = dict(zip(val_metric, out))
        elif isinstance(outputs[0][0], Dict):
            out = self._test_epoch_end(outputs)
        self.log_dict(out)
        return out

    def test_epoch_end(self, outputs):
        test_metric = self.config['test_metrics'] if isinstance(self.config['test_metrics'], list) \
            else [self.config['test_metrics']]
        cutoffs = self.config['cutoff'] if isinstance(self.config['cutoff'], list) \
            else [self.config.setdefault('cutoff', None)]
        test_metric = [f'{m}@{cutoff}' if len(eval.get_rank_metrics(m)) > 0 \
            else m for cutoff in cutoffs for m in test_metric]
        if isinstance(outputs[0][0], List):
            out = self._test_epoch_end(outputs)
            out = dict(zip(test_metric, out))
        elif isinstance(outputs[0][0], Dict):
            out = self._test_epoch_end(outputs)
        self.log_dict(out)
        return out

    def _test_epoch_end(self, outputs):
        if isinstance(outputs[0][0], List):
            metric, bs = zip(*outputs)
            metric = torch.tensor(metric)
            bs = torch.tensor(bs)
            out = (metric * bs.view(-1, 1)).sum(0) / bs.sum()
        elif isinstance(outputs[0][0], Dict):
            metric_list, bs = zip(*outputs)
            bs = torch.tensor(bs)
            out = defaultdict(list)
            for o in metric_list:
                for k, v in o.items():
                    out[k].append(v)
            for k, v in out.items():
                metric = torch.tensor(v)
                out[k] = (metric * bs).sum() / bs.sum()
        return out

    def log_dict(self, metrics: Dict):
        self.logged_metrics.update(metrics)

    def _init_parameter(self):
        init_methods = {
            'xavier_normal': init.xavier_normal_initialization,
            'xavier_uniform': init.xavier_uniform_initialization,
            'normal': init.normal_initialization,
        }
        for name, module in self.named_children():
            if isinstance(module, Recommender):
                module._init_parameter()
            else:
                if self.config['init_method'] == 'normal':
                    init_method = init.normal_initialization(self.config['init_range'])
                else:
                    init_method = init_methods[self.config['init_method']]
                module.apply(init_method)

    @staticmethod
    def _get_dataset_class():
        pass

    def _get_loss_func(self):
        return None

    def _get_item_feat(self, data):
        if isinstance(data, dict):  # batch_data
            if len(self.item_fields) == 1:
                return data[self.fiid]
            else:
                return dict((field, value) for field, value in data.items() if field in self.item_fields)
        else:  # neg_item_idx
            if len(self.item_fields) == 1:
                return data
            else:
                return self.item_feat[data]

    def _get_train_loaders(self, train_data, ddp=False) -> List:
        # TODO: modify loaders in model
        return [train_data.train_loader(
            batch_size = self.config['batch_size'],
            shuffle = True,
            num_workers = self.config['num_workers'],
            drop_last = False, ddp=ddp)]


    def _get_optimizers(self) -> List[Dict]:
        if 'learner' not in self.config:
            self.config['learner'] = 'adam'
            self.logger.warning("`learner` is not detected in the configuration, Adam optimizer"
                                "is used.")

        if self.config['learner'] is None:
            self.logger.warning('There is no optimizers in the model due to `learner` is'
                                'set as None in configurations.')
            return None

        if isinstance(self.config['learner'], list):
            self.logger.warning("If you want to use multi learner, please \
                override `_get_optimizers` function. We will use the first \
                learner for all the parameters.")
            opt_name = self.config['learner'][0]
            lr = self.config['learning_rate'][0]
            weight_decay = None if self.config['weight_decay'] is None \
                else self.config['weight_decay'][0]
            scheduler_name = None if self.config['scheduler'] is None \
                else self.config['scheduler'][0]
        else:
            opt_name = self.config['learner']
            if 'learning_rate' not in self.config:
                self.logger.warning("`learning_rate` is not detected in the configurations,"
                                    "the default learning is set as 0.001.")
                self.config['learning_rate'] = 0.001
            lr = self.config['learning_rate']

            if 'weight_decay' not in self.config:
                self.logger.warning("`weight_decay` is not detected in the configurations,"
                                    "the default weight_decay is set as 0.")
                self.config['weight_decay'] = 0
            weight_decay = self.config['weight_decay']
            scheduler_name = self.config['scheduler']
        params = self.parameters()
        optimizer = self._get_optimizer(opt_name, params, lr, weight_decay)
        scheduler = self._get_scheduler(scheduler_name, optimizer)
        m = self.val_metric if self.val_check else 'train_loss'
        if scheduler:
            return [{
                'optimizer': optimizer,
                'lr_scheduler': {
                    'scheduler': scheduler,
                    'monitor': m,
                    'interval': 'epoch',
                    'frequency': 1,
                    'strict': False
                }
            }]
        else:
            return [{'optimizer': optimizer}]

    def _get_optimizer(self, name, params, lr, weight_decay):
        r"""Return optimizer for specific parameters.

        The optimizer can be configured in the config file with the key ``learner``.
        Supported optimizer: ``Adam``, ``SGD``, ``AdaGrad``, ``RMSprop``, ``SparseAdam``.

        .. note::
            If no learner is assigned in the configuration file, then ``Adam`` will be user.

        Args:
            params: the parameters to be optimized.

        Returns:
            torch.optim.optimizer: optimizer according to the config.
        """
        # '''@nni.variable(nni.choice(0.1, 0.05, 0.01, 0.005, 0.001), name=learning_rate)'''
        learning_rate = lr
        # '''@nni.variable(nni.choice(0.1, 0.01, 0.001, 0), name=decay)'''
        decay = weight_decay
        if name.lower() == 'adam':
            optimizer = optim.Adam(params, lr=learning_rate, weight_decay=decay)
        elif name.lower() == 'sgd':
            optimizer = optim.SGD(params, lr=learning_rate, weight_decay=decay)
        elif name.lower() == 'adagrad':
            optimizer = optim.Adagrad(params, lr=learning_rate, weight_decay=decay)
        elif name.lower() == 'rmsprop':
            optimizer = optim.RMSprop(params, lr=learning_rate, weight_decay=decay)
        elif name.lower() == 'sparse_adam':
            optimizer = optim.SparseAdam(params, lr=learning_rate)
            # if self.weight_decay > 0:
            #    self.logger.warning('Sparse Adam cannot argument received argument [{weight_decay}]')
        else:
            optimizer = optim.Adam(params, lr=learning_rate)
        return optimizer

    def _get_scheduler(self, name, optimizer):
        r"""Return learning rate scheduler for the optimizer.

        Args:
            optimizer(torch.optim.Optimizer): the optimizer which need a scheduler.

        Returns:
            torch.optim.lr_scheduler: the learning rate scheduler.
        """
        if name is not None:
            if name.lower() == 'exponential':
                scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.98)
            elif name.lower() == 'onplateau':
                scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer)
            else:
                scheduler = None
        else:
            scheduler = None
        return scheduler

    def fit_loop(self, val_dataloader=None):
        try:
            nepoch = 0
            for e in range(self.config['epochs']):
                self.logged_metrics = {}
                self.logged_metrics['epoch'] = nepoch

                # training procedure
                tik_train = time.time()
                self.train()
                training_output_list = self.training_epoch(nepoch)
                tok_train = time.time()

                # validation procedure
                tik_valid = time.time()
                if self.val_check:
                    self.eval()
                    validation_output_list = self.validation_epoch(nepoch, val_dataloader)
                    self.validation_epoch_end(validation_output_list)
                tok_valid = time.time()

                self.training_epoch_end(training_output_list)
                self.logger.info("Train time: {:.5f}s. Valid time: {:.5f}s".format(
                    (tok_train-tik_train), (tok_valid-tik_valid)
                ))

                # learning rate scheduler step
                optimizers = self.current_epoch_optimizers(e)
                if optimizers is not None:
                    for opt in optimizers:
                        if 'scheduler' in opt:
                            opt['scheduler'].step()

                # model is saved in callback when the callback return True.
                stop_training = self.callback(self, nepoch, self.logged_metrics)
                if stop_training:
                    break

                nepoch += 1

            self.callback.save_checkpoint(nepoch)
            self.ckpt_path = self.callback.get_checkpoint_path()
        except KeyboardInterrupt:
            # if catch keyboardinterrupt in training, save the best model.
            if (self.config['accelerator']=='ddp'):
                if (dist.get_rank()==0):
                    self.callback.save_checkpoint(nepoch)
                    self.ckpt_path = self.callback.get_checkpoint_path()
            else:
                self.callback.save_checkpoint(nepoch)
                self.ckpt_path = self.callback.get_checkpoint_path()

    def training_epoch(self, nepoch):
        if hasattr(self, "_update_item_vector"):
            self._update_item_vector()

        if hasattr(self, "sampler"):
            if hasattr(self.sampler, "update"):
                self.sampler.update(item_embs=self.item_vector)  # TODO: add frequency
        output_list = []
        optimizers = self.current_epoch_optimizers(nepoch)

        trn_dataloaders, combine = self.current_epoch_trainloaders(nepoch)
        if isinstance(trn_dataloaders, List) or isinstance(trn_dataloaders, Tuple):
            if combine:
                trn_dataloaders = [CombinedLoaders(list(trn_dataloaders))]
        else:
            trn_dataloaders = [trn_dataloaders]

        if not (isinstance(optimizers, List) or isinstance(optimizers, Tuple)):
            optimizers = [optimizers]

        for loader_idx, loader in enumerate(trn_dataloaders):
            outputs = []
            for optimizer_idx, opt in enumerate(optimizers):
                for batch_idx, batch in enumerate(loader):
                    # data to device
                    batch = self._to_device(batch, self._parameter_device)

                    if opt is not None:
                        opt['optimizer'].zero_grad()
                    # model loss
                    training_step_args = {'batch': batch}
                    if 'nepoch' in inspect.getargspec(self.training_step).args:
                        training_step_args['nepoch'] = nepoch
                    if 'loader_idx' in inspect.getargspec(self.training_step).args:
                        training_step_args['loader_idx'] = loader_idx 
                    if 'batch_idx' in inspect.getargspec(self.training_step).args:
                        training_step_args['batch_idx'] = batch_idx

                    loss = self.training_step(**training_step_args)

                    if isinstance(loss, dict):
                        if loss['loss'].requires_grad:
                            loss['loss'].backward()
                        loss_ = {}
                        for k, v in loss.items():
                            if k == 'loss':
                                v = v.detach()
                            loss_[f'{k}_{loader_idx}'] = v
                        outputs.append(loss_)
                    elif isinstance(loss, torch.Tensor):
                        if loss.requires_grad:
                            loss.backward()
                        outputs.append({f"loss_{loader_idx}": loss.detach()})

                    if opt is not None:
                        opt['optimizer'].step()

                    del loss

                if len(outputs) > 0:
                    output_list.append(outputs)
        return output_list

    def validation_epoch(self, nepoch, dataloader):
        if hasattr(self, '_update_item_vector'):  # TODO: config frequency
            self._update_item_vector()
        output_list = []

        for batch in dataloader:
            # data to device
            batch = self._to_device(batch, self._parameter_device)

            # model validation results
            output = self.validation_step(batch)

            output_list.append(output)

        return output_list

    def test_epoch(self, dataloader):
        if hasattr(self, '_update_item_vector'):
            self._update_item_vector()

        output_list = []

        for batch in dataloader:
            # data to device
            batch = self._to_device(batch, self._parameter_device)

            # model validation results
            output = self.test_step(batch)

            output_list.append(output)

        return output_list

    @staticmethod
    def _set_device(gpus):
        if gpus is not None:
            gpus = [str(i) for i in gpus]
            os.environ['CUDA_VISIBLE_DEVICES'] = " ".join(gpus)

    @staticmethod
    def _to_device(batch, device):
        if isinstance(batch, torch.Tensor) or isinstance(batch, torch.nn.Module):
            return batch.to(device)
        elif isinstance(batch, Dict):
            for k in batch:
                batch[k] = Recommender._to_device(batch[k], device)
            return batch
        elif isinstance(batch, List) or isinstance(batch, Tuple):
            output = []
            for b in batch:
                output.append(Recommender._to_device(b, device))
            return output if isinstance(batch, List) else tuple(output)
        else:
            raise TypeError(f"`batch` is expected to be torch.Tensor, Dict, \
                List or Tuple, but {type(batch)} given.")

    def _accelerate(self):
        gpu_list = self.config['gpu']
        if gpu_list is not None:
            if len(gpu_list) == 1:
                # self._set_device(gpu_list)
                self.device = torch.device("cuda", gpu_list[0])
                self = self._to_device(self, self.device)
            elif self.config['accelerator'] == 'dp':
                # self._set_device(gpu_list)
                self.device = torch.device("cuda")
                self = self.to(self.device)
                self = torch.nn.DataParallel(self, device_ids=gpu_list, output_device=gpu_list[0])
            elif self.config['accelerator'] == 'ddp':
                os.environ["MASTER_ADDR"] = "localhost"
                os.environ["MASTER_PORT"] = "29500"
                self.device_list = [torch.device("cuda", i) for i in gpu_list]
                self.world_size = len(self.device_list)
                # dist.init_process_group("nccl", rank=rank, world_size=world_size)
                # dist.init_process_group(backend="nccl")
                # device = torch.device("cuda", local_rank)
                # self = DDP(self, device_ids=[local_rank], output_device=local_rank)
                raise NotImplementedError("'ddp' not implemented.")
            else:
                raise ValueError("expecting accelerator to be 'dp' or 'ddp'"
                                 f"while get {self.config['accelerator']} instead.")
        else:
            self.device = torch.device("cpu")
            self = self._to_device(self, self.device)

    @property
    def _parameter_device(self):
        if len(list(self.parameters())) == 0:
            return torch.device('cpu')
        else:
            return next(self.parameters()).device

    def _get_ckpt_param(self):
        '''
        Returns:
        OrderedDict : the parameters to be saved as check point.
        '''
        return self.state_dict()

    def save_checkpoint(self, ckpt: Dict) -> str:
        save_path = os.path.join(self.config['save_path'])
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        best_ckpt_path = os.path.join(save_path, self._best_ckpt_path)
        torch.save(ckpt, best_ckpt_path)
        self.logger.info("Best model checkpoint saved in {}.".format(
            best_ckpt_path
        ))

    def load_checkpoint(self, path: str) -> None:
        ckpt = torch.load(path)
        self.config = ckpt['config']
        self.load_state_dict(ckpt['parameters'])
