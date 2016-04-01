# Stdlib imports
import os

# Internal imports
from mvm.pkgspec import *

###############################################################################
class MvmCmdInstall(object):

    def InstallPackage(self, force=False, clean=False, verbose=False, arg=False):
        if arg and os.path.isfile('%s/%s.json' % (self.config.dirs.pkgspecs,
                                                  arg)):
            spec = PackageSpec('%s/%s.json' % (self.config.dirs.pkgspecs,
                                               arg))
            spec.Build(force=force, clean=clean, verbose=verbose)
        else:
            raise(ValueError, 'Specfile does not exist in %s' % self.config.dirs.pkgspecs)
