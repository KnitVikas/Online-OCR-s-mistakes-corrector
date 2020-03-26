from distutils.core import setup
from Cython.Build import cythonize
import numpy
import experiments
setup(ext_modules = cythonize('experiments.pyx'))
