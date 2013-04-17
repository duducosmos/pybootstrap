#!/usr/bin/env python
__title__ = "example"
__author__ = "Eduardo S. Pereira"
__email__ = "pereira.somoza@gmail.com"
__data__ = "15/04/2013"
__versio__ = "0.1"



"""
example


This file is part of PyBootstrap.
    copyright : Eduardo dos Santos Pereira
    15 april 2013

    PyBootstrap is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License.
    PyBootstraps is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Foobar.  If not, see <http://www.gnu.org/licenses/>.
"""


from pybootstrap import *

import time
import numpy
import matplotlib.pyplot as plt
f2=eval('lambda p, x:p[0]*x**p[1]')
def func(p, x):
    return  f2(p, x)
myData = numpy.array([[1., 0.9], [1.45, 2.27], [2.05, 4.3], [2.7, 6.5], [3.1, 9.83], [3.9, 15.5], [5.05, 24.3], [5.9, 35.8], [7.3, 49.8]])
myBootstrap = pybootstrap.bootstrap(myData, 10000, func =func)    

bootstrap = myBootstrap.resample()    


myBootstrap.parameter([1., 2.])

t1 = time.time()

parameters = myBootstrap.bootstrapparameters()

t2=time.time()
parameters = myBootstrap.bootstrapparameters()
t3=time.time()
print'times',  t2-t1, t3-t2
print 'bias ', myBootstrap.bias()
print 'Error ', myBootstrap.sdt()
confidence= myBootstrap.confidence(0.25)
plt.plot(myData[:, 0], myData[:, 1], '.')
pybootstrap.plotHistoFreq(parameters[:, 0], bin=200, percentil=95, low=confidence[0][0], up=confidence[0][1], xalbel=r'a')

from pybootstrap.fishermatrix import *
t1 = time.time()
bp =  pybootstrap.optimizer([1., 2.], myData, func)
t2 = time.time()
bp1 =  pybootstrap.optimizer([1., 2.], myData, func)
t3 = time.time()
print 'time', t2-t1, t3-t2
print'Best Fit Parameters: ',  bp1
obj = fisher(p=bp, dp=[0.01, 0.01, 0.01],  likefunc=func, xy=myData)
MM = obj()
print'Fisher Matrix:\n',  MM[0]
print'\nCovaricance Matrix:\n',  MM[1]
