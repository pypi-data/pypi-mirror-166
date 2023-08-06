#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implementations of NSGA3, muPlusLambda, and Particle Swarm optimizers.
"""
from numbers import Number
import numpy as np
import tensorflow as tf
from . import operators
from . import population


class NSGA3:
    '''
    The NSGA3 algorithm developmed by Deb and Jain 2014 [1]_. Implemented using
    Tensorflow for use with objective functions created with Tensorflow
    (ie. Gaussian Processes). Uses tournament selection to choose individuals to
    apply simulated binary crossover and polynomial mutation.
    
    This algorithm is a minimizer. Objectives to be maximized should be returned
    from the objective function as the negative (ie. :math:`-f(X)`).
    
    To promote diversity and avoid the non-dominated front being filled by
    duplicate solutions, duplicates are removed at each generation and only unique
    solutions are retained for the next generation.
    
    A couple metrics are calculated by this algorithm, including mutual domination
    rate (MDR) and the % of filled reference
    directions. These can be used to assess the success of the optimization.
    However, no early stopping for convergence is implemented.
    

    Parameters
    ----------
    obj_func : function Y = f(X)
        Objective function that takes only a tensor X of shape (None,n_variables)
        and returns a tensor of fitness values of shape (None,n_objectives) and
        with dtype=tf.float64.
    n_objectives : int
        The number of objectives to optimize. Must be >1.
    n_variables : int
        The number of variables in X.
    population_size : int, optional
        The size of the population to generate. May not be exact. The default is 92.
    tournament_size : int, optional
        Tournament selection is used to choose individuals to perform crossover with.
        Must be between [2, population_size]. The default is 2.
    upperbound : float, list/tuple of floats, optional
        Upper bounds for X. The default is 1.0.
    lowerbound : float, list/tuple of floats, optional
        Lower bounds for X. The default is -1.0.
    generations : int, optional
        Number of generations to evolve. The default is 1000.
    mutation_prob : float, optional
        The probability of mutating an element in an individual solution.
        Must be between [0,1]. The default is 0.1.
    crossover_prob : float, optional
        The probability of performing crossover on an element in an individual solution.
        Must be between [0,1]. The default is 0.7.
    mutation_eta : float, optional
        Controls the degree of mutation. Higher values generate children
        that are more similar to their parents. The default is 1.0.
    crossover_eta : float, optional
        Controls the degree of crossover. Higher values generate children
        that are more similar to their parents. The default is 1.0.
    record_gens : int, optional
        How often to record statistics and calculate convergence metrics. The default is
        10 generations.
    verbose : bool
        Whether to print progress to screen. The default is True.
    seed : int, optional
        Random seed. The default is None.

    Returns
    -------
    :class:`gatf.population.Population`
        Optimization results as dict-like key/value pairs including 'X', 'fitness',
        and 'statistics'. The statistics key contains a :class:`population.Statistics`
        object with the keys 'gen', 'mdr', and 'refs'.
    
    Notes
    -----
    The input signatures are defined for Tensorflow functions to avoid
    graph retracing and, therefore, this algorithm expects a tf.float64 datatype.
    Objective functions should be designed to output the proper datatype or an 
    error with be thrown. Custom objectives should also make use of
    the @tf.function decorator to allow compilation into the Tensorflow graph.
    
    >>> @tf.function(input_signature=(tf.TensorSpec(shape=[None,n_objectives], dtype=tf.float64),))
    >>> def my_custom_objective(X):
    >>>    # calculate fitness here
    >>>    return fitness
    
    Providing an input signature is not absolutely necessary but recommended if
    a warning is raised that the graph is being retraced. 
    
    References
    ----------
    .. [1] Deb, Kalyanmoy, and Himanshu Jain. “An Evolutionary Many-Objective
       Optimization Algorithm Using Reference-Point-Based Nondominated Sorting 
       Approach, Part I: Solving Problems With Box Constraints.” IEEE Transactions
       on Evolutionary Computation 18, no. 4 (August 2014): 577–601. 
       https://doi.org/10.1109/TEVC.2013.2281535.

    Examples
    --------
    The NSGA3 algorithm is first instantiated with the desired objective and 
    hyperparameters, then it is called to begin the optimization.
    
    >>> # Initialize NSGA3
    >>> optimizer = NSGA3(my_custom_objective, n_objectives, n_variables, ...)
    >>> # Run the optimizer
    >>> results = optimizer()
    
    The returned results object contains key-accessible values (like a dict).
    
    >>> # Get the final population
    >>> results['X']
    <tf.Tensor: shape=(population_size,n_variables), dtype=float64, numpy=...>
    >>> # Get the associated fitnesses
    >>> results['fitness']
    <tf.Tensor: shape=(population_size,n_objectives), dtype=float64, numpy=...>
    
    Additionally, statistics are recorded throughout the optimization. The
    statistics object contains lists of values that are either numbers or tensors.
    
    >>> # Get the generations that were recorded
    >>> results['statistics']['gen']
    [0,10,20,...]
    >>> # Get the statistic recorded associated with each generation
    >>> results['statistics']['mdr']
    [<tf.Tensor: shape=(), dtype=float64, numpy=...>, <tf.Tensor: shape=(), dtype=float64, numpy=...>, ...]
    
    These can be made into a single numpy array for plotting
    
    >>> np.array(results['statistics']['mdr'])
    array([...])
    
    '''
    
    def __init__(self,
                 obj_func,
                 n_objectives,
                 n_variables,
                 population_size = 92,
                 tournament_size = 2,
                 upperbound=1.0,
                 lowerbound=-1.0,
                 generations=1000,
                 mutation_prob=0.1,
                 crossover_prob=0.7,
                 mutation_eta=1.0,
                 crossover_eta=1.0,
                 record_gens=10,
                 verbose=True,
                 seed=None):
        
        if seed is not None:
            tf.random.set_seed(seed)
        
        self.verbose = verbose
        
        assert n_objectives > 1
        assert tournament_size < population_size

        # Make 1D tensors of bounds
        if isinstance(upperbound,Number):
            upperbound = tf.constant(upperbound, shape=n_variables, dtype=tf.float64)
        elif isinstance(upperbound,(list,tuple)):
            assert len(upperbound) == n_variables
            upperbound = tf.constant(upperbound, dtype = tf.float64)
        else:
            raise TypeError
            
        if isinstance(lowerbound,Number):
            lowerbound = tf.constant(lowerbound, shape=n_variables, dtype=tf.float64)
        elif isinstance(lowerbound,(list,tuple)):
            assert len(lowerbound) == n_variables
            lowerbound = tf.constant(lowerbound, dtype = tf.float64)
        else:
            raise TypeError
        # Check that all upperbound >= lowerbound
        # Permits upper==lower to allow some values to be fixed
        assert tf.reduce_all(upperbound>=lowerbound)

        def set_reference_partitions(n_objectives, population_size, partitions=1):
            # Calculate number of reference points for given partitions
            n_refs = np.math.factorial(n_objectives + partitions - 1) / (np.math.factorial(partitions) * np.math.factorial(n_objectives - 1))
            # Calculate pop size as first multiple of 4 larger than n_refs
            pop_size = int(n_refs + (4 - n_refs % 4))
            # Find closest value >= population_size
            if pop_size < population_size:
                return set_reference_partitions(n_objectives,population_size,partitions+1)
            else:
                return pop_size, n_refs, partitions        

        # Set number of reference partitions
        population_size,n_references,partitions = set_reference_partitions(n_objectives, population_size, n_objectives)
        # Generate reference directions
        ref_dirs = population.uniform_reference_points(n_objectives, partitions)
        
        if self.verbose: print('Population size: {}, reference directions: {}, partitions: {}'.format(population_size,int(n_references),partitions))
        
        # Normalize reference directions so that each is a unit vector
        self.ref_dirs = ref_dirs / tf.norm(ref_dirs, axis=1, keepdims=True)
        self.population_size = tf.constant(population_size, dtype=tf.int32)
        self.tournament_size = tf.constant(tournament_size, dtype=tf.int32)
        self.n_objectives = tf.constant(n_objectives, dtype=tf.int32)
        self.n_variables = tf.constant(n_variables, dtype=tf.int32)
        self.hv_ref = tf.ones((1,n_objectives), dtype = tf.float64)
        self.record_gens = record_gens
        self.obj_func = obj_func
        
        # Randomly initialize populations
        initial_population = population.initialize_uniform_population(population_size, lowerbound, upperbound)
        
        # Creat population object to hold individuals and their fitness
        self.population = population.Population(initial_population)
        
        # Initialize crossover and mutation objects
        self.crossover = operators.SimulatedBinaryCx(lowerbound=lowerbound,
                                                     upperbound=upperbound,
                                                     prob_per_var=crossover_prob,
                                                     eta=crossover_eta)
        self.mutation = operators.PolynomialMutation(lowerbound = lowerbound,
                                                     upperbound = upperbound,
                                                     prob_per_var=mutation_prob,
                                                     eta=mutation_eta)
        
        self.generations = generations

    @tf.function(input_signature=(tf.TensorSpec(shape=[None,None], dtype=tf.float64),tf.TensorSpec(shape=[None,None], dtype=tf.float64))) 
    def _nondominated_comparison(self, f1,f2):
        '''
        Calculates number of individuals in f1 that are dominated by at least one individual in f2.
        '''
        D = f1[:,None,:] > f2[None,:,:]
        return tf.reduce_sum(tf.cast(tf.reduce_any(tf.reduce_all(D,axis=-1),axis=-1), tf.int64)) 

    @tf.function(input_signature=(tf.TensorSpec(shape=[None,None], dtype=tf.float64),tf.TensorSpec(shape=[None,None], dtype=tf.float64))) 
    def _calculate_mdr(self,f_prev,f_curr):
        '''
        Calculates the mutual domination rate.
        '''
        # Find indices of non-dominated front in each
        nd_prev,_ = self._find_nondominated(f_prev)
        nd_curr,_ = self._find_nondominated(f_curr)
        # Actually get non-dominated front for each
        f_prev_nd = tf.gather(f_prev,nd_prev,axis=0)
        f_curr_nd = tf.gather(f_curr,nd_curr,axis=0)
        
        M1 = self._nondominated_comparison(f_prev_nd,f_curr_nd) / tf.cast(tf.shape(f_prev_nd)[0], tf.int64)
        M2 = self._nondominated_comparison(f_curr_nd,f_prev_nd) / tf.cast(tf.shape(f_curr_nd)[0], tf.int64)
        
        return M1 - M2
    
    @tf.function(input_signature=(tf.TensorSpec(shape=[None,None], dtype=tf.float64),)) 
    def _calculate_filled_references(self,f):
        '''
        Calculates the proportion of reference directions with at least one associated individual
        '''
        # Find indices of non-dominated front
        nd_idx,_ = self._find_nondominated(f)
        # Actually get non-dominated front for each
        f_nd = tf.gather(f,nd_idx,axis=0)
        # Normalize f_last
        f_norm = self._adaptive_normalization(f_nd)
        # Get distance to ref. lines
        D = self._distance_to_references(f_norm)
        # Find associated ref. line for each fi
        min_d = tf.argmin(D,axis=-1, output_type=tf.int32)
        # Count number of associations per ref. line
        counts_per_ref = tf.math.bincount(min_d, dtype = tf.int32)
        # Sum reference directions with at least one association and divide by total number of reference directions
        return tf.reduce_sum(tf.cast(counts_per_ref > 0,tf.int32)) / tf.shape(self.ref_dirs)[0]
    
    @tf.function(input_signature=(tf.TensorSpec(shape=[None,None], dtype=tf.float64),)) 
    def _adaptive_normalization(self, f):
        '''
        Normlize fronts to allow comparison to unit reference directions
        '''
        f_norm = f - tf.reduce_min(f, axis=0, keepdims=True)
        return f_norm / tf.reduce_max(f_norm, axis=0, keepdims=True) 
    
    
    @tf.function(input_signature=(tf.TensorSpec(shape=[None,None], dtype=tf.float64),)) 
    def _distance_to_references(self, f):
        '''
        Reference directions are normalized to unit vectors in __init__
        '''
        # Calculate scalar projection of f onto r
        scalar_proj = tf.reduce_sum(tf.multiply(f[:,None,:], self.ref_dirs[None,:,:]),axis=-1)
        # Calculate f vector along r
        f_projection = (scalar_proj[:,:,None] * self.ref_dirs[None,:,:])
        # Get distance between f and f_projection and return
        return tf.norm((f[:,None,:] - f_projection),axis=-1)
     
    @tf.function(input_signature=(tf.TensorSpec(shape=[None,None], dtype=tf.float64),)) 
    def _drop_duplicates(self, X):
        '''
        Drops duplicate rows
        '''
        D = tf.reduce_all(X[:,None,:] == X[None,:,:], axis=-1)
        # D is nxn
        # Make nxn upper triangle mask
        UT = tf.cast(tf.linalg.band_part(tf.ones_like(D), 0, -1), tf.int32)
        # Apply mask to D
        D = tf.cast(D, tf.int32) * UT
        # Sum last axis
        D = tf.reduce_sum(D,axis=-1)
        # Keep indices with sum > 1
        keep_idx = tf.squeeze(tf.where(D==1))
        
        return tf.gather(X, keep_idx, axis=0)
    
    @tf.function(input_signature=(tf.TensorSpec(shape=[None,None], dtype=tf.float64),)) 
    def _find_nondominated(self, f):
        '''
        Find the non-dominated front in f and returns their indices.
        '''
        D = f[:,None,:] > f[None,:,:]
        dominated_by_n = tf.reduce_sum(tf.cast(tf.reduce_all(D,axis=-1), tf.int32),axis=-1)
        nd_idx = tf.squeeze(tf.where(dominated_by_n == 0))
        d_idx = tf.squeeze(tf.where(dominated_by_n > 0))
        return nd_idx, d_idx
    
    @tf.function(input_signature=(tf.TensorSpec(shape=[None,None], dtype=tf.float64),tf.TensorSpec(shape=[None,None], dtype=tf.float64)))   
    def _tournament(self, f, X):
        ''' 
        Apply tournament selection to choose individuals for crossover and mutation.
        '''
        
        n_elements = tf.shape(X)[0]
        # Define tensor array to hold data while performing tournaments
        X_ta = tf.TensorArray(tf.float64, size=self.population_size, dynamic_size=False)
        
        for i in tf.range(self.population_size):
            idx = tf.random.shuffle(tf.range(0, n_elements, dtype=tf.int32))[:self.tournament_size]
            ft = tf.gather(f,idx,axis=0)
            Xt = tf.gather(X,idx,axis=0)
            
            idx,_ = self._find_nondominated(ft)
            # If idx has multiple values, return the first
            idx = tf.cond(tf.rank(idx) > 0, lambda: idx[0], lambda: idx)
            
            X_ta = X_ta.write(i,Xt[idx])
        
        return X_ta.stack()
   
    
    def _selection(self, f, X):
        '''
        Fills up successive non-dominated fronts [F1,F2,...] until the number of
        individuals in the fronts is greater than or equal to the population size.
        If the number is greater, individuals from the last front are chosen to
        fill up under-represented reference directions, thereby maintaining diveristy.
        '''
        # Fill up non-dominated fronts [F1,F2,...]
        f_fronts = []
        X_fronts = []
        keepers = 0
        
        while keepers < self.population_size:
            
            # Get indices of non-dominated and dominated values
            nd_idx,d_idx = self._find_nondominated(f)
            
            # Make rank 1 if scalar
            if tf.rank(nd_idx) == 0:
                nd_idx = tf.reshape(nd_idx,(-1))
            
            # Select non-dominated front
            f_to_append = tf.gather(f,nd_idx,axis=0)
            X_to_append = tf.gather(X,nd_idx,axis=0)
            
            # Check rank and make rank 2 if a single value is selected
            if tf.rank(f_to_append) == 1:
                f_to_append = tf.reshape(f_to_append,(1,-1))
                X_to_append = tf.reshape(X_to_append,(1,-1))
            
            # Append to list of fronts
            f_fronts.append(f_to_append)
            X_fronts.append(X_to_append)
            
            # Select dominated front to reuse in while loop
            f = tf.gather(f,d_idx,axis=0)
            X = tf.gather(X,d_idx,axis=0)
            
            # Add length of last front to counter
            keepers += nd_idx.shape[0] 
                         
        
        # Sample from last front to maintain constance population size
        if keepers > self.population_size:
            # Get values from last front
            f_last = f_fronts[-1]
            X_last = X_fronts[-1]     
       
            # Calculate number of individuals to select
            n_to_sample = self.population_size - keepers + f_last.shape[0]  
            # Normalize f_last
            f_norm = self._adaptive_normalization(f_last)
            # Get distance to ref. lines
            D = self._distance_to_references(f_norm)
            # Find associated ref. line for each fi
            min_d = tf.argmin(D,axis=-1, output_type=tf.int32)
            # Count number of associations per ref. line
            counts_per_ref = tf.math.bincount(min_d, dtype = tf.int32)
            # Make into numpy to support assignment to indices
            counts_per_ref = counts_per_ref.numpy()
            D = D.numpy()
            # For storing selections
            f_select_idx = []
            for _ in range(n_to_sample):
                # Get ref. line with fewest associations
                ref_idx = np.argmin(counts_per_ref)
                # Find f with lowest D
                f_idx = np.argmin(D[:,ref_idx])
                # Append to list
                f_select_idx.append(f_idx)
                # Add 1 to index that was selected from
                counts_per_ref[ref_idx] += 1
                # Set value of D to inf to avoid selecting it again
                D[f_idx,ref_idx] = np.inf
            
            # Concatenate selected indices
            f_select_idx = tf.concat(f_select_idx, axis=0)
            
            # Update last front with selection
            f_last = tf.gather(f_last, f_select_idx, axis=0)
            X_last = tf.gather(X_last, f_select_idx, axis=0)
            
            # Check if rank 1 and make rank 2 if neccessary
            if tf.rank(f_last) == 1:
                f_last = tf.reshape(f_last,(1,-1))
                X_last = tf.reshape(X_last,(1,-1))
            
            # Update last front with selected individuals
            f_fronts[-1] = f_last
            X_fronts[-1] = X_last
        
        # Concatenate and return
        f = tf.concat(f_fronts, axis=0)
        X = tf.concat(X_fronts, axis=0)
        return f,X

    def __call__(self):
        '''
        The NSGA3 algorithm is implemented here:
            1. Select parents using tournament selection
            2. Generate children using crossover.
            3. Apply mutation to children.
            4. Select non-dominated solutions from parents and children.
            
        '''
        # Calculate statistics before starting optimization
        parents = self.population['X']
        f_new = self.obj_func(parents)
        mdr = self._calculate_mdr(f_new,f_new)
        refs = self._calculate_filled_references(f_new)

        if self.verbose: print('Generation 0 – MDR {} – Ref dirs {}%     '.format(np.round(mdr.numpy(),2),np.round(100*refs.numpy())), end = '\r')

        # Add statistics
        self.population.statistics['gen'] = 0
        self.population.statistics['mdr'] = mdr
        self.population.statistics['refs'] = refs
        
        for gen in range(1, self.generations+1):
            
            # f_prev is retained to calculate MDR
            f_prev = f_new
            # Tournament selection for crossover
            child1 = self._tournament(f_new, parents)
            child2 = self._tournament(f_new, parents)
            # Perform crossover
            children = self.crossover(child1,child2)
            # Perform mutation on children
            children = self.mutation(children)
            # Concat parents and children
            parents = tf.concat([parents,children],axis=0)
            
            # Remove duplicate individuals
            parents = self._drop_duplicates(parents)
                    
            # Calculate fitness of parents and children
            f_new = self.obj_func(parents)
            # Select best from parents and children to form next generation
            f_new, parents = self._selection(f_new, parents)
            
            if gen % self.record_gens == 0: 
                
                # For statistics
                mdr = self._calculate_mdr(f_prev,f_new)
                refs = self._calculate_filled_references(f_new)

                if self.verbose: print('Generation {} – MDR {} – Ref dirs {}%     '.format(gen,np.round(mdr.numpy(),2),np.round(100*refs.numpy())), end = '\r')

                # Add statistics
                self.population.statistics['gen'] = gen
                self.population.statistics['mdr'] = mdr
                self.population.statistics['refs'] = refs
                
            
        # Get non-dominated front to return
        nd_idx,_ = self._find_nondominated(f_new)
        self.population['X'] = tf.gather(parents, nd_idx, axis=0)
        self.population['fitness'] = tf.gather(f_new, nd_idx, axis=0)
        
        if self.verbose: print('\nComplete – non-dominated front size: {}'.format(nd_idx.shape[0]))
        return self.population

    
    
class muPlusLambda:
    '''
    The muPlusLambda algorithm uses tournament selection to choose individuals
    for mating. Simulated binary crossover is applied followed by polynomial
    mutation. The population carried on to the next generation is chosen from the
    resultant children and the parents.
    
    This algorithm is a minimizer. Objectives to be maximized should be returned
    from the objective function as the negative (:math:`-f(X)`).
    
    This algoritm may break if the positions (X) converge or the objective function
    values converge. This can be set using the `position_tolerance` and 
    `func_tolerance` arguments. Convergence will only be checked every
    `record_gens` generations.
    
    
    Parameters
    ----------
    obj_func : function Y = f(X)
        Objective function that takes only a tensor X of shape (None,n_variables)
        and returns a tensor of fitness values of shape (None,1).
    n_variables : int
        The number of variables in X.
    population_size : int, optional
        The size of the population to generate. May not be exact. The default is 15.
    tournament_size : int, optional
        Tournament selection is used to choose individuals to perform crossover with.
        Must be >2 and <population_size. The default is 2.
    upperbound : float, list, tuple, optional
        Upper bounds for X. The default is 1.0.
    lowerbound : float, list, tuple, optional
        Lower bounds for X. The default is -1.0.
    generations : int, optional
        Number of generations to evolve. The default is 1000.
    mutation_prob : float, optional
        The probability of mutating an element in an individual solution.
        The default is 0.3.
    crossover_prob : float, optional
        The probability of performing crossover on an element in an individual solution.
        The default is 0.7.
    mutation_eta : float, optional
        Controls the degree of mutation. Higher values generate children
        that are more similar to their parents. The default is 1.0.
    crossover_eta : float, optional
        Controls the degree of crossover. Higher values generate children
        that are more similar to their parents. The default is 1.0.
    func_tolerance : float, optional
        If the absolute difference between the minimum and maximum fitness is < func_tolerance,
        the algorithm will break. The default is 0.0.
    position_tolerance : float, optional
        If the absolute difference between the minimum and maximum fitness is < func_tolerance,
        the algorithm will break. The default is 1e-8.
    record_gens : int, optional
        How often to record statistics and check for convergence. The default is
        10 generations.
    verbose : bool
        Whether to print progress to screen. The default is True.
    seed : int, optional
        Random seed. The default is None.

    Returns
    -------
    :class:`gatf.population.Population`
        Optimization results as dict-like key/value pairs including 'X', 'fitness',
        and 'statistics'. Also includes the best-ever individual 'X_best' and its
        associated fitness 'fitness_best'. The statistics key contains a
        :class:`population.Statistics` object with the keys 'gen', 'X_min', 
        'X_mean', and 'X_max'.
    
        
    Notes
    -----
    The input signatures are defined for Tensorflow functions to avoid
    graph retracing and, therefore, this algorithm expects a tf.float64 datatype.
    Objective functions should be designed to output the proper datatype or an 
    error with be thrown. Custom objectives should also make use of
    the @tf.function decorator to allow compilation into the Tensorflow graph.
    
    >>> @tf.function(input_signature=(tf.TensorSpec(shape=[None,n_objectives], dtype=tf.float64),))
    >>> def my_custom_objective(X):
    >>>    # calculate fitness here
    >>>    return fitness
    
    Providing an input signature is not absolutely necessary but recommended if
    a warning is raised that the graph is being retraced. 
    
    Examples
    --------
    The muPlusLambda algorithm is first instantiated with the desired objective and 
    hyperparameters, then it is called to begin the optimization.
    
    >>> # Initialize muPlusLambda
    >>> optimizer = muPlusLambda(my_custom_objective, n_variables, ...)
    >>> # Run the optimizer
    >>> results = optimizer()
    
    The returned results object contains key-accessible values (like a dict).
    
    >>> # Get the final best solution
    >>> results['X_best']
    <tf.Tensor: shape=(1,n_variables), dtype=float64, numpy=...>
    >>> # Get the associated fitnesses
    >>> results['fitness_best']
    <tf.Tensor: shape=(1,1), dtype=float64, numpy=...>
    
    Additionally, statistics are recorded throughout the optimization. The
    statistics object contains lists of values that are either numbers or tensors.
    
    >>> # Get the generations that were recorded
    >>> results['statistics']['gen']
    [0,10,20,...]
    >>> # Get the statistic recorded associated with each generation
    >>> results['statistics']['X_mean']
    [<tf.Tensor: shape=(), dtype=float64, numpy=...>, <tf.Tensor: shape=(), dtype=float64, numpy=...>, ...]
    
    These can be made into a single numpy array for plotting
    
    >>> np.array(results['statistics']['X_mean'])
    array([...])

    '''
    def __init__(self,
                 obj_func,
                 n_variables,
                 population_size = 15,
                 tournament_size = 2,
                 upperbound=1.0,
                 lowerbound=-1.0,
                 generations=1000,
                 mutation_prob=0.3,
                 crossover_prob=0.7,
                 mutation_eta=1.0,
                 crossover_eta=1.0,
                 func_tolerance=0.0,
                 position_tolerance=1e-8,
                 record_gens=10,
                 verbose=True,
                 seed=None):
    
        if seed is not None:
            tf.random.set_seed(seed)
           
        self.verbose = verbose
        
        assert tournament_size < population_size
        
        # Make 1D tensors of bounds
        if isinstance(upperbound,Number):
            upperbound = tf.constant(upperbound, shape=n_variables, dtype=tf.float64)
        elif isinstance(upperbound,(list,tuple)):
            assert len(upperbound) == n_variables
            upperbound = tf.constant(upperbound, dtype = tf.float64)
        else:
            raise TypeError
            
        if isinstance(lowerbound,Number):
            lowerbound = tf.constant(lowerbound, shape=n_variables, dtype=tf.float64)
        elif isinstance(lowerbound,(list,tuple)):
            assert len(lowerbound) == n_variables
            lowerbound = tf.constant(lowerbound, dtype = tf.float64)
        else:
            raise TypeError
        # Check that all upperbound >= lowerbound
        # Permits upper==lower to allow some values to be fixed
        assert tf.reduce_all(upperbound>=lowerbound)
        
        self.generations = generations
        self.population_size = tf.constant(population_size, dtype=tf.int32)
        self.tournament_size = tf.constant(tournament_size, dtype=tf.int32)
        self.n_variables = tf.constant(n_variables, dtype=tf.int32)
        self.func_tolerance = func_tolerance
        self.position_tolerance = position_tolerance
        self.record_gens = record_gens
        self.obj_func = obj_func
        
        # Randomly initialize populations
        if n_variables < 5:
            initial_population = population.initialize_uniform_population(population_size, lowerbound, upperbound)
        else:
            initial_population = population.initialize_normal_population(population_size, lowerbound, upperbound)
        
        # Creat population object to hold individuals and their fitness
        self.population = population.Population(initial_population)
        
        # Initialize crossover and mutation objects
        self.crossover = operators.SimulatedBinaryCx(lowerbound=lowerbound,
                                                     upperbound=upperbound,
                                                     prob_per_var=crossover_prob,
                                                     eta=crossover_eta)
        self.mutation = operators.PolynomialMutation(lowerbound = lowerbound,
                                                     upperbound = upperbound,
                                                     prob_per_var=mutation_prob,
                                                     eta=mutation_eta)
    

    @tf.function(input_signature=(tf.TensorSpec(shape=[None,1], dtype=tf.float64),
                                  tf.TensorSpec(shape=[None,None], dtype=tf.float64),
                                  tf.TensorSpec(shape=[None,1], dtype=tf.float64),
                                  tf.TensorSpec(shape=[None,None], dtype=tf.float64))) 
    def _select_best(self, f_curr, X_curr, f_best, X_best):
        '''
        Finds the current best individual and compares it to the all-time best.
        '''
        # Get index of best current fitness
        best_fit = tf.argmin(tf.squeeze(f_curr), axis=0)
        # Actually get best fitness and solution
        f_curr_best = f_curr[best_fit]
        X_curr_best = tf.reshape(X_curr[best_fit,:], (1,-1))
        # Compare with gbest fitness
        better_fit = f_curr_best<f_best
        # Apply boolean mask to update pbest
        X_best = X_best * tf.cast(~better_fit, tf.float64) + X_curr_best * tf.cast(better_fit, tf.float64)
        f_best = f_best * tf.cast(~better_fit, tf.float64) + f_curr_best * tf.cast(better_fit, tf.float64)
        return f_best, tf.reshape(X_best, (1,-1))
           
    @tf.function(input_signature=(tf.TensorSpec(shape=[None,None], dtype=tf.float64),tf.TensorSpec(shape=[None,None], dtype=tf.float64)))  
    def _selection(self, f, X):
        '''
        Sorts individuals according to their fitness
        '''
        f_idx = tf.argsort(tf.squeeze(f),axis=0)
        f = tf.gather(f, f_idx, axis=0)
        X = tf.gather(X, f_idx, axis=0)
        
        return f[:self.population_size], X[:self.population_size]
     
    @tf.function(input_signature=(tf.TensorSpec(shape=[None,None], dtype=tf.float64),tf.TensorSpec(shape=[None,None], dtype=tf.float64)))   
    def _tournament(self, f, X):
        '''
        Applies tournament selection to choose individuals for crossover and mutation
        '''
        n_elements = tf.shape(X)[0]
        # Define tensor arrays to hold data while performing tournaments
        f_ta = tf.TensorArray(tf.float64, size=self.population_size, dynamic_size=False)
        X_ta = tf.TensorArray(tf.float64, size=self.population_size, dynamic_size=False)
        
        for i in tf.range(self.population_size):
            idx = tf.random.shuffle(tf.range(0, n_elements, dtype=tf.int32))[:self.tournament_size]
            ft = tf.gather(f,idx,axis=0)
            Xt = tf.gather(X,idx,axis=0)
            idx = tf.squeeze(tf.argmin(ft, axis=0))
            f_ta = f_ta.write(i,ft[idx])
            X_ta = X_ta.write(i,Xt[idx])
        
        return f_ta.stack(), X_ta.stack()

   
        
    def __call__(self):
        '''
        The muPlusLambda algorithm is implemented here:
            1. Select parents using tournament selection
            2. Generate children using crossover.
            3. Apply mutation to children.
            4. Select best solutions from parents and children.
            
        '''  
        # Get population and calculate fitness
        parents = self.population['X']
        fitness = self.obj_func(parents)
        
        fitness, parents = self._selection(fitness,parents)
        # Assign value to best solution
        f_best = tf.reshape(fitness[0], (1,-1))
        X_best = tf.reshape(parents[0], (1,-1))
        
        # Calculate statistics
        f_mean,f_min,f_max = tf.reduce_mean(fitness),tf.reduce_min(fitness),tf.reduce_max(fitness)
        
        # Add statistics
        self.population.statistics['gen'] = 0
        self.population.statistics['fitness_min'] = f_min
        self.population.statistics['fitness_max'] = f_max
        self.population.statistics['fitness_mean'] = f_mean
        self.population.statistics['fitness_best'] = f_best
        
        if self.verbose: print('Generation 0 – min {} - mean {} – max {} – best {}   '.format(np.round(f_min.numpy(),2),np.round(f_mean.numpy(),2),np.round(f_max.numpy(),2),np.round(tf.squeeze(f_best).numpy(),2)), end = '\r')
        
        for gen in range(1, self.generations+1):
            # Apply tournament selection
            _,child1 = self._tournament(fitness, parents)
            _,child2 = self._tournament(fitness, parents)
            # Perform crossover
            children = self.crossover(child1,child2)
            # Perform mutation on children
            children = self.mutation(children)
            # Concat parents and children
            parents = tf.concat([parents,children],axis=0)
            # Calculate fitness of parents and children
            fitness = self.obj_func(parents)
            # Select best from parents and children to form next generation
            fitness, parents = self._tournament(fitness,parents)
            # fitness, parents = self._selection(fitness,parents)

            # Update best solution
            f_best,X_best = self._select_best(fitness, parents, f_best, X_best)
            
            if gen % self.record_gens == 0: 
                # For statistics and to check for convergence
                f_mean,f_min,f_max = tf.reduce_mean(fitness),tf.reduce_min(fitness),tf.reduce_max(fitness)
                X_min,X_max = tf.reduce_min(parents, axis=0),tf.reduce_max(parents, axis=0)
                
                # Add statistics
                self.population.statistics['gen'] = gen
                self.population.statistics['fitness_min'] = f_min
                self.population.statistics['fitness_max'] = f_max
                self.population.statistics['fitness_mean'] = f_mean
                self.population.statistics['fitness_best'] = f_best
                
                if self.verbose: print('Generation {} – min {} - mean {} – max {} – best {}   '.format(gen,np.round(f_min.numpy(),2),np.round(f_mean.numpy(),2),np.round(f_max.numpy(),2),np.round(tf.squeeze(f_best).numpy(),2)), end = '\r')
                
                # Check convergence and break if converged
                if f_max-f_min < self.func_tolerance:
                    if self.verbose: print('\nFitness converged at gen {}'.format(gen), end = '\r')
                    break
                elif tf.reduce_all(X_max-X_min < self.position_tolerance):
                    if self.verbose: print('\nPositions converged at gen {}'.format(gen), end = '\r')
                    break
        
        # Update population object
        self.population['X'] = parents
        self.population['fitness'] = fitness
        self.population['X_best'] = X_best
        self.population['fitness_best'] = f_best
        
        if self.verbose: print('\nComplete')
        return self.population
        
        
class PSO:
    '''
    Particle swarm optimization. Moves particles with a velocity calculated by
    that particle's inertia, best ever position, and the global best particle's position.
    
    This algorithm is a minimizer. Objectives to be maximized should be returned
    from the objective function as the negative (:math:`-f(X)`).
    
    This algoritm may break if the positions (X) converge or the objective function
    values converge. This can be set using the `position_tolerance` and 
    `func_tolerance` arguments. Convergence will only be checked every
    `record_gens` generations.
    
    Parameters
    ----------
    obj_func : function Y = f(X)
        Objective function that takes only a tensor X of shape (None,n_variables)
        and returns a tensor of fitness values of shape (None,1) with dtype tf.float64.
    n_variables : int
        The number of variables in X.
    population_size : int, optional
        The size of the population to generate. The default is 15.
    upperbound : float, list, tuple, optional
        Upper bounds for X. The default is 1.0.
    lowerbound : float, list, tuple, optional
        Lower bounds for X. The default is -1.0.
    generations : int, optional
        Number of generations to evolve. The default is 1000.
    inertia : float, optional
        Inertia of particles. Higher inertia makes it harder for particles to
        change directions. If this value is too high the optimizer may never
        converge. The default is 0.8.
    cognitive_coeff : float
        The influence of a particle's best ever position on its velocity. 
        The default is 0.1.
    social_coeff : float
        The influence of the global best particles position on a particle's velocity.
        The default is 0.1.
    func_tolerance : float, optional
        If the absolute difference between the minimum and maximum fitness is < func_tolerance,
        the algorithm will break. The default is 0.0.
    position_tolerance : float, optional
        If the absolute difference between the minimum and maximum fitness is < func_tolerance,
        the algorithm will break. The default is 1e-8.
    record_gens : int
        How often to record statistics and check for convergence. The default is
        10 generations.
    verbose : bool
        Whether to print progress to screen. The default is True.
    seed : int, None
        Random seed. The default is None.

    Returns
    -------
    :class:`gatf.population.Population`
        Optimization results as dict-like key/value pairs including 'X', 'fitness',
        and 'statistics'. Also includes the best-ever individual 'X_best' and its
        associated fitness 'fitness_best'. The statistics key contains a
        :class:`population.Statistics` object with the keys 'gen', 'X_min', 
        'X_mean', and 'X_max'.
        
        
    Notes
    -----
    The input signatures are defined for Tensorflow functions to avoid
    graph retracing and, therefore, this algorithm expects a tf.float64 datatype.
    Objective functions should be designed to output the proper datatype or an 
    error with be thrown. Custom objectives should also make use of
    the @tf.function decorator to allow compilation into the Tensorflow graph.
    
    >>> @tf.function(input_signature=(tf.TensorSpec(shape=[None,n_objectives], dtype=tf.float64),))
    >>> def my_custom_objective(X):
    >>>    # calculate fitness here
    >>>    return fitness
    
    Providing an input signature is not absolutely necessary but recommended if
    a warning is raised that the graph is being retraced. 
    
    Examples
    --------
    The PSO algorithm is first instantiated with the desired objective and 
    hyperparameters, then it is called to begin the optimization.
    
    >>> # Initialize PSO
    >>> optimizer = PSO(my_custom_objective, n_variables, ...)
    >>> # Run the optimizer
    >>> results = optimizer()
    
    The returned results object contains key-accessible values (like a dict).
    
    >>> # Get the final best solution
    >>> results['X_best']
    <tf.Tensor: shape=(1,n_variables), dtype=float64, numpy=...>
    >>> # Get the associated fitnesses
    >>> results['fitness_best']
    <tf.Tensor: shape=(1,1), dtype=float64, numpy=...>
    
    Additionally, statistics are recorded throughout the optimization. The
    statistics object contains lists of values that are either numbers or tensors.
    
    >>> # Get the generations that were recorded
    >>> results['statistics']['gen']
    [0,10,20,...]
    >>> # Get the statistic recorded associated with each generation
    >>> results['statistics']['X_mean']
    [<tf.Tensor: shape=(), dtype=float64, numpy=...>, <tf.Tensor: shape=(), dtype=float64, numpy=...>, ...]
    
    These can be made into a single numpy array for plotting
    
    >>> np.array(results['statistics']['X_mean'])
    array([...])

    '''
    def __init__(self,
                 obj_func,
                 n_variables,
                 population_size = 15,
                 upperbound=1.0,
                 lowerbound=-1.0,
                 generations=1000,
                 inertia=0.8,
                 cognitive_coeff=0.1,
                 social_coeff=0.1,
                 func_tolerance=0.0,
                 position_tolerance=1e-8,
                 record_gens=10,
                 verbose=True,
                 seed=None):
    
        if seed is not None:
            tf.random.set_seed(seed)
        
        self.verbose = verbose
        
        # Make 1D tensors of bounds
        if isinstance(upperbound,Number):
            upperbound = tf.constant(upperbound, shape=n_variables, dtype=tf.float64)
        elif isinstance(upperbound,(list,tuple)):
            assert len(upperbound) == n_variables
            upperbound = tf.constant(upperbound, dtype = tf.float64)
        else:
            raise TypeError
            
        if isinstance(lowerbound,Number):
            lowerbound = tf.constant(lowerbound, shape=n_variables, dtype=tf.float64)
        elif isinstance(lowerbound,(list,tuple)):
            assert len(lowerbound) == n_variables
            lowerbound = tf.constant(lowerbound, dtype = tf.float64)
        else:
            raise TypeError
        # Check that all upperbound >= lowerbound
        # Permits upper==lower to allow some values to be fixed
        assert tf.reduce_all(upperbound>=lowerbound)
        
        self.generations = generations
        self.population_size = tf.constant(population_size, dtype=tf.int32)
        self.n_variables = tf.constant(n_variables, dtype=tf.int32)
        self.inertia = tf.constant(inertia, dtype=tf.float64)
        self.cog_coeff = tf.constant(cognitive_coeff, dtype=tf.float64)
        self.soc_coeff = tf.constant(social_coeff, dtype=tf.float64)
        self.func_tolerance = func_tolerance
        self.position_tolerance = position_tolerance
        self.record_gens = record_gens
        self.obj_func = obj_func
        
        # Randomly initialize population position and velocity
        if n_variables < 5:
            initial_population = population.initialize_uniform_population(population_size, lowerbound, upperbound)
        else:
            initial_population = population.initialize_normal_population(population_size, lowerbound, upperbound)
        
        # Creat particle object to hold individuals and their fitness
        self.particles = population.Population(initial_population)
        
    
    @tf.function(input_signature=(tf.TensorSpec(shape=[None,1], dtype=tf.float64),
                                  tf.TensorSpec(shape=[None,None], dtype=tf.float64),
                                  tf.TensorSpec(shape=[None,1], dtype=tf.float64),
                                  tf.TensorSpec(shape=[None,None], dtype=tf.float64))) 
    def _set_particle_best(self, f_curr, X_curr, f_particle, X_particle):
        ''' 
        Updates a particles all-time best position
        '''
        # Make boolean mask where new fitness is better than pbest
        better_fit = f_curr<f_particle
        # Apply boolean mask to update pbest
        X_particle = X_particle * tf.cast(~better_fit, tf.float64) + X_curr * tf.cast(better_fit, tf.float64)
        f_particle = f_particle * tf.cast(~better_fit, tf.float64) + f_curr * tf.cast(better_fit, tf.float64)
        return tf.reshape(f_particle, (-1,1)), X_particle
        
    
    @tf.function(input_signature=(tf.TensorSpec(shape=[None,1], dtype=tf.float64),
                                  tf.TensorSpec(shape=[None,None], dtype=tf.float64),
                                  tf.TensorSpec(shape=[None,1], dtype=tf.float64),
                                  tf.TensorSpec(shape=[None,None], dtype=tf.float64))) 
    def _set_global_best(self, f_curr, X_curr, f_global, X_global):
        ''' 
        Updates the global best particle
        '''
        # Get index of best current fitness
        best_fit = tf.argmin(tf.squeeze(f_curr), axis=0)
        # Actually get best fitness and solution
        f_curr_best = f_curr[best_fit]
        X_curr_best = tf.reshape(X_curr[best_fit,:], (1,-1))
        # Compare with gbest fitness
        better_fit = f_curr_best<f_global
        # Apply boolean mask to update pbest
        X_global = X_global * tf.cast(~better_fit, tf.float64) + X_curr_best * tf.cast(better_fit, tf.float64)
        f_global = f_global * tf.cast(~better_fit, tf.float64) + f_curr_best * tf.cast(better_fit, tf.float64)
        return f_global, tf.reshape(X_global, (1,-1))
    
    
    @tf.function(input_signature=(tf.TensorSpec(shape=[None,None], dtype=tf.float64),
                                  tf.TensorSpec(shape=[None,None], dtype=tf.float64))) 
    def _set_position(self, X_curr, V_curr):
        ''' 
        Calculate a particles new position
        '''
        return X_curr + V_curr
    
    
    @tf.function(input_signature=(tf.TensorSpec(shape=[None,None], dtype=tf.float64),
                                  tf.TensorSpec(shape=[None,None], dtype=tf.float64),
                                  tf.TensorSpec(shape=[None,None], dtype=tf.float64),
                                  tf.TensorSpec(shape=[None,None], dtype=tf.float64))) 
    def _set_velocity(self, X_curr, V_curr, X_particle, X_global):
        ''' 
        Calculate a particles new velocity
        '''
        return self.inertia * V_curr + self.cog_coeff * tf.random.uniform((self.population_size,1), dtype=tf.float64) * (X_particle - X_curr) + self.soc_coeff * tf.random.uniform((self.population_size,1), dtype=tf.float64) * (X_global - X_curr)
    
    def __call__(self):
        '''
        The particle swarm optimization algorithm is implemented here:
            1. Use the particle and global best to update each particles velocity
            2. Use the updated velocity to update each particles position
            3. Set new particle and global best
            
        '''  
        
        # Get initial population and calculate fitness
        particles = self.particles['X']
        fitness = self.obj_func(particles)
        # Set particle best to current population
        pbest_X = particles
        pbest_f = fitness
        # Set gbest to a random particle
        idx = np.random.choice(self.population_size)
        
        gbest_X = tf.reshape(particles[idx], (1,-1))
        gbest_f = tf.reshape(fitness[idx], (1,-1))
        
        # Update global best
        gbest_f,gbest_X = self._set_global_best(fitness, particles, gbest_f, gbest_X)
        # Initialize random velocities
        velocity = tf.random.normal((self.population_size, self.n_variables), mean=0.0, stddev=0.2, dtype=tf.float64)
   
        # For statistics
        f_mean,f_min,f_max = tf.reduce_mean(fitness),tf.reduce_min(fitness),tf.reduce_max(fitness)
        
        # Add statistics
        self.particles.statistics['gen'] = 0
        self.particles.statistics['fitness_min'] = f_min
        self.particles.statistics['fitness_max'] = f_max
        self.particles.statistics['fitness_mean'] = f_mean
        self.particles.statistics['fitness_best'] = tf.squeeze(gbest_f)
        
        if self.verbose: print('Generation 0 – min {} - mean {} – max {} – best {}   '.format(np.round(f_min.numpy(),2),np.round(f_mean.numpy(),2),np.round(f_max.numpy(),2),np.round(tf.squeeze(gbest_f).numpy(),2)), end = '\r')
        
        for gen in range(1, self.generations+1):
            
            # Update velocity
            velocity = self._set_velocity(particles, velocity, pbest_X, gbest_X)
            # Update position
            particles = self._set_position(particles, velocity)
            # Calculate fitness
            fitness = self.obj_func(particles)
            # Update particle best
            pbest_f,pbest_X = self._set_particle_best(fitness, particles, pbest_f, pbest_X)
            # Update global best
            gbest_f,gbest_X = self._set_global_best(fitness, particles, gbest_f, gbest_X)
            
            if gen % self.record_gens == 0: 
                # For statistics and to check for convergence
                f_mean,f_min,f_max = tf.reduce_mean(fitness),tf.reduce_min(fitness),tf.reduce_max(fitness)
                X_min,X_max = tf.reduce_min(particles, axis=0),tf.reduce_max(particles, axis=0)
                
                # Add statistics
                self.particles.statistics['gen'] = gen
                self.particles.statistics['fitness_min'] = f_min
                self.particles.statistics['fitness_max'] = f_max
                self.particles.statistics['fitness_mean'] = f_mean
                self.particles.statistics['fitness_best'] = tf.squeeze(gbest_f)
                
                if self.verbose: print('Generation {} – min {} - mean {} – max {} – best {}   '.format(gen,np.round(f_min.numpy(),2),np.round(f_mean.numpy(),2),np.round(f_max.numpy(),2),np.round(tf.squeeze(gbest_f).numpy(),2)), end = '\r')
                
                # Check convergence and break if converged
                if f_max-f_min < self.func_tolerance:
                    if self.verbose: print('\nFitness converged at gen {}'.format(gen), end = '\r')
                    break
                elif tf.reduce_all(X_max-X_min < self.position_tolerance):
                    if self.verbose: print('\nPositions converged at gen {}'.format(gen), end = '\r')
                    break
        
        # Update population object
        self.particles['X'] = particles
        self.particles['fitness'] = fitness
        self.particles['X_best'] = gbest_X
        self.particles['fitness_best'] = gbest_f
        
        if self.verbose: print('\nComplete')
        return self.particles
        
        
        