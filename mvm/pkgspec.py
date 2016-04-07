# Author: Mike 'Fuzzy' Partin
# Copyright: (c) 2016-2018
# Email: fuzzy@fumanchu.org
# License: See LICENSE.md for details

# Stdlib imports
import os
import re
import sys
import json
import time
import subprocess
import multiprocessing

try:
    from urllib2 import urlopen
    str_types = (str, unicode)
except ImportError:
    from urllib.request import urlopen
    str_types = (str,)

# Internal imports
from mvm.term import *

class PackageSpec(object):

    osname       = os.uname()[0]
    arch         = os.uname()[-1:][0]
    cores        = multiprocessing.cpu_count()
    prefix_b     = '/.mvm/packages/instroot/%package%/%osnamel%/%arch%/%version%'
    keywords     = {'required': ('packager',  'email',   'homepage',
                                 'package',   'version', 'source',
                                 'license'),
                    'optional': ('patches',),
                    'methods':  ('configure', 'compile', 'install')}

    def __init__(self, pkgSpec=False):
        if not pkgSpec or not os.path.isfile(pkgSpec):
            raise(ValueError, 'Absent package spec.')
        self.defaults       = {'configure': {'cmd':    './configure',
                                             'args':   ['--prefix=%s%s' % (os.getenv('HOME'),
                                                                           self.prefix_b),],
                                             'env':    [],
                                             "enable": True},
                               'compile':   {'cmd':    'make',
                                             'args':   ['-j%d' % self.cores,],
                                             'env':    [],
                                             "enable": True},
                               'install':   {'cmd':    'make',
                                             'args':   ['install',],
                                             'env':    [],
                                             "enable": True},
                               'osname':    self.osname,
                               'osnamel':   self.osname.lower(),
                               'arch':      self.arch}
        try:
            data            = json.loads(open(pkgSpec).read())
        except Exception:
            fatal('%s is not valid json.' % pkgSpec)
            raise
        data['prefix']      = os.getenv('HOME')+'/'+self.prefix_b
        self.data           = self._lint(data)
        self.data           = self._expandMacros(self.data)
        tdata               = self.data['prefix'].lower()
        self.data['prefix'] = tdata
        debug(tdata)

    def _lint(self, data=False):
        if not data:
            raise(ValueError, 'No data structure supplied to PackageSpec._lint().')
        for kwt in self.keywords.keys():
            for kw in self.keywords[kwt]:
                if kw not in data.keys() and kwt == 'required':
                    fatal('required keyword %s is not in the pkgSpec.' % kw)
                    sys.exit(1)
        for dflt in self.defaults.keys():
            if dflt in data.keys():
                for attr in self.defaults[dflt].keys():
                    if attr not in data[dflt].keys():
                        data[dflt][attr] = self.defaults[dflt][attr]
            else:
                data[dflt] = self.defaults[dflt]
        return data # self._expandMacros(data)

    def _expandMacros(self, data=False):
        if not data:
            raise(ValueError, 'No data structure supplied to PackageSpec._expandMacros()')
        for itm in data.keys():
            if isinstance(data[itm], dict):
                tdata = self._expandMacros(data[itm])
                data[itm] = tdata
            elif isinstance(data[itm], (list, tuple)):
                for initm in range(0, len(data[itm])):
                    if isinstance(data[itm][initm], str_types):
                        tmps = data[itm][initm]
                        tmpk = ''
                        for macro in re.findall(r'%[a-zA-Z0-9_]*%', data[itm][initm]):
                            tmpk = re.sub('%', '', macro)
                            tmps = re.sub(macro, self.data[tmpk], data[itm][initm])
                            data[itm][initm] = tmps
            elif isinstance(data[itm], str_types):
                tmps = data[itm]
                tmpk = ''
                for macro in re.findall(r'%[a-zA-Z0-9_]*%', data[itm]):
                    tmpk = re.sub('%', '', macro)
                    tmps = re.sub(macro, self.data[tmpk], tmps)
                data[itm] = tmps
        return data

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

    def _extract(self, fname):
        distfiles = '%s/.mvm/packages/distfiles' % os.getenv('HOME')
        tempdir   = '%s/.mvm/packages/temp'      % os.getenv('HOME')
        print('%s%s Extracting %s' % (cyan('>'), white('>'), fname))
        os.system('bsdtar xpf %s/%s -C %s' % (distfiles, fname, tempdir))

    def _cmd(self, dname, data):
        cdir = os.getcwd()
        env  = []

        os.chdir(dname)
        for e in data['env']:
            env.append('='.join(e))

        cmd  = 'env %s %s %s' % (' '.join(env), data['cmd'], ' '.join(data['args']))
        proc = subprocess.Popen(cmd,
                                shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                close_fds=True)
        logfile = '%s/.mvm/packages/temp/%s-%s.log' % (os.getenv('HOME'),
                                                       self.data['package'].lower(),
                                                       self.data['version'])
        open(logfile, 'ab').write(proc.stdout.read())
        #os.system('env %s %s %s' % (' '.join(env), data['cmd'], ' '.join(data['args'])))
        os.chdir(cdir)

    def _configure(self):
        if self.data['configure']['enable']:
            print("%s%s Configuring." % (cyan('>'), white('>')))
            dname = '%s/.mvm/packages/temp/%s-%s' % (os.getenv('HOME'),
                                                     self.data['package'],
                                                     self.data['version'])
            self._cmd(dname, self.data['configure'])

    def _compile(self):
        if self.data['compile']['enable']:
            print('%s%s Compiling.' % (cyan('>'), white('>')))
            dname = '%s/.mvm/packages/temp/%s-%s' % (os.getenv('HOME'),
                                                     self.data['package'],
                                                     self.data['version'])
            self._cmd(dname, self.data['compile'])

    def _install(self):
        if self.data['install']['enable']:
            print('%s%s Installing.' % (cyan('>'), white('>')))
            dname = '%s/.mvm/packages/temp/%s-%s' % (os.getenv('HOME'),
                                                     self.data['package'],
                                                     self.data['version'])
            self._cmd(dname, self.data['install'])

    def Build(self, force=False, clean=False, verbose=False):
        self._fetch(self.data['source'])
        self._extract(os.path.basename(self.data['source']))
        self._configure()
        self._compile()
        self._install()
