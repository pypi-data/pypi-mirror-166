#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crossover and mutation operations applied to a population to generate diversity.
"""
import tensorflow as tf

class PolynomialMutation:
    '''
    Uses polynomial mutation to randomly mutate individuals. Adapted from the
    Pymoo library [3]_.
    
    
    Parameters
    ----------
    lowerbound : 1D tensor
        Lower bounds for X.
    upperbound : 1D tensor
        Upper bounds for X.
    prob_per_var : float, optional
        The probability that a variable is mutated. If None, the probability is
        1 / n_var. The default is None.
    eta : float, optional
        Controls the degree of mutation. Higher values generate children
        that are more similar to their parents. The default is 1.0.

    Returns
    -------
    Tensor with the same shape and type as X.
    
    References
    ----------
    .. [3] https://github.com/anyoptimization/pymoo/blob/master/pymoo/operators/mutation/pm.py

    '''
    def __init__(self, lowerbound, upperbound, prob_per_var = None, eta = 1.0):
        
        if tf.is_tensor(lowerbound) and tf.is_tensor(upperbound):
            assert tf.rank(lowerbound) == 1
            assert tf.rank(upperbound) == 1
            self.x_lower = lowerbound
            self.x_upper = upperbound
        else:
            raise TypeError
        
        if prob_per_var is None:
            self.prob_per_var = 1.0 / lowerbound.shape[0]
        else:
            assert prob_per_var > 0.0 and prob_per_var <= 1.0
            self.prob_per_var = prob_per_var
        
        assert eta > 0
        self.eta = eta
        

    @tf.function(input_signature=(tf.TensorSpec(shape=[None,None], dtype=tf.float64),))  
    def __call__(self, X):
        '''
        Apply mutation. X must be rank 2 with dtype=tf.float64.
        '''
        do_mut = tf.random.uniform(tf.shape(X)) < self.prob_per_var
        
        Y = tf.identity(X)
        
        delta1 = (X - self.x_lower) / (self.x_upper - self.x_lower)
        delta2 = (self.x_upper - X) / (self.x_upper - self.x_lower)
    
        mut_pow = 1.0 / (self.eta + 1.0)
    
        rand = tf.random.uniform(tf.shape(X), dtype=tf.float64)
        mask = rand <= 0.5
        mask_not = ~mask
    
        deltaq = tf.zeros_like(X, dtype=tf.float64)
    
        xy = 1.0 - delta1
        val = 2.0 * rand + (1.0 - 2.0 * rand) * (tf.math.pow(xy, (self.eta + 1.0)))
        d = tf.math.pow(val, mut_pow) - 1.0
        deltaq = deltaq + d * tf.cast(mask, tf.float64)
    
        xy = 1.0 - delta2
        val = 2.0 * (1.0 - rand) + 2.0 * (rand - 0.5) * (tf.math.pow(xy, (self.eta + 1.0)))
        d = 1.0 - (tf.math.pow(val, mut_pow))
        deltaq = deltaq + d * tf.cast(mask_not, tf.float64)
    
        # Mutated values
        _Y = X + deltaq * (self.x_upper - self.x_lower)
    
        # Set the values for output
        Y = Y * tf.cast(~do_mut, tf.float64) + _Y * tf.cast(do_mut, tf.float64)
        
        # Clip to bounds and return
        return tf.clip_by_value(Y, self.x_lower, self.x_upper)



class SimulatedBinaryCx:
    '''
    Uses simulated binary crossover to create child solutions from parents.
    Generates 2 * int(n_individuals / 2) children which is equal to 
    n_individuals only when it is even. Adapted from the Pymoo library [4]_
    
    
    Parameters
    ----------
    lowerbound : 1D tensor
        Lower bounds for X.
    upperbound : 1D tensor
        Upper bounds for X.
    prob_per_var : float, optional
        The probability of performing crossover on an element in an individual
        solution. The default is 0.7.
    eta : float, optional
        Controls the degree of crossover. Higher values generate children
        that are more similar to their parents. The default is 1.0.

    Returns
    -------
    Tensor with the same shape and type as X.
    
    References
    ----------
    .. [4] https://github.com/anyoptimization/pymoo/blob/master/pymoo/operators/crossover/sbx.py

    '''
    def __init__(self, lowerbound, upperbound, prob_per_var=0.7, eta=1.0):    
        if tf.is_tensor(lowerbound) and tf.is_tensor(upperbound):
            assert len(lowerbound.shape) == 1
            assert len(upperbound.shape) == 1
            self.x_lower = lowerbound
            self.x_upper = upperbound
        else:
            raise TypeError
                
        assert prob_per_var > 0.0 and prob_per_var <= 1.0
        assert eta > 0
        self.prob_per_var = prob_per_var
        self.eta = eta
        
    @tf.function(input_signature=(tf.TensorSpec(shape=[None,None], dtype=tf.float64),tf.TensorSpec(shape=[None,None], dtype=tf.float64)))  
    def __call__(self, X1, X2):
        '''
        Apply crossover. X1,X2 must be rank 2 with dtype=tf.float64.
        '''        
        
        def calc_betaq(beta):
            alpha = 2.0 - tf.math.pow(beta, -(self.eta + 1.0))
    
            mask = (rand <= (1.0 / alpha))
            mask_not = ~mask
            
            betaq = tf.math.pow((rand * alpha), (1.0 / (self.eta + 1.0))) * tf.cast(mask, tf.float64)
            betaq = betaq + tf.math.pow((1.0 / (2.0 - rand * alpha)), (1.0 / (self.eta + 1.0))) * tf.cast(mask_not, tf.float64)
    
            return betaq
        
        # Get shape of input tensor
        shape = tf.shape(X1)
        n_candidates = shape[0]
        n_var = shape[1]
        
        # Randomly select elements to crossover
        do_cx = tf.random.uniform((n_candidates, n_var)) < self.prob_per_var
        
        # If values are too close no mating is done
        do_cx = tf.logical_and(do_cx, ~(tf.abs(X1-X2) <= 1.0e-14))
        
        # assign y1 the smaller and y2 the larger value
        y1 = tf.minimum(X1,X2)
        y2 = tf.maximum(X1,X2)
        
        delta = y2 - y1
        # To avoid division by zero
        delta_mask = delta < 1.0e-10
        delta = delta * tf.cast(~delta_mask,tf.float64) + 1.0e-10 * tf.cast(delta_mask,tf.float64)
        
        # Random values for each individual
        rand = tf.random.uniform((n_candidates, n_var), dtype=tf.float64)
        
        beta = 1.0 + (2.0 * (y1 - self.x_lower) / delta)
        betaq = calc_betaq(beta)
        c1 = 0.5 * ((y1 + y2) - betaq * delta)
    
        beta = 1.0 + (2.0 * (self.x_upper - y2) / delta)
        betaq = calc_betaq(beta)
        c2 = 0.5 * ((y1 + y2) + betaq * delta)
        
        # Do a random swap of variables
        var_mask = tf.random.uniform((n_candidates, n_var)) <= 0.5
        
        c1_copy = tf.identity(c1)
        c1 = c1 * tf.cast(~var_mask, tf.float64) + c2 * tf.cast(var_mask, tf.float64)
        c2 = c2 * tf.cast(~var_mask, tf.float64) + c1_copy * tf.cast(var_mask, tf.float64)
          
        # Take the parents as a template
        cc1 = tf.identity(X1)
        cc2 = tf.identity(X2)
    
        # Copy the positions where the crossover was done
        cc1 = cc1 * tf.cast(~do_cx, tf.float64) + c1 * tf.cast(do_cx, tf.float64)
        cc2 = cc2 * tf.cast(~do_cx, tf.float64) + c2 * tf.cast(do_cx, tf.float64)
        
        # Concatenate all children
        all_children =  tf.concat([cc1,cc2], axis=0)
        
        # Clip to bounds and return
        return tf.clip_by_value(all_children, self.x_lower, self.x_upper)
    
    
