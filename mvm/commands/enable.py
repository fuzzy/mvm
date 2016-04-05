# Author: Mike 'Fuzzy' Partin
# Copyright: (c) 2016-2018
# Email: fuzzy@fumanchu.org
# License: See LICENSE.md for details

# Stdlib imports

# Internal imports
from mvm.term import *
from mvm.commands.pkglist import *

class MvmCmdEnable(object):

    def EnablePackage(self, arg=None, session=True):
        self.ListPackages(output=False)
        for pkg in self.instPkgs:
            if pkg.__str__() == arg:
                if session:
                    pkg.Enable()
                else:
                    pkg.Enable(session=False)

    def DisablePackage(self, arg=None, session=True):
        self.ListPackages(output=False)
        for pkg in self.instPkgs:
            if pkg.__str__() == arg:
                if pkg.IsGlobal() or pkg.IsSession():
                    if session:
                        pkg.Disable()
                    else:
                        pkg.Disable(session=False)
