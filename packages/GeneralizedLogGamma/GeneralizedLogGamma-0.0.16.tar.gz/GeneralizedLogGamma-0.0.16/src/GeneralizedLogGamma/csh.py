"""
Cumulative distribution, survival, hazard functions of a generalized gamma and log-gamma distribution.
"""

# Author: Carlos Alberto Cardozo Delgado <cardozopypackages@gmail.com>

import math
import numpy as np
from scipy.special import gammainc

def cdf(x, location = 0, scale = 1, shape = 1):
    x = np.array(x)
    y = (x - location)/scale
    sh_2 = shape**2
    out = gammainc( 1/sh_2, (1/sh_2)*np.exp(shape*y))
    if shape < 0:
        out = 1 - out
    return out

def pdf(x, location = 0, scale = 1, shape = 1):
    x = np.array(x)
    if abs(shape) < 0.1:
        if shape > 0: 
            shape = 0.1
        else:
            shape = -0.1
    inv_shape = 1/shape        
    inv_shape_2 = inv_shape**2
    cl_shape = (np.abs(shape)/math.gamma(inv_shape_2))*(inv_shape_2)

    y = (x - location)/scale
    output = (inv_shape)*y - (inv_shape_2)*np.exp(shape*y)
    output = np.exp(output)
    output = cl_shape*output/scale
    return output

def surv(x, location = 0, scale = 1, shape = 1):
    x = np.array(x)
    if np.min(x > 0) == False:
       print('x must be a list of positive numbers.')
       return None   
    out = 1 - cdf(x, location, scale, shape)
    return out


def hazard(x, location = 0, scale = 1, shape = 1):
    x = np.array(x)
    if np.min(x > 0) == False:
       print('x must be a list of positive numbers.')
       return None   
    out = pdf(x, location, scale, shape)/(x*surv(x, location, scale, shape))
    return out

#print('--------------------------------------------------------')
#print(hazard(x = [15, 3, 2, 1, 0.0000001], shape = -1))
#print(hazard(x = [0.001, 1, 1.81], scale = 0.5, shape = 1))
#print(hazard(x = -1))
#print('--------------------------------------------------------')
#print(cdf(x = [-1.24589932, -0.36651292, 0.32663426], shape = 1))
#print(cdf(x = [-0.3266343, 0.3665129, 1.2458993], shape = 1))
#print('--------------------------------------------------------')
#print(surv(x = [15, 3, 2, 1, 0.0000001], shape = -1))
#print(surv(x = [0.000000001, 1, 2], scale = 0.5, shape = 1 ))
#print(surv(x = -1))