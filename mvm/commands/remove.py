# Author: Mike 'Fuzzy' Partin
# Copyright: (c) 2016-2018
# Email: fuzzy@fumanchu.org
# License: See LICENSE.md for details

# Stdlib imports
import os
import sys

# Internal imports
from mvm.term    import *
from mvm.package import *

class MvmCmdRemove(object):

    def RemovePackage(self, arg=None, session=True):
        if session:
            cdir = self.config.dirs.sessionroot+'/'+self.SessionID
        else:
            cdir = self.config.dirs.globalroot

        pkg      = arg.split('-')[0]
        vers     = '-'.join(arg.split('-')[1:])
        target   = self.config.dirs.instroot
        obj      = False

        for i in os.listdir(target):
            if i.lower() == pkg.lower():
                target += '/'+pkg
                if os.path.isdir(target+'/'+self.sysInfo.os.name.lower()):
                    target += '/'+self.sysInfo.os.name.lower()
                    if os.path.isdir(target+'/'+self.sysInfo.os.arch):
                        target += '/'+self.sysInfo.os.arch
                        if os.path.isdir(target+'/'+vers):
                            target += '/'+vers
                            obj     = Package(self.config, target)

        if not obj:
            fatal('The package you specified is not installed.')
            sys.exit(1)
        else:
            obj.Delete()
