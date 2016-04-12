# Author: Mike 'Fuzzy' Partin
# Copyright: (c) 2016-2018
# Email: fuzzy@fumanchu.org
# License: See LICENSE.md for details

# Stdlib imports
import os
import re
import sys
import json

# Internal imports
from mvm.term import *

class Edict(dict):
    def __init__(self, data={}):
        for key in data:
            if isinstance(data[key], dict):
                self.__setitem__(key, Edict(data[key]))
            else:
                self.__setitem__(key, data[key])

    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __setattr__(self, attr, value):
        self.__setitem__(attr, value)

    def __setitem__(self, attr, value):
        dict.__setitem__(self, attr, value)
        dict.__setattr__(self, attr, value)

class Elist(list):
    def __init__(self, data=[]):
        for itm in data:
            if isinstance(itm, list):
                self.append(Elist(itm))
            else:
                self.append(itm)

    def unique(self, index):
        cnt = 0
        for itm in self:
            if itm == self[index]:
                cnt += 1
        if cnt != 1:
            return False
        else:
            return True

    def last(self):
        return self[-1:][0]

class MvmConfig(object):

    def _readConfig(self):
        # First we load our main configuration
        cfg_file              = False
        for cfg in ('/etc/mvm.cfg', '~/.mvmrc'):
            if os.path.isfile(cfg):
                cfg_file      = cfg
                break
        if not cfg_file:
            fatal('Neither /etc/mvm.cfg nor ~/.mvmrc were found. Cannot continue.')
            sys.exit(1)
        cfg                   = Edict(json.loads(open(cfg_file, 'r').read()))
        for d in cfg.dirs:
            tcfg              = re.sub('~', os.getenv('HOME'), cfg.dirs[d])
            cfg.dirs[d]       = tcfg
        if os.path.isdir(cfg.dirs['cfgdata']):
            if os.path.isfile('%s/arguments.json' % cfg.dirs['cfgdata']):
                tfp           = open('%s/arguments.json' % cfg.dirs['cfgdata'])
                cfg.arguments = Edict(json.loads(tfp.read()))
            else:
                fatal("I can't load my commandline argument metadata.")
                sys.exit(1)
        self.config           = cfg
