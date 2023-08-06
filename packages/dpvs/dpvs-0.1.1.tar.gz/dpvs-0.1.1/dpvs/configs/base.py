from itertools import product
from typing import Tuple
from scipy.stats._distn_infrastructure import rv_generic
from .extra import *

__all__ = ['Config', 'Case', 'Book', 'Args', 'Grid']

class Case(object):
    def __init__(self, follow_name, value_d: dict = None):
        self.follow_name = follow_name
        if not 'default' in value_d: 
            value_d['default'] = {}
        if isinstance(value_d['default'], dict):
            self.rtn_dict = True
        else:
            self.rtn_dict = False
        self.value_d = value_d
    def __call__(self, key, default_d={}):
        if self.rtn_dict:
            return {**default_d, **self.value_d.get(key, {})}
        else:
            return self.value_d.get(key, self.value_d['default'])
    def __str__(self):
        return f'&{self.follow_name}'
    @property
    def key(self):
        return Config(self.value_d['default']).obtain_key()

class Book(dict):
    def __init__(self, values):
        super().__init__(values)
    def __str__(self): 
        return ','.join(map(str, self)) #TODO: unimplemented
    @property
    def key(self): # {'a': [1, 2], 'd': ['a', 'b']}
        return Config(self).obtain_key()   

class Config:
    r"""Defines a set of configurations for the experiment. 
    The configuration includes the following possible items:
    * Hyperparameters: learning rate, batch size etc.
    * Experiment settings: training iterations, logging directory, environment name etc.
    All items are stored in a dictionary. It is a good practice to semantically name each item
    e.g. `network.lr` indicates the learning rate of the neural network. 
    For hyperparameter search, we support both grid search (:class:`Grid`) and random search (:class:`Sample`).
    Call :meth:`make_configs` to generate a list of all configurations, each is assigned
    with a unique ID. 
    
    Example::
    
        >>> config = Config({'log.dir': 'some path', 'network.lr': Grid([1e-3, 5e-3]), 'env.id': Grid(['CartPole-v1', 'Ant-v2'])}, num_sample=1, keep_dict_order=False)
        >>> import pandas as pd
        >>> print(pd.DataFrame(config.make_configs()))
               ID       env.id    log.dir  network.lr
            0   0  CartPole-v1  some path       0.001
            1   1       Ant-v2  some path       0.001
            2   2  CartPole-v1  some path       0.005
            3   3       Ant-v2  some path       0.005
    
    Args:
        items (dict): a dictionary of all configuration items. 
        n_iter (int): number of samples for random configuration items. 
        keep_dict_order (bool): if ``True``, then each generated configuration has the same key ordering with :attr:`items`. 
    """

    def __init__(self, items, n_iter=None):
        if not isinstance(items, dict):
            items = {}
        self.item_d = items
        self.param_d = {}
        self.n_iter = n_iter
    
    def obtain_key(self, tune=[]):
        new_dict = {k: v for k,v in self.item_d.items() if k not in tune}
        param_d = {}
        for key,param in new_dict.items():
            if isinstance(param, Grid):
                param_d[key] = param.key
            if _is_distribution(param):
                param = Distribution(param)
                param_d[key] = param.key
        for key,param in new_dict.items():
            if isinstance(param, Follow) and param.follow_name in param_d:
                param_d[key] = param.key or param_d[param.follow_name]
        for key,param in new_dict.items():
            if isinstance(param, Case):
                for k,v in param.key.items():
                    param_d[f'{key}.{k}'] = v
            elif isinstance(param, (dict, Book)):
                for k,v in Config(param).obtain_key().items():
                    param_d[f'{key}.{k}'] = v

        for k in param_d.copy(): #delete parameter with only one choice
            if param_d[k] is None or len(param_d[k]) <= 1:
                param_d.pop(k)
        self.item_d, self.param_d = new_dict, {**new_dict, **param_d}
        return param_d

    def __getitem__(self, __name):
        return self.item_d.get(__name, None)

    def __contains__(self, __name):
        return __name in self.item_d

    def __iter__(self):
        yield from self.param_d

    def make_configs(self, new_id=True, **kwargs):
        keys_grid, keys_fixed, keys_sample = {}, [], []
        self.item_d = {**self.item_d, **kwargs}
        for key, param in self.item_d.items():
            if isinstance(param, (dict, Book)):
                vlist = Config(param).make_configs(new_id=False)
                keys_grid[key] = vlist
            elif isinstance(param, Case):
                vlist = Config(param.value_d['default']).make_configs(new_id=False)
                keys_grid[key] = [(param, v) for v in vlist]
            elif isinstance(param, Grid):
                keys_grid[key] = param
            elif isinstance(param, Sample) or _is_distribution(param):
                if not isinstance(param, Sample):
                    self.item_d[key] = Distribution(param)
                keys_sample.append(key)
            elif isinstance(param, Follow):
                param.follow(self.item_d[param.follow_name])
                keys_fixed.append(key)
            else:
                keys_fixed.append(key)
                
        grid_product = list(
            dict(zip(keys_grid.keys(), values)) for values in product(*keys_grid.values())
        )
        list_rtn = []
        fixed_d = {key: self.item_d[key] for key in keys_fixed}
        for i in range(len(grid_product)):
            d = {'ID': i} if new_id else {}
            d = {**d, **fixed_d, **grid_product[i%len(grid_product)]}
            for key in keys_sample:
                d[key] = self.item_d[key]()
            for key, value in d.items():
                if isinstance(value, Condition):
                    d[key] = value(d)
                elif isinstance(value, Follow):
                    d[key] = value(d[value.follow_name]) 
                elif isinstance(value, Tuple):
                    fn, default_d = value
                    d[key] = fn(d[fn.follow_name], default_d)
            list_rtn.append(d)
        return list_rtn

    def merge(self, params):
        """merge with already sampled parameters
        """
        config = self.make_configs()[0]; new_config = {}
        param_key = set(x.rpartition('__')[0] for x in params.param_distributions[0])
        for k,v in config.items():
            if k in param_key and isinstance(v, dict):
                for kv, vv in v.items():
                    new_config['%s_%s'%(k,kv)] = vv
            else:
                new_config[k] = v
        res = []
        for param in params:
            res.append({**new_config, **param})
        return res

def _is_distribution(param):
    if hasattr(param, 'dist') and isinstance(param.dist, rv_generic):
        return True
    return False

class Distribution(Sample):

    def __init__(self, param):
        self.dist = param
    
    @property
    def key(self): return self.dist.rvs(2)

    def __call__(self):
        return self.dist.rvs(1).item()
