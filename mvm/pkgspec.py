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
from mvm.term   import *
from mvm.config import Edict

class PackageSpec(object):
    '''
    The PkgSpec() class deals with compiling and building packages based on a given data template
    known as a Spec File. This is a standard JSON file, which describes the process of compilation.
    The format of the file will (at some point) be documented in the project wiki.
    '''

    ##
    ## Class attributes

    _defaults          = Edict({'osname':    os.uname()[0].lower(),
                                'osvers':    os.uname()[2].lower(),
                                'osarch':    os.uname()[4].lower(),
                                'cores':     multiprocessing.cpu_count(),
                                'prefix':    'X',           'packager':  None,
                                'email':     None,          'homepage':  None,
                                'package':   None,          'version':   None,
                                'source':    None,          'license':   None,
                                'patches':   [],            'depends':   [],
                                'configure': {'cmd':  './configure',
                                               'args': ['--prefix=%prefix%',],
                                               'env':  []},
                                'compile':   {'cmd':  'make',
                                               'args': ['-j%cores%',],
                                               'env':  []},
                                'install':   {'cmd':  'make',
                                               'args': ['install',],
                                               'env': []}})

    ##
    ## Class Methods

    def __init__(self, pSpec=False, config=False):
        '''
        Instantiating:

        PkgSpec(pSpec='/path/to/specfile.json', config=ConfigObject)

        or

        PkgSpec(pSpec='specfile.json', config=ConfigObject)

        where the pkgspecs directory will be searched for the given file.
        '''
        if False in (pSpec, config):
            raise(ValueError, 'Must supply a package spec, and a config object.')
        # First let's record our config object
        self._cfg            = config
        # And then validate we have a real file
        if os.path.isfile(pSpec):
            self._spec       = pSpec
        elif os.path.isfile(self._cfg.dirs.pkgspecs+'/'+pSpec):
            self._spec       = self._cfg.dirs.pkgspecs+'/'+pSpec
        # Let's read in our JSON data
        try:
            self._data       = Edict(json.loads(open(self._spec).read()))
        except Exception:
            fatal("The file %s contains malformed JSON data." % self._spec)
            sys.exit(1)
        # Now let's update our defaults map
        self._defaults.prefix = '%s/%s/%s/%s/%s' % (self._cfg.dirs.instroot,
                                                    self._data.package.lower(),
                                                    self._defaults.osname,
                                                    self._defaults.osarch,
                                                    self._data.version.lower())
        self._lint()
        self.data             = self._macros(self._data.copy())
        
    def __str__(self):
        return str('pkgspec:%s-%s' % (self._data.package, self._data.version))

    def __repr__(self):
        print(str(self.__str__()))

    ##
    ## Private Methods

    def _lint(self):
        for k in self._defaults.keys():
            if k not in self._data.keys():
                if self._defaults[k] != None:
                    self._data[k] = self._defaults[k]
                else:
                    fatal("Required keyword %s is missing from %s." % (k, self._spec))
                    sys.exit(1)

    def _macros(self, data=False):
        if not data:
            raise(ValueError, 'No data structure supplied to PackageSpec._expandMacros()')
        for itm in data.keys():
            if isinstance(data[itm], dict):
                tdata = self._macros(data[itm])
                data[itm] = tdata
            elif isinstance(data[itm], (list, tuple)):
                for initm in range(0, len(data[itm])):
                    if isinstance(data[itm][initm], str_types):
                        tmps = data[itm][initm]
                        tmpk = ''
                        for macro in re.findall(r'%[a-zA-Z0-9_]*%', data[itm][initm]):
                            tmpk = re.sub('%', '', macro)
                            tmps = re.sub(macro, str(self._data[tmpk]), data[itm][initm])
                            data[itm][initm] = tmps
            elif isinstance(data[itm], str_types):
                tmps = data[itm]
                tmpk = ''
                for macro in re.findall(r'%[a-zA-Z0-9_]*%', data[itm]):
                    tmpk = re.sub('%', '', macro)
                    tmps = re.sub(macro, self._data[tmpk], tmps)
                data[itm] = tmps
        return data

    def _fetch(self, uri):
        output    = '%s/%s' % (self._cfg.dirs.dstfiles,
                               os.path.basename(uri))
        print('%s%s %s' % (cyan('>'), white('>'), uri))
        inFP      = urlopen(uri)
        outFP     = open(output, 'wb+')
        buffsize  = (1024 * 40)
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

    def _extract(self):
        print('%s%s Extracting %s' % (cyan('>'), white('>'),
                                      os.path.basename(self._data.source)))
        os.system('bsdtar xpf %s/%s -C %s' % (self._cfg.dirs.dstfiles,
                                              os.path.basename(self._data.source),
                                              self._cfg.dirs.pkgtemp))

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
        logfile = '%s/%s-%s.log' % (self._cfg.dirs.pkgtemp,
                                    self._data['package'].lower(),
                                    self._data['version'])
        open(logfile, 'ab').write(proc.stdout.read())
        #os.system('env %s %s %s' % (' '.join(env), data['cmd'], ' '.join(data['args'])))
        os.chdir(cdir)

    ##
    ## Public Methods

    def Configure(self):
        print(self._data.configure)
        sys.exit(0)
        if self._data.configure.enable:
            print("%s%s Configuring." % (cyan('>'), white('>')))
            dname = '%s/%s-%s' % (self._cfg.dirs.pkgtemp,
                                  self._data.package,
                                  self._data.version)
            self._cmd(dname, self._data.configure)


    def Compile(self):
        pass

    def Install(self):
        pass

    def Package(self):
        pass

    def Build(self, force=None, clean=None, verbose=None):
        self._fetch(self._data.source)
        self._extract()
        self.Configure()

class PackageSpecOld(object):

    def _extract(self, fname):
        distfiles = '%s/.mvm/packages/distfiles' % os.getenv('HOME')
        tempdir   = '%s/.mvm/packages/temp'      % os.getenv('HOME')
        print('%s%s Extracting %s' % (cyan('>'), white('>'), fname))
        os.system('bsdtar xpf %s/%s -C %s' % (distfiles, fname, tempdir))

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

    ##
    ## Public Methods

    def Build(self, force=False, clean=False, verbose=False):
        self._fetch(self.data['source'])
        self._extract(os.path.basename(self.data['source']))
        self._configure()
        self._compile()
        self._install()
