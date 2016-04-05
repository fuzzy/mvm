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

    def __setitem__(self, attr, value):
        dict.__setitem__(self, attr, value)
        self.__setattr__(attr, value)

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
            cfg.dirs[d]       = re.sub('~', os.getenv('HOME'), cfg.dirs[d])
        if os.path.isdir(cfg.dirs['cfgdata']):
            if os.path.isfile('%s/arguments.json' % cfg.dirs['cfgdata']):
                tfp           = open('%s/arguments.json' % cfg.dirs['cfgdata'])
                cfg.arguments = Edict(json.loads(tfp.read()))
            else:
                fatal("I can't load my commandline argument metadata.")
                sys.exit(1)
        self.config           = cfg
