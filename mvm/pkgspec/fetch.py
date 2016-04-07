# Author: Mike 'Fuzzy' Partin
# Copyright: (c) 2016-2018
# Email: fuzzy@fumanchu.org
# License: See LICENSE.md for details

# Stdlib imports
try: # Python2
    from urllib2 import urlopen
    str_types = (str, unicode)
except ImportError: # Python3
    from urllib.request import urlopen
    str_types = (str,)

class PkgSpecFetch(object):

    def _fetch(self, uri):
        output    = '%s/.mvm/packages/distfiles/%s' % (os.getenv('HOME'),
                                                       os.path.basename(uri))
        print('%s%s %s' % (cyan('>'), white('>'), uri))
        inFP      = urlopen(uri)
        outFP     = open(output, 'wb+') # .write(urlopen(uri).read())
        buffsize  = 40960
        buff      = inFP.read(buffsize)
        outsz     = 0
        st        = time.time()
        while buff:
            outFP.write(buff)
            outFP.flush()
            buff  = inFP.read(buffsize)
            outsz += len(buff)
            tlen  = int(time.time() - st)
            if tlen == 0: tlen = 1
            sys.stdout.write('%s%s %s in %s @ %s/sec%s\r' % (cyan('>'),
                                                             white('>'),
                                                             humanSize(outsz),
                                                             humanTime(tlen),
                                                             humanSize(outsz / tlen),
                                                             ' '*10))
            sys.stdout.flush()
        print('')
