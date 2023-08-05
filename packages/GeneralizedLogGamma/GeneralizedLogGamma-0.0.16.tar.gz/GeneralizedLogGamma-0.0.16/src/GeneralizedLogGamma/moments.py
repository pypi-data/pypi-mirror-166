"""
Mean, median, mode, variance, coeficient of variation, skewness, kurtosis, probability density function, 
quantile function, and random generating function of the K-th order statistics from a Generalized log-gamma distribution.
"""

# Author: Carlos Alberto Cardozo Delgado <cardozopypackages@gmail.com>

import math
import numpy as np
import scipy.special as ssp
import scipy.stats as stats

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

#print(pdf(x = [0,1,2]))

def ppf(x = 0.5, location = 0, scale = 1, shape = -1):
    x = np.array(x)
    s_two = shape**2
    n = x.size
    new_x = np.zeros(n)
    if (shape < 0):
        x = 1 - x     
    for i in range(0,n):
        new_x[i] = (1/shape)*np.log((0.5*s_two)*stats.chi2.ppf(x[i], df = 2/s_two))
    new_x = location + scale * new_x
    return new_x

#print(ppf(x= [0.25,0.5,0.75]))

def rvs(size, location = 0, scale = 1, shape = 1, k = 1, n = 1, alpha = 0.05):
  '''
  Parameters
  ----------
  size int, represents the size of the sample.
  location float, represents the location parameter. Default value is 0.
  scale float, represents the scale parameter. Default value is 1.
  shape float, represents the shape parameter. Default value is 1.
  k int, represents the K-th smallest value from a sample.
  n int, represents the size of the sample to compute the order statistic from.
  alpha float, (1 - alpha) represents the confidence of an interval for the population median of the distribution of the k-th order statistic. Default value is 0.05.
  
  Returns
  -------
  A list with an one numpy array random sample of order statistics from a generalized log-gamma distribution and the join probability density function evaluated in the random sample.
  '''

  initial = stats.beta.rvs(size = size, a = k, b = n + 1 - k)
  sample  = ppf(initial, location, scale, shape)
  values_pdf     = math.factorial(size) * np.cumprod(pdf(x = sample, location= location, scale = scale, shape = shape))[size - 1]
  if (size > 5):
    return [sample, values_pdf]
  print("---------------------------------------------------------------------------------------------\n")
  print("We cannot report the confidence interval. The size of the sample is less or equal than five.\n")
  return [sample, values_pdf]

#print(rvs(size = 10, shape = -1))

def lss(location = 0, scale = 1, shape = 1):
  '''
  Parameters
  ----------
  location float, represents the location parameter. Default value is 0.
  scale float, represents the scale parameter. Default value is 1.
  shape float, represents the shape parameter. Default value is 1.
 
  Returns
  -------
  A dictionary object with the mean, median, mode, variance, cv, skewness, kurtosis.
  '''
  shape_two = shape**2
  inv_shape_two = 1/shape_two
  mean = location + scale*((ssp.polygamma(0, inv_shape_two) - np.log(inv_shape_two))/shape)
  median = ppf(x = [0.5] , location = location, scale = scale, shape = shape)
  variance = (scale**2) * (inv_shape_two) * ssp.polygamma(1, inv_shape_two)
  if(abs(shape) < 0.09):
    cv = "It is not defined because the mean of this distribution is too close to zero!"
  else:
    cv = np.square(variance)/mean
    skewness = np.sign(shape) * ssp.polygamma(2, inv_shape_two)/ssp.polygamma(1, inv_shape_two)**1.5
    kurtosis = (ssp.polygamma(3, inv_shape_two)/(ssp.polygamma(1, inv_shape_two)**2)) + 3
    return { 'mean' : mean, 
             'median' : median, 
             'mode' : location, 
             'variance' : variance, 
             'cv' : cv, 
             'skewness' : skewness, 
             'kurtosis' : kurtosis}
#print(lss())