# Author: Mike 'Fuzzy' Partin
# Copyright: (c) 2016-2018
# Email: fuzzy@fumanchu.org
# License: See LICENSE.md for details

# Stdlib imports
import os

# Internal imports
from mvm.pkgspec import *

###############################################################################
class MvmCmdInstall(object):

    def InstallPackage(self, force=False, clean=False, verbose=False, arg=False):
        if arg:
            pkg = arg.split('-')[0]
            ver = '-'.join(arg.split('-')[1:])
            if os.path.isfile('%s/%s/%s.json' % (self.config.dirs.pkgspecs, pkg, ver)):
                spec = PackageSpec(pSpec='%s/%s/%s.json' % (self.config.dirs.pkgspecs, pkg, ver),
                                   config=self.config)
                spec.Build(force=force, clean=clean, verbose=verbose)
        else:
            raise(ValueError, 'Specfile does not exist in %s' % self.config.dirs.pkgspecs)
