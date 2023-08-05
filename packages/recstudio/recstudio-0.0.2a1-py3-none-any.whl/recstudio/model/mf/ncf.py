import torch
from recstudio.ann import sampler
from recstudio.data import dataset
from recstudio.model import basemodel, loss_func, scorer, module

class NCF(basemodel.BaseRetriever):

    def add_model_specific_args(parent_parser):
        parent_parser = basemodel.Recommender.add_model_specific_args(parent_parser)
        parent_parser.add_argument_group('NCF')
        parent_parser.add_argument("--activation", type=str, default='relu', help='activation function for MLP')
        parent_parser.add_argument("--mlp_hidden_size", type=int, nargs='+', default=32, help='MLP layer size')
        parent_parser.add_argument("--dropout", type=float, default=0.3, help='dropout rate for MLP')
        parent_parser.add_argument("--score_mode", type=str, choices=['mlp', 'mf', 'fusion'], default='fusion', help='score mode')
        parent_parser.add_argument("--negative_count", type=int, default=1, help='negative sampling numbers')
        return parent_parser


    def _get_dataset_class():
        return dataset.MFDataset

    def _get_item_encoder(self, train_data):
        return torch.nn.Embedding(train_data.num_items, self.embed_dim, padding_idx=0)

    def _get_query_encoder(self, train_data):
        return torch.nn.Embedding(train_data.num_users, self.embed_dim, padding_idx=0)

    def _get_score_func(self):
        assert self.config['score_mode'] in set(['mlp', 'mf', 'fusion']), \
            "Only 3 score modes are supported for NCF: ['mlp', 'mf', 'fusion']"
        if self.config['score_mode']== 'mlp':
            return scorer.MLPScorer(module.MLPModule(
                mlp_layers = [self.embed_dim*2]+self.config['mlp_hidden_size']+[1],
                activation_func = self.config['activation'],
                dropout = self.config['dropout']))
        elif self.config['score_mode'] == 'mf':
            return scorer.GMFScorer(self.embed_dim, activation=self.config['activation'])
        else:
            mlp = module.MLPModule(
                mlp_layers = [self.embed_dim*2]+self.config['mlp_hidden_size'],
                activation_func = self.config['activation'],
                dropout = self.config['dropout'])
            return scorer.FusionMFMLPScorer(
                emb_dim = self.embed_dim,
                hidden_size = self.config['mlp_hidden_size'][-1],
                mlp = mlp,
                activation = self.config['activation'])


    def _get_loss_func(self):
        return loss_func.BinaryCrossEntropyLoss()

    def _get_sampler(self, train_data):
        return sampler.UniformSampler(train_data.num_items)
