# Author: Mike 'Fuzzy' Partin
# Copyright: (c) 2016-2018
# Email: fuzzy@fumanchu.org
# License: See LICENSE.md for details

# Stdlib imports
import os

# Internal imports
from mvm.config  import *
from mvm.pkgspec import *

###############################################################################
class MvmCmdInstall(object):

    def InstallPackage(self, force=False, clean=False, verbose=False, arg=False):
        if arg:
            pkg   = arg.split('-')[0]
            ver   = '-'.join(arg.split('-')[1:])
            specs = Elist()
            if os.path.isfile('%s/%s/%s.json' % (self.config.dirs.pkgspecs, pkg, ver)):
                specs.append(PackageSpec(pSpec='%s/%s/%s.json' % (self.config.dirs.pkgspecs, pkg, ver),
                                         config=self.config))
                # Now let's plow through our depends list, and build our whole install list
                if len(specs[0].Depends()) > 0:
                    for dep in specs[0].Depends():
                        specs.append(PackageSpec(pSpec='%s.json' % dep, config=self.config))
                        for dep in specs.last().Depends():

                spec.Build(force=force, clean=clean, verbose=verbose)
        else:
            raise(ValueError, 'Specfile does not exist in %s' % self.config.dirs.pkgspecs)
