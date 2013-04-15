#!/usr/bin/env python
__title__ = "bootstrap"
__author__ = "Eduardo S. Pereira"
__email__ = "pereira.somoza@gmail.com"
__data__ = "12/04/2013"
__versio__ = "0.1"

import numpy
import scipy.optimize as sopt
from random import choice
import multiprocessing as mpg
import os
import time
import sys

import matplotlib
import matplotlib.pyplot as plt

"""
Bootstrap resample with replacement as described by
Wherens et al. 2000

Wherens, R. et al., 2000. Chemometrics and Inteligent Laboratory System, 54, 35


This file is part of PyBootstrap.
    copyright : Eduardo dos Santos Pereira
    15 april 2013

    PyBootstrap is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.
    PyGraWC is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""


def optimizer(p0, sample, func):
    """
    Given a parametric function in lambda format and a start parameters, return the 
    best fit parameter from a data
    Arguments:
        p0 - list with parameters
        sample: a bidimensional array been the collunm 0 the  x values and 1 the y values of the sample
        func - function: 
                ex : 
                    func = lambda p,x: p[0]*x+p[1]
                The last argument must be x
    """
    DOF = sample.shape[0]-len(p0)
    
    def residual(p,sample):
        y = sample[:, 1]
        x = sample[:, 0]
        p1 = [p]
        Y = []            
        sigma = sample.std()
        if(sigma == 0):
            sigma = DOF
        tmp = p1
        tmp.append(0)
        for xi in x:                
            tmp[-1] = xi
            Y.append(func(*tmp))
            
        Y = numpy.array(Y)
        return (y-Y)/sigma
        
    plsq=sopt.leastsq(residual,p0,args=(sample))
    return plsq[0]
    

def plotHistoFreq(parameter, bin=20, percentil=95, low=False, up=False, xalbel=r'parameter'):
    """
    Given a sample of bootstrap parameter, plot the frequence histogram
    parameters:
        parameter : Array of parameters
        bin:  bin of data
        percentil : Percentil confincende level
        low : Value of low percentil
        up : Value of up percentil
        xalbel: x label 
    """

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(211)
    font = {'weight' : 'bold',
    'size'   : 22}

    matplotlib.rc('font', **font)
    matplotlib.rcParams['text.usetex'] = True
    if(low != False):
        ax1.hist(parameter, bin, label=r'p $\le$ %s %s : $[%1.2f, %1.2f]$'\
                                                           %( percentil,'$\%$', low, up))
    else:
        ax1.hist(parameter, bin, (parameter[0], parameter[-1]))
    ax1.legend()
    ax1.set_xlabel(xalbel)
    ax1.set_ylabel('Frequency')
    plt.show()


class parallelization:
    
    def __init__(self, func, N):
        self.func = func
        self.N  = N
    
    def parallel(self,func, n,q,Dmatriz,n_process):     
        E=Dmatriz/n_process
        k=n*E
        q.put(func(k,E,n))
    
    def myPool(self):
        n_process=mpg.cpu_count()
        subprocess=[]    
    
        for i in range(n_process):
            q = mpg.Queue()
            p=mpg.Process(target=self.parallel,\
                args=(self.func, i,q,self.N,n_process))
            p.start()
            subprocess.append(p)
            
        while subprocess:
            subprocess.pop().join()
    


class bootstrap:
    """
Bootstrap resample with replacement as described by
Wherens et al. 2000

