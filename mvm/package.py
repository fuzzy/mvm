# Author: Mike 'Fuzzy' Partin
# Copyright: (c) 2016-2018
# Email: fuzzy@fumanchu.org
# License: See LICENSE.md for details

# Stdlib imports
import os
import re
import sys
import json
import shutil

# Internal imports
from mvm.term import *

class Package(object):
    def __init__(self, cfg, path):
        # External use stuff
        self.Path      = path
        self.SessionID = os.getenv('MVM_SESSION_ID')
        data           = path.split('/')[-4:]
        self.Name      = data[0]
        self.Platform  = data[1]
        self.Arch      = data[2]
        self.Version   = data[3]
        # Internal use stuff
        self._gprofile = '%s/global.json' % cfg.dirs.profiles
        self._sprofile = '%s/session.json' % cfg.dirs.profiles
        self._config   = cfg
        self._sessiond = '%s/%s' % (cfg.dirs.sessionroot,
                                    self.SessionID)

    def __str__(self):
        return '%s-%s' % (self.Name, self.Version)

    def __repr__(self):
        print(self.__str__())

    def _link(self, session=True):
        src            = self.Path
        if session:
            dst        = self._sessiond
        else:
            dst        = self._config.dirs.globalroot
        # Output
        if session:
            print('%s Linking %s into session dir.' % (cyan('>>'), self.Name))
        else:
            print('%s Linking %s into global dir.' % (green('>>'), self.Name))
        # Work
        for r,d,f in os.walk(src):
            for i in f:
                sfile  = '%s/%s' % (r, i)
                dfile  = '%s%s/%s' % (dst, r.replace(src, ''), i)
                try: os.symlink(sfile, dfile)
                except OSError: pass
            for i in d:
                tdir   = '%s%s/%s' % (dst, r.replace(src, ''), i)
                if not os.path.isdir(tdir):
                    os.mkdir(tdir)

    def _unlink(self, session=True):
        src            = self.Path
        if session:
            dst        = self._sessiond
        else:
            dst        = self._config.dirs.globalroot
        sdobj = {}
        dirs  = []
        # Output
        if session:
            print('%s Unlinking %s from the session dir.' % (cyan('>>'), self.Name))
        else:
            print('%s Unlinking %s from the global dir.' % (green('>>'), self.Name))
        # Work
        for r,d,f in os.walk(src):
            for i in f:
                sfile = '%s%s/%s' % (dst, r.replace(src, ''), i)
                if os.path.islink(sfile):
                    if os.readlink(sfile) == r+'/'+i:
                        os.unlink(sfile)
            for i in d:
                dirs.append(r.replace(self.Path, '')+'/'+i)
        dirs.sort(key=len)
        dirs.reverse()
        for d in dirs:
            if len(os.listdir('%s%s' % (dst, '/'.join(d.split('/'))))) == 0:
                os.rmdir('%s%s' % (dst, '/'.join(d.split('/'))))

    def Enable(self, session=True):
        if session:
            data = json.loads(open(self._sprofile).read())
            if self.Name.lower() not in data[self.SessionID].keys():
                data[self.SessionID][self.Name.lower()] = [self.Version,]
            else:
                if self.Version not in data[self.SessionID][self.Name.lower()]:
                    data[self.SessionID][self.Name.lower()].append(self.Version)
            open(self._sprofile, 'w+').write(json.dumps(data))
        else:
            data = json.loads(open(self._gprofile).read())
            if self.Name.lower() not in data.keys():
                data[self.Name.lower()] = [self.Version,]
            else:
                if self.Version not in data[self.Name.lower()]:
                    data[self.Name.lower()].append(self.Version)
            open(self._gprofile, 'w+').write(json.dumps(data))
        self._link(session)

    def Disable(self, session=True):
        if session:
            data = json.loads(open(self._sprofile).read())
            if self.Name.lower() in data[self.SessionID].keys():
                if len(data[self.SessionID][self.Name.lower()]) > 1:
                    for cnt in range(0, len(data[self.SessionID][self.Name.lower()])):
                        if data[self.SessionID][self.Name.lower()][cnt] == self.Version:
                            data[self.SessionID][self.Name.lower()].pop(cnt)
                            break
                else:
                    data[self.SessionID].pop(self.Name.lower(), False)
                open(self._sprofile, 'w+').write(json.dumps(data))
        else:
            data = json.loads(open(self._gprofile).read())
            if self.Name.lower() in data.keys():
                if len(data[self.Name.lower()]) > 1:
                    for cnt in range(0, len(data[self.Name.lower()])):
                        if data[self.Name.lower()][cnt] == self.Version:
                            data[self.name.lower()].pop(cnt)
                            break
                else:
                    data.pop(self.Name.lower(), False)
                open(self._gprofile, 'w+').write(json.dumps(data))
        self._unlink(session)

    def IsGlobal(self):
        data = json.loads(open(self._gprofile).read())
        if self.Name.lower() not in data.keys():
            return False
        else:
            if self.Version in data[self.Name.lower()]:
                return True
            else:
                return False

    def IsSession(self):
        data = json.loads(open(self._sprofile).read())
        if self.Name.lower() not in data[self.SessionID].keys():
            return False
        else:
            if self.Version in data[self.SessionID][self.Name.lower()]:
                return True
            else:
                return False

    def Delete(self):
        # If there is more than 1 version, delete just me
        if len(os.listdir(self.Path+'/../')) > 1:
            shutil.rmtree(self.Path)
        else:
            shutil.rmtree(self._config.dirs.instroot+'/'+self.Name)

    def Display(self):
        if self.IsGlobal():
            return green(self.Version)
        elif self.IsSession():
            return cyan(self.Version)
        else:
            return white(self.Version)
