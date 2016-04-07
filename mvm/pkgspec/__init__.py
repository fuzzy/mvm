# Author: Mike 'Fuzzy' Partin
# Copyright: (c) 2016-2018
# Email: fuzzy@fumanchu.org
# License: See LICENSE.md for details

# Stdlib imports
import os
import multiprocessing

# Internal imports
from mvm.pkgspec.fetch   import *
from mvm.pkgspec.extract import *

class PkgSpec(PkgSpecFetch, PkgSpecXtract):

    osname  = os.uname()[0]
    arch    = os.uname()[-1:][0]
    cores   = multiprocessing.cpu_count()
    dirs    = None

    def __init__(self, pkgspec=False, dirs=False):
        if not pkgspec or not dirs or not os.path.isfile(pkgspec):
            raise(ValueError, 'Absent package spec.')
        self.pspecFP = open(pkgspec)
        self.dirs    = dirs

