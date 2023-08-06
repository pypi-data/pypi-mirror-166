#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Population and statistics objects and methods to randomly initialize populations.
"""
import numpy as np
import tensorflow as tf
from collections.abc import MutableMapping

def uniform_reference_points(n_objectives, partitions=4):
    ''' 
    Generates uniformly spaced reference points on a unit simplex. Note this
    function is not intended to be called directly but is used by 
    :class:`gatf.algorithms.NSGA3`. Adapted from the Pymoo library [2]_.
    
    Parameters
    ----------
    n_objectives : int
        The number of objectives to be optimized.
    partitions: int
        The number of partitions used to create the reference points.
        
    Returns
    -------
    Rank 2 tensor of shape (n_points, n_objectives)
    
    References
    ----------
    .. [2] https://github.com/DEAP/deap/blob/master/deap/tools/emo.py
    '''
    
    def gen_refs_recursive(ref, n_objectives, left, total, depth):
        points = []
        if depth == n_objectives - 1:
            ref[depth] = left / total
            points.append(ref)
        else:
            for i in range(left + 1):
                ref[depth] = i / total
                points.extend(gen_refs_recursive(ref.copy(), n_objectives, left - i, total, depth + 1))
        return points

    return tf.convert_to_tensor(np.array(gen_refs_recursive(np.zeros(n_objectives),
                                                            n_objectives,
                                                            partitions,
                                                            partitions, 
                                                            0)), dtype=tf.float64)


def initialize_uniform_population(population_size, lowerbound, upperbound):
    '''
    Generates a uniformly distributed population within the bounds provided.
    Note this function is not intended to be called directly.
    
    Parameters
    ----------
    population_size : int
        The number of random individuals to generate.
    lowerbound : tensor
        Rank 1 tensor of shape (n_dim,) where n_dim is the dimensions of X.
    upperbound : tensor
        Rank 1 tensor of shape (n_dim,) where n_dim is the dimensions of X.
        
    Returns
    -------
    Rank 2 tensor of shape (population_size, n_dims)
    
    '''
    return tf.random.uniform(shape=(population_size,lowerbound.shape[0]),
                             minval=lowerbound,
                             maxval=upperbound,
                             dtype=tf.float64)

def initialize_normal_population(population_size, lowerbound, upperbound, mean=None, stddev=None):
    '''
    Generates a normally distributed population within the bounds provided.
    Note this function is not intended to be called directly.

    
    Parameters
    ----------
    population_size : int
        The number of random individuals to generate.
    lowerbound : tensor
        Rank 1 tensor of shape (n_dim,) where n_dim is the dimensions of X.
    upperbound : tensor
        Rank 1 tensor of shape (n_dim,) where n_dim is the dimensions of X.
    mean : tensor, optional
        Rank 1 tensor of shape (n_dim,) where n_dim is the dimensions of X.
        If None, mean is set to (upperbound - lowerbound) / 2 + lowerbound.
        The default is None.
    stddev : tensor, optional
        Rank 1 tensor of shape (n_dim,) where n_dim is the dimensions of X.
        If None, it is set to (upperbound - lowerbound) / 3 such that 99.7%
        of samples will fall between between the bounds provided the mean is centred
        in the space. Any sampled outside of the bounds will be clipped.
        The default is None.
        
    Returns
    -------
    Rank 2 tensor of shape (population_size, n_dims)
    '''
    if mean is None:
        mean = (upperbound - lowerbound) / 2 + lowerbound
    
    if stddev is None:
        stddev = (upperbound - lowerbound) / 3
    X = tf.random.normal(shape=(population_size,lowerbound.shape[0]),
                         mean=mean,
                         stddev=stddev, 
                         dtype=tf.float64)
    return tf.clip_by_value(X, clip_value_min = lowerbound, clip_value_max = upperbound)
    

class Statistics(MutableMapping):
    '''
    For storing population statistics per generation. Dict-like object where
    Statistics[key] = value appends value to a list or creates a new key and
    places value in a list.
    
    '''
    def __init__(self, *args):
        for arg in list(args):
            self.__dict__[arg] = []
    
    def __setitem__(self, key, value):
        try:
            self.__dict__[key].append(value)
        except KeyError:
            self.__dict__[key] = [value]

    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __delitem__(self, key):
        del self.__dict__[key]
    
    def __iter__(self):
        return iter(self.__dict__)
    
    def __len__(self):
        return len(self.__dict__)
    
    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        return '{}, D({})'.format(super(Statistics, self).__repr__(), self.__dict__)
    
    def return_last_n(self, key, n):
        ''' 
        Fetches the last `n` values from entry `key`.
        
        Paramters
        ---------
        key : str
            The key of the values to return.
        n : int
            Number of values to return
            
        Returns
        -------
        list
            A list contain `n` values from `key`. If `key` is not valid, returns `None`.
        '''
        try:
            return self.__dict__[key][-n:]
        except KeyError:
            return None
        
    
class Population(MutableMapping):
    '''
    Dict-like object containing keys 'X', 'fitness', and 'statistics' and, 
    optionally, 'X_best', and 'fitness_best'. Setting Population['X'] = value 
    also sets `Population['fitness']` = None. The 'statistics' key is a :class:`population.Statistics`
    object that also has a dict-like structure. No other keys can be added and
    'statistics' can be accessed but the object cannot be replaced by a new value.
    
    Notes
    -----
    Setting Population.X = value does not set 'fitness' to None. Therefore,
    only set X using Population['X'] = value
    
    '''
    def __init__(self, initial_population):
        self.__dict__.update(X=initial_population, fitness=None, statistics = Statistics())
    
    def __setitem__(self, key, value):
        if key in ['fitness','fitness_best','X_best']:
            self.__dict__[key] = value
        elif key == 'X':
            self.__dict__[key] = value
            self.__setitem__('fitness', None)
        else:
            pass
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __delitem__(self, key):
        del self.__dict__[key]
    
    def __iter__(self):
        return iter(self.__dict__)
    
    def __len__(self):
        return len(self.__dict__)
    
    def __str__(self):
        return str(self.__dict__)
    
    def __repr__(self):
        return '{}, D({})'.format(super(Population, self).__repr__(), self.__dict__)
    
    
    