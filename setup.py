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
      classifiers=["Development Status :: 2 - Pre-Alpha",
                   "Topic :: Utilities",
                   "Topic :: System :: Systems Administration",
                   "Topic :: System :: Software Distribution",
                   "Topic :: System :: Operating System",
                   "Topic :: System :: Installation/Setup",
                   "License :: OSI Approved :: BSD License",
                   "Environment :: Console",
                   "Intended Audience :: System Administrators",
                   "Intended Audience :: Developers",
                   "Intended Audience :: Ender Users/Desktop",
                   "Operating System :: POSIX",])
