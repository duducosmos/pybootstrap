#!/usr/bin/env python
__title__ = "bootstrap"
__author__ = "Eduardo S. Pereira"
__email__ = "pereira.somoza@gmail.com"
__data__ = "04/04/2013"
__versio__ = "0.1"

"""
DISCLAIMER
    This module contain class and function of Bootstrap resample with replacement as described by
Wherens et al. 2000

    This software may be used, copied, or redistributed as long as it
    is not sold and this copyright notice is reproduced on each copy
    made. This routine is provided as is without any express or implied
    warranties whatsoever.
    

AUTHOR
    Eduardo S. Pereira
    email: pereira.somoza@gmail.com
    
REFERENCES:
    Wherens, R. et al., 2000. Chemometrics and Inteligent Laboratory System, 54, 35
    
"""


#import sys,os
#import shutil
#
#HOME = os.path.expanduser('~')

__all__ = ['bootstrap','optimizer', 'plotHistoFreq', 'parallelization']
