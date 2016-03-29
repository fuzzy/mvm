# Stdlib imports
import os
import sys
import json

# Internal imports
from mvm.term import *

class Edict(dict):
    def __getattr__(self, attr):
        return self.__getitem__(attr)

    def __setitem__(self, attr, value):
        dict.__setitem__(self, attr, value)
        self.__setattr__(attr, value)

def read_config():
    # First we load our main configuration
    cfg_file = False
    for cfg in ('/etc/mvm.cfg', '~/.mvmrc'):
        if os.path.isfile(cfg):
            cfg_file = cfg
            break
    if not cfg_file:
        fatal('Neither /etc/mvm.cfg nor ~/.mvmrc were found. Cannot continue.')
        sys.exit(1)
    config            = Edict(json.loads(open(cfg_file, 'r').read()))
    if os.path.isdir(config.dirs['cfgdata']):
        if os.path.isfile('%s/arguments.json' % config.dirs['cfgdata']):
            tfp = open('%s/arguments.json' % config.dirs['cfgdata'])
            config.arguments = Edict(json.loads(tfp.read()))
        else:
            fatal("I can't load my commandline argument metadata.")
            sys.exit(1)
    return config
