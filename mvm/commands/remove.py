
# Stdlib imports

# Internal imports
from mvm.term import *

class MvmCmdRemove(object):

    def RemovePackage(self, arg=None, session=True):
        debug('arg=%r session=%r' % (arg, session))
        if session:
            cdir = self.config.dirs.sessionroot+'/'+self.SessionID
        else:
            cdir = self.config.dirs.globalroot