Wherens, R. et al., 2000. Chemometrics and Inteligent Laboratory System, 54, 35
    """
    def __init__(self, sample, B, func=None):
        """
        sample: a bidimensional array been the collunm 0 the  x values and 1 the y values of the sample
        B : Number of Bootstrap resamples
        func : function to be minizades, Optional
            This function must be contruced in the follow way: first argument is a list of parameter, second argument is the x variable
                ex : 
                    func = lambda p,x: p[0]*x+p[1]
                The last argument must be x
        """
        self.sample = sample
        self.sSize = sample.size
        self.B = B
        self.func = func
        self.AllBootstrap = None
        self.p = None
        self.allParameters = None
        self.Bias = None
        self.Std = None
        self.Cinterval = None
    
    def __resample(self):
        '''
        Peforme the bootstrap with replacement from a sample
        '''
        r = xrange(self.sample.shape[0])
        r = [choice(r) for _ in r]
        return [self.sample[r]]
        
    def resample(self):
        """
        Return a array of arraies with the all bootstrap sample
        """
        AllBootstrap = [ self.__resample() for i in range(self.B)]
        self.AllBootstrap = AllBootstrap
        return AllBootstrap
        
    def parameter(self, p):
        """
        p is a initial parameter aproximation
        """
        if(self.func):
            self.p = self.optimizer(p, self.sample, self.func)        
        return self.p
            
    def __bootstrapparameters(self):
        n_process=mpg.cpu_count()
        if(self.B <= n_process):
            B = n_process
        else:
            if(self.B%n_process != 0):
                B = self.B-self.B%n_process
                rB = self.B%n_process        
            else:
                B = self.B
                
        NS = len(self.p)
        NT = NS*B
        allParameters =  mpg.Array('d',[0.0 for i in range(NT)])
        
        def calcula(k,E,n):
            
            for i in range(0, E): 
                ni = (k)*NS
                nf = (k+1)*NS
                allParameters[ni:nf] = self.optimizer(self.p, self.AllBootstrap[k][0], self.func)
                k+=1

        MyParallel = parallelization(calcula,B)
        MyParallel.myPool()
        allParameters = [allParameters[i*NS:(i+1)*NS] for i in range(B)]
        if(self.B <= n_process):
            rB = B-self.B
            self.allParameters = numpy.array(allParameters[:B-rB])
        else:
            if(self.B%n_process != 0):
                B = self.B-self.B%n_process
                rB = self.B%n_process   
                lestP = len(allParameters)
                for i in range(rB):
                     allParameters.append(self.optimizer(self.p, self.AllBootstrap[lestP][0], self.func))
                self.allParameters = numpy.array(allParameters)
            else:
                self.allParameters = numpy.array(allParameters)
                
                
                
    def bootstrapparameters(self):
        """
        Given a function to be adjusted in the sample, calculate 
        the parameters of this function from the bootstrap sample
        """
        if(self.func != None):            
            if(self.AllBootstrap != None):
                if(self.p != None):
                    self.__bootstrapparameters()     
                    return self.allParameters
                else:
                    print 'Run parameter method with initial parameters'   
                    return None
                    
            else:
                self.resample()
                if(self.p != None):
                    self.__bootstrapparameters()     
                    return self.allParameters
                else:
                    print 'Run parameter method with initial parameters'
                    return None
                    
    def __bias(self):
        npar = self.allParameters[0].size
        bs = []
        for i in range(npar):
            BS = self.allParameters[:, i].mean()-self.p[i]
            bs.append(BS)
        self.Bias = bs
            
    def bias(self):
        """
        Return a bias from parameters of a function to be adjusted from the sample.
        """
        if(self.allParameters != None):
            self.__bias()
            return self.Bias 
        else:
            ptest = self.bootstrapparameters()
            if(ptest != None):
                self.__bias()
                return self.Bias
            else:
                return None
                
            
    def __std(self):
        npar = self.allParameters[0].size
        st = []
        for i in range(npar):
            ST = self.allParameters[:, i].std()
            st.append(ST)
        self.Std = st
        
    def sdt(self):
        """
        Return the standard deviation from parameters of a function to be adjusted from the sample.
        """
        if(self.allParameters != None):
            self.__std()
            return self.Std 
        else:
            ptest = self.bootstrapparameters()
            if(ptest != None):
                self.__std()
                return self.Std
            else:
                return None
                
    def __confidence(self, percentil):
        
        qup = (self.B+1.0)*(1.0-percentil/2.0)
        qup = int(qup)-1
        qlow = (self.B+1.0)*(percentil/2.0)
        qlow = int(qlow)-1
        npar = self.allParameters[0].size
        ci = []
        for i in range(npar):
            CI = self.allParameters[:, i]
            CI = numpy.sort(CI)
            ci.append([CI[qlow], CI[qup]])
        self.Cinterval = ci
        
    
    def confidence(self, percentil):
        """
        Return a percentil bootstrap confidence levele from parameters of a function to be adjusted from the sample.
        """
        if(self.allParameters != None):
            self.__confidence(percentil)
            return self.Cinterval 
        else:
            ptest = self.bootstrapparameters()
            if(ptest != None):
                self.__confidence(percentil)
                return self.Cinterval
            else:
                return None

        
    def optimizer(self, p0, sample, func):
        """
    Given a parametric function in lambda format and a start parameters, return the 
    best fit parameter from a data
    Arguments:
        p0 - list with parameters
        sample: a bidimensional array been the collunm 0 the  x values and 1 the y values of the sample
        func - function: 
                ex : 
                    func = lambda p,x: p[0]*x+p[1]
                The last argument must be x
        """
        DOF = sample.shape[0]-len(p0)
        
        def residual(p,sample):
            y = sample[:, 1]
            x = sample[:, 0]
            p1 = [p]
            Y = []            
            sigma = sample.std()
            if(sigma == 0):
                sigma = DOF
            tmp = p1
            tmp.append(0)
            for xi in x:                
                tmp[-1] = xi
                Y.append(func(*tmp))
                
            Y = numpy.array(Y)
            return (y-Y)/sigma
            
        plsq=sopt.leastsq(residual,p0,args=(sample))
        return plsq[0]


