
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
                    debug('Enabling %s in your session.' % pkg)
                    pkg.Enable()
                else:
                    debug('Enabling %s globally.' % pkg)
                    pkg.Enable(session=False)

    def DisablePackage(self, arg=None, session=True):
        self.ListPackages(output=False)
        for pkg in self.instPkgs:
            if pkg.__str__() == arg:
                if pkg.IsGlobal() or pkg.IsSession():
                    if session:
                        debug('Disabling %s in your session' % pkg)
                        pkg.Disable()
                    else:
                        debug('Disabling %s globally.' % pkg)
                        pkg.Disable(session=False)
