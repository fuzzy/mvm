# Author: Mike 'Fuzzy' Partin
# Copyright: (c) 2016-2018
# Email: fuzzy@fumanchu.org
# License: See LICENSE.md for details

# Stdlib imports
import os

class PkgSpecExtract(object):

    def _extract(self, fname):
        distfiles = '%s/.mvm/packages/distfiles' % os.getenv('HOME')
        tempdir   = '%s/.mvm/packages/temp'      % os.getenv('HOME')
        print('%s%s Extracting %s' % (cyan('>'), white('>'), fname))
        os.system('bsdtar xpf %s/%s -C %s' % (distfiles, fname, tempdir))
