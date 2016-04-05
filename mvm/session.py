# Author: Mike 'Fuzzy' Partin
# Copyright: (c) 2016-2018
# Email: fuzzy@fumanchu.org
# License: See LICENSE.md for details

# Stdlib imports
import os
import json
import time

# Internal imports
from mvm.term import *

class MvmSession(object):

    def _startSession(self):
        dataFile                 = self.config.dirs.profiles+'/session.json'
        data                     = json.loads(open(dataFile).read())
        if self.SessionID not in data.keys():
            data[self.SessionID] = {"timestamp": time.time()}
            open(dataFile, 'w+').write(json.dumps(data))
        sessionDir               = '%s/%s' % (self.config.dirs.sessionroot,
                                              self.SessionID)
        if not os.path.isdir(sessionDir):
            os.mkdir(sessionDir)
