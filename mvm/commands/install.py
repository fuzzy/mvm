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
        def NewPackage(pspec, cfg):
            retv = Elist([])
            retv.append(PackageSpec(pSpec=pspec, config=cfg))
            for d in retv.last()._data.depends:
                t = d.split('-')
                pkg = t.pop(0)
                ver = '-'.join(t)
                pspec = '%s/%s/%s.json' % (cfg.dirs.pkgspecs, pkg, ver)
                retv.extend(NewPackage(pspec, cfg))
            return retv

        if arg:
            pkg   = arg.split('-')[0]
            ver   = '-'.join(arg.split('-')[1:])
            specs = Elist()
            pspec = '%s/%s/%s.json' % (self.config.dirs.pkgspecs, pkg, ver)
            if os.path.isfile(pspec):
            #    specs.append(PackageSpec(pSpec='%s/%s/%s.json' % (self.config.dirs.pkgspecs, pkg, ver),
            #                             config=self.config))
                # Now let's plow through our depends list, and build our whole install list
                specs = NewPackage(pspec, self.config)

            # Now let's resolve dependancy ordering
            changes = True
            iters   = 0
            while changes:
                changes = False
                if iters >= 5000:
                    raise(Exception, 'Circular dependancy detected.')
                else:
                    iters += 1
                for a in range(0, len(specs)):
                    for b in range(0, len(specs)):
                        if specs[b].Requires(specs[a]):
                            if b <= a:
                                specs.insert(a, specs.pop(b))
                                changes = True
                                break
                    if changes:
                        break

            # And now let's install each successive package
            for spec in specs:
                spec.Build(force=force, clean=clean, verbose=verbose)
        else:
            raise(ValueError, 'Specfile does not exist in %s' % self.config.dirs.pkgspecs)
