#!/usr/bin/env python
__title__ = "FisherMatrix"
__author__ = "Eduardo S. Pereira"
__email__ = "pereira.somoza@gmail.com"
__data__ = "15/04/2013"
__versio__ = "0.1"


"""
Fisher Matrix


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


import numpy

class fisher:
    """
    Atributs:
        p: list of best fit parameters of chi square
        dp: list with delta of parameters to be used in the derivation of the log of likelihoold functio.
        likefunc : Likelikood function
        xy : 2d array with x and y data
    """
    
    def __init__(self, p=None, dp=None, likefunc= None, xy=None ):       
        
        self.likefunc = likefunc
        self.p = p
        self.dp = dp
        self.xy=xy
        
    def __call__(self):
        return self.fisherMatrix()
        
    def chi2(self, p):
        """
        Chi square as likelehoold function estimator
        Parameter:
            p, list of best fit parameters
        """
        if(self.likefunc != None):
            Y = numpy.array([self.likefunc(p,self.xy[i, 0]) for i in range(self.xy.shape[0])])
            if(self.xy[:, 1].std() > 0.0):
                sigma  = self.xy[:, 1].std() 
                return sum((self.xy[:, 1]-Y)**2.0)/(2.0*sigma**2.0)
            else:
                DOF = Y.size-len(p)
                return sum((self.xy[:, 1]-Y)**2.0)/(2.0*DOF)
            
    def d2logfdpi2(self, p, dp):
        """
        Return de second numerical derivative of the log of the chi square likelihold estimatior in the best fit point of parameters
        Parameters:
            p: list of parameters, been that the parameter where will be derived must be added Delta p
            dp : 2d list of Delta parameter and position of dp in p
        """

            
        if(self.likefunc != None):
            if(dp[0][1] != dp[1][1]):
                p0 = [pi for pi  in p]
                p1 = [pi for pi in p]
                p2 = [pi for pi in p]
                p3 = [pi for pi in p]
                p0[dp[0][1]] = p0[dp[0][1]]+dp[0][0]
                p0[dp[1][1]] = p0[dp[1][1]]+dp[1][0]
                
                p1[dp[0][1]] = p1[dp[0][1]]-dp[0][0]
                p1[dp[1][1]] = p1[dp[1][1]]-dp[1][0]
                
                p2[dp[0][1]] = p2[dp[0][1]]-dp[0][0]
                p2[dp[1][1]] = p2[dp[1][1]]+dp[1][0]
                
                p3[dp[0][1]] = p3[dp[0][1]]+dp[0][0]
                p3[dp[1][1]] = p3[dp[1][1]]-dp[1][0]
                
                dif = numpy.log(self.chi2(p0))+\
                                           numpy.log(self.chi2(p1))-\
                                           numpy.log(self.chi2(p2))-\
                                           numpy.log(self.chi2(p3))
                diff = dif/(4.0*dp[1][0]*dp[0][0])
                return diff
                
            else:
                p0 = [pi for pi in p]
                p1 = [pi for pi  in p]
                
                p0[dp[0][1]] = p0[dp[0][1]]+dp[0][0]
                
                p1[dp[0][1]] = p1[dp[0][1]]-dp[0][0]
                    
                dif = numpy.log(self.chi2(p0))-\
                                           2*numpy.log(self.chi2(p))+\
                                           numpy.log(self.chi2(p1))
                diff = dif/(4.0*dp[0][0]**2.0)
                return diff
     
           
    def fisherMatrix(self):
        N = len(self.p)
        MFisher = numpy.zeros((N,N))
        for i in range(N):
            for j in range(N):
                diff = self.d2logfdpi2(self.p, [[self.dp[i], i], [self.dp[j], j]])
                MFisher[i, j] = diff

        MFisher = numpy.matrix(MFisher)
        NMFisher = -MFisher

        return MFisher, NMFisher.I
    
