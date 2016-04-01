# Stdlib imports
import os
import re
import json

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
        for r,d,f in os.walk(src):
            for i in f:
                sfile  = '%s/%s' % (r, i)
                dfile  = '%s%s/%s' % (dst, r.replace(src, ''), i)
                os.symlink(sfile, dfile)
            for i in d:
                tdir   = '%s%s/%s' % (dst, r.replace(src, ''), i)
                if not os.path.isdir(tdir):
                    os.mkdir(tdir)

    def _unlink(self, session=True):
        files = []
        for r,d,f in os.walk(self.Path):
            for i in f: files.append('%s/%s' % (r.split(self.Version)[1], i))
        if session:
            sdir = self._sessiond
        else:
            sdir = self._config.dirs.globalroot
        for f in files:
            if os.path.isfile('%s%s' % (sdir, f)):
                os.unlink('%s%s' % (sdir, f))

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

    def Display(self):
        if not self.IsGlobal():   g = ' '
        else:                     g = green('G')
        if not self.IsSession():  s = ' '
        else:                     s = cyan('S')
        print('[%1s%1s] %s-%s' % (g,
                                  s,
                                  self.Name,
                                  self.Version))
