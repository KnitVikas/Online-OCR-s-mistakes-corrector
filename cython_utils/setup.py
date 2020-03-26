from distutils.core import setup
from Cython.Build import cythonize
import numpy
import main
setup(ext_modules = cythonize('main.pyx'))
