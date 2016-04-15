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
import hashlib
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

class PackageOp(object):
    def __init__(self):
        pass

class PackageSpec(object):
    '''
    The PkgSpec() class deals with compiling and building packages based
    on a given data template known as a Spec File. This is a standard JSON
    file, which describes the process of compilation. The format of the
    file will (at some point) be documented in the project wiki.
    '''

    ##
    ## Class attributes

    _defaults = Edict({
        'osname':    os.uname()[0].lower(),
        'osvers':    os.uname()[2].lower(),
        'osarch':    os.uname()[4].lower(),
        'cores':     multiprocessing.cpu_count(),
        'prefix':    'X',           'packager':  None,
        'email':     None,          'homepage':  None,
        'package':   None,          'version':   None,
        'source':    None,          'license':   None,
        'patches':   [],            'depends':   [],
        'sha256':    None,
        'configure': {'cmd':  './configure',
                      'args': ['--prefix=%prefix%',],
                      'env':  [], 'enable': True},
        'compile':   {'cmd':  'make',
                      'args': ['-j%cores%',],
                      'env':  [], 'enable': True},
        'install':   {'cmd':  'make',
                      'args': ['install',],
                      'env': [], 'enable': True}
    })

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
        self._cfg             = config
        # And then validate we have a real file
        if os.path.isfile(pSpec):
            self._spec        = pSpec
        elif os.path.isfile(self._cfg.dirs.pkgspecs+'/'+pSpec):
            self._spec        = self._cfg.dirs.pkgspecs+'/'+pSpec
        else:
            debug(pSpec)
        # Let's read in our JSON data
        try:
            self._data        = Edict(json.loads(open(self._spec).read()))
        except Exception:
            fatal("The file %s contains malformed JSON data." % self._spec)
            sys.exit(1)
        # Now let's update our defaults map
        self._defaults.prefix = '%s/%s/%s/%s/%s' % (self._cfg.dirs.instroot,
                                                    self._data.package.lower(),
                                                    self._defaults.osname,
                                                    self._defaults.osarch,
                                                    self._data.version.lower())
        data                  = Edict(self._lint(self._defaults, self._data))
        self._data            = data.copy()
        self._data            = Edict(self._macros(self._data.copy()).copy())

    def __str__(self):
        return str('%s-%s' % (self._data.package, self._data.version))

    def __repr__(self):
        return self.__str__()

    ##
    ## Private Methods

    def _lint(self, a, b):
        c = b.copy()
        for k in a.keys():
            if k not in c.keys():
                c[k] = a[k]
            elif isinstance(a[k], (list, tuple)):
                for i in a[k]:
                    if i not in c[k]:
                        c[k].append(i)
            elif isinstance(a[k], dict):
                c[k] = self._lint(a[k], c[k])
        return c

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

    def _validate(self, fname, sha256):
        lineOut('%s Checksumming' % block(str(self)))
        if os.path.isfile(fname):
            sha  = hashlib.sha256()
            fp   = open(fname, 'rb')
            buff = fp.read(1048576)
            while buff:
                sha.update(buff)
                buff = fp.read(1048576)
            if sha256 == sha.hexdigest():
                return True
            else:
                return False

    def _fetch(self, uri):
        output    = '%s/%s' % (self._cfg.dirs.dstfiles,
                               os.path.basename(uri))
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
            sys.stdout.write(
                '%s%s %s %s: %s in %s @ %s/sec%s\r' % (
                    cyan('>'),
                    white('>'),
                    block(str(self)),
                    os.path.basename(uri),
                    white(humanSize(outsz)),
                    white(humanTime(tlen)),
                    white(humanSize(outsz / tlen)),
                    ' '*10))
            sys.stdout.flush()
        print('')
        if self._data.sha256 != None:
            if not self._validate(output, self._data.sha256):
                raise(Exception, 'The downloaded file does not match the recorded sha256.')

    def _extract(self, xfile):
        lineOut('%s Extracting' % block(str(self)))
        odir = '%s/%s-%s' % (self._cfg.dirs.pkgtemp,
                             self._data.package,
                             self._data.version)
        if not os.path.isdir(odir):
            os.mkdir(odir)
        self._cmd(data={
            'cmd': 'bsdtar -xpf %s/%s --strip-components 1 -C %s/' % (self._cfg.dirs.dstfiles,
                                                               xfile,
                                                               odir),
            'env': [],
            'args': []})


    def _patch(self, pname=False):
        if not pname or not os.path.isfile('%s/%s' % (self._cfg.dirs.dstfiles, pname)):
            raise(ValueError, 'You must supply a valid patch file.')
        lineOut('%s Applying patch: %s' % (block(str(self)), white(pname)))
        sdir = '%s/%s-%s' % (self._cfg.dirs.pkgtemp,
                             self._data.package,
                             self._data.version)
        self._cmd(sdir, {
            'cmd': 'patch -p0 <%s/%s' % (self._cfg.dirs.dstfiles, pname),
            'env': [],
            'args': []})

    def _cmd(self, dname='/', data=False):
        cdir     = os.getcwd()
        env      = []
        if data:
            # Let's get into place
            os.chdir(dname)
            # And build our environment if any
            for e in data['env']:
                env.append('='.join(e))
            # Then put env, cmd and args together
            cmd      = 'env %s %s %s' % (' '.join(env), data['cmd'], ' '.join(data['args']))
            # And build our process object
            proc     = subprocess.Popen(
                cmd,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                close_fds=True
            )
            # This of course is necessary
            logfile  = '%s/%s-%s.log' % (
                self._cfg.dirs.pkgtemp,
                self._data['package'].lower(),
                self._data['version']
            )
            logfp    = open(logfile, 'ab')
            # Now let's get to work processing the output of the command
            buff     = proc.stdout.readline()
            while buff:
                logfp.write(buff)
                logfp.flush()
                buff = proc.stdout.readline()
            # Let's be good citizens and clean up
            proc.stdin.close()
            proc.stdout.close()
            # Now let's take into account our return value
            if proc.wait() != 0:
                raise(
                    Exception,
                    'The command (%s) failed to execute properly. See %s for more information.' % (
                        cmd,
                        logfile
                    ))
            # And finally let's go back home, and return
            os.chdir(cdir)
            return True
        else:
            return False

    ##
    ## Public Methods

    def Depends(self):
        return self._defaults.depends

    def Requires(self, pkg):
        if str(pkg) in self._data.depends:
            return True
        else:
            return False

    def Package(self):
        pass

    def Download(self, first=False):
        if isinstance(self._data.source, str_types):
            self._fetch(self._data.source)
            return self._data.source
        elif isinstance(self._data.source, list):
            for uri in self._data.source:
                self._fetch(uri)
                if first:
                    return uri

    def Extract(self):
        return self._extract(os.path.basename(self._data.source))

    def Patch(self):
        if isinstance(self._data.patches, str_types):
            self._patch(os.path.basename(self._data.patches))
        elif isinstance(self._data.patches, list):
            for uri in self._data.patches:
                self._patch(os.path.basename(uri))

    def Build(self, force=None, clean=None, verbose=None):
        try:
            # Let's get our downloading out of the way.
            #source = self.Download(first=True)
            #self._data.source = self._data.patches
            #self.Download()
            #self._data.source = source
            # Now let's extract
            #self.Extract()
            # Apply those patches
            #self.Patch()
            # And set about doing the real work
            for method in ((self._data.configure, 'Configuring.'),
                           (self._data.compile,   'Compiling.'),
                           (self._data.install,   'Installing.')):
                if method[0].enable:
                    lineOut("%s %s" % (block(str(self)), method[1]))
                    dname = '%s/%s-%s' % (self._cfg.dirs.pkgtemp,
                                          self._data.package,
                                          self._data.version)
                    self._cmd(dname, method[0])
        except Exception as e:
            fatal(repr(msg.args))
            sys.exit(1)

