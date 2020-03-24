# cython: language_level=3

#import numpy as np
#cimport numpy as np
import math
from math import sqrt

def mean_var_sigma(a):
    cdef int N = len(a)
    cdef float mean = sum(a)/N
    cdef float var = sum(map(lambda x:(x-mean)**2, a))/N
    cdef float sig = sqrt(var)
    return mean, var, sig
    
cpdef float mean(list numbers):
    return float(sum(numbers)) / max(len(numbers), 1)