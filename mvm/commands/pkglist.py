
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
                print('%s%s %s%s%s\n' % (cyan('I'),
                                       white('nstalled'),
                                       cyan('P'),
                                       white('ackages'),
                                       cyan(':')))
            pkgs = os.listdir(self.config.dirs['instroot'])
            pkgs.sort()
            longest = 0
            for pkg in pkgs:
                if len(pkg) > longest:
                    longest = len(pkg)
            longest  = longest+3
            for pkg in pkgs:
                oput = '%s%s%s(' % (cyan(pkg[0].upper()),
                                    white(pkg[1:]),
                                    ' '*(longest - len(pkg)))
                pkgPath = '%s/%s/%s/%s' % (self.config.dirs['instroot'],
                                           pkg,
                                           self.sysInfo['os']['name'].lower(),
                                           self.sysInfo['os']['arch'])
                if os.path.isdir(pkgPath):
                    versions = os.listdir(pkgPath)
                    versions.sort()
                    for vers in versions:
                        self.instPkgs.append(Package(self.config, pkgPath+'/'+vers))
                        oput += self.instPkgs[-1:][0].Display()
                        if pkg != pkgs[-1:][0]: oput += ', '
                if output:
                    if oput[-2:] == ', ':
                        print(oput[:-2]+')')
                    else:
                        print(oput+')')
            if output:
                print('\n %s = Session, %s = Global' % (cyan('*'), green('*')))
        else:
            if output:
                print('%s%s %s%s%s\n' % (cyan('A'),
                                       white('vailable'),
                                       cyan('P'),
                                       white('ackages'),
                                       cyan(':')))
            pkgs = os.listdir(self.config.dirs.pkgspecs)
            pkgs.sort()
            longest = 0
            for pkg in pkgs:
                if len(pkg) > longest:
                    longest = len(pkg)
            for pkg in pkgs:
                pdir = self.config.dirs.pkgspecs+'/'+pkg
                if pkg[0] != '.' and os.path.isdir(pdir):
                    vers = []
                    for v in os.listdir(pdir):
                        if os.path.isfile(pdir+'/'+v) and v[-5:] == '.json':
                            vers.append(v)
                    oput = '%s%s%s(' % (cyan(pkg[0].upper()),
                                        white(pkg[1:]),
                                        ' '*(longest - len(pkg)))
                    vers.sort()
                    for v in vers:
                        oput += blue(v.split('.jso')[0])
                        if v != vers[-1:][0]:
                            oput += ', '
                    if output: print(oput+')')
