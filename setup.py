#!/usr/bin/env python

# Stdlib imports
import os
import sys
from setuptools import setup

# Internal imports

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='mvm',
      version='0.3.0',
      author="Mike 'Fuzzy' Partin",
      author_email='fuzzy@fumanchu.org',
      description=('MVM is a tool for managing multiple versions of....anything.',
                   'Think rvm+virtualenv+luaenv+goenv+allTheOtherEnvs and then go even further.',
                   'Manage multiple versions of vim, or hexdump, wget if you want too.'),
      license='BSD',
      keywords='setuptools deployment installation distutils',
      url='',
      long_description=read('README.md'),
      classifiers=["Development Status :: 3 - Alpha",
                   "Topic :: Utilities",
                   "License :: OSI Approved :: BSD License"])
