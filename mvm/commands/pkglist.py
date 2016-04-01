
# Stdlib imports
import os
import json

# Internal imports
from mvm.term    import *
from mvm.package import *

class MvmCmdList(object):

    def ListPackages(self, installed=True, output=True):
        # TODO: list available packages
        self.instPkgs = []
        if installed:
            if output:
                print('%s%s %s%s%s' % (cyan('I'),
                                       white('nstalled'),
                                       cyan('P'),
                                       white('ackages'),
                                       cyan(':')))
            pkgs = os.listdir(self.config.dirs['instroot'])
            pkgs.sort()
            for pkg in pkgs:
                pkgPath = '%s/%s/%s/%s' % (self.config.dirs['instroot'],
                                           pkg,
                                           self.sysInfo['os']['name'].lower(),
                                           self.sysInfo['os']['arch'])
                if os.path.isdir(pkgPath):
                    for vers in os.listdir(pkgPath):
                        self.instPkgs.append(Package(self.config, pkgPath+'/'+vers))
                        if output: self.instPkgs[-1:][0].Display()
        else:
            if output:
                print('%s%s %s%s%s' % (cyan('A'),
                                       white('vailable'),
                                       cyan('P'),
                                       white('ackages'),
                                       cyan(':')))
            pkgs = os.listdir(self.config.dirs.pkgspecs)
            pkgs.sort()
            for pkg in pkgs:
                print(pkg.split('.jso')[0])
