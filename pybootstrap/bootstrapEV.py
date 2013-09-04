#!/usr/bin/env python
#*-* Coding: UTF-8 *-*
__title__ = "bootstrapEV"
__author__ = "Eduardo S. Pereira"
__email__ = "pereira.somoza@gmail.com"
__data__ = "31/09/2013"
__versio__ = "0.1"

import numpy
from random import choice
import multiprocessing as mpg
import os
import time
import sys


"""
Bootstrap resample with replacement as described by
Wherens et al. 2000

Wherens, R. et al., 2000. Chemometrics and Inteligent Laboratory System, 54, 35
"""


def fncache(fn):
    """
   Function caching decorator. Keeps a cache of the return
   value of a function and serves from cache on consecutive
   calls to the function.

   Cache keys are computed from a hash of the function
   name and the parameters (this differentiates between
   instances through the 'self' param). Only works if
   parameters have a unique repr() (almost everything).

   Example:

   >>> @fncache
   ... def greenham(a, b=2, c=3):
   ...   print 'CACHE MISS'
   ...   return('I like turtles')
   ...
   >>> print greenham(1)           # Cache miss
   CACHE MISS
   I like turtles
   >>> print greenham(1)           # Cache hit
   I like turtles
   >>> print greenham(1, 2, 3)     # Cache miss (even though default params)
   CACHE MISS
   I like turtles
   >>> print greenham(2, 2, ['a']) # Cache miss
   CACHE MISS
   I like turtles
   >>> print greenham(2, 2, ['b']) # Cache miss
   CACHE MISS
   I like turtles
   >>> print greenham(2, 2, ['a']) # Cache hit
   I like turtles
   """
    def new(*args, **kwargs):
        h = hash(repr(fn) + repr(args) + repr(kwargs))
        if not h in __cache:
            __cache[h] = fn(*args, **kwargs)
        return(__cache[h])
    new.__doc__ = "%s %s" % (fn.__doc__, "(cached)")
    return(new)


# Global cache
__cache = {}


class bootstrapEV:
    """
Bootstrap resample with replacement
    """
    def __init__(self, sample, B):
        """
        sample: a numpy array of the sample
        B : Number of Bootstrap resamples
        """
        self.sample = sample
        self.sSize = sample.size
        self.expecValueSample = sample.mean()
        self.B = B
        self.AllBootstrap = None
        self.Bias = None
        self.Std = None
        self.Cinterval = None

    def __resample(self):
        '''
        Peforme the bootstrap with replacement from a sample
        '''
        r = xrange(self.sample.shape[0])
        r = [choice(r) for _ in r]
        return numpy.array([self.sample[r]])

    def resample(self):
        """
        Return a array of arraies with the all bootstrap sample
        """
        def rsample(B):
            return [self.__resample() for i in range(B)]

        self.AllBootstrap = rsample(self.B)
        return self.AllBootstrap

    def __error(self):
        squarM = [(self.AllBootstrap[i].mean() - self.expecValueSample) ** 2.0
                            for i in range(self.B)]
        squarM = numpy.array(squarM)
        err = numpy.sqrt(squarM.sum() / self.B)
        return err

    def std(self):
        if(self.AllBootstrap is not None):
            return self.__error()
        else:
            self.resample()
            return self.__error()

    def __bias(self):
        bsEV = numpy.array([self.AllBootstrap[i].mean()
                            for i in range(self.B)])
        bias = bsEV.mean() - self.expecValueSample
        return bias

    def bias(self):
        if(self.AllBootstrap is not None):
            return self.__bias()
        else:
            self.resample()
            return self.__bias()

    def __confidence(self, percentil):

        qup = (self.B + 1.0) * (1.0 - percentil / 2.0)
        qup = int(qup) - 1
        qlow = (self.B + 1.0) * (percentil / 2.0)
        qlow = int(qlow) - 1
        bsEV = numpy.array([self.AllBootstrap[i].mean()
                            for i in range(self.B)])
        CI = numpy.sort(bsEV)
        return [CI[qlow], CI[qup]]

    def confidence(self, percentil):
        if(self.AllBootstrap is not None):
            return self.__confidence(percentil)
        else:
            self.resample()
            return self.__confidence(percentil)





