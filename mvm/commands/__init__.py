# Author: Mike 'Fuzzy' Partin
# Copyright: (c) 2016-2018
# Email: fuzzy@fumanchu.org
# License: See LICENSE.md for details

# Internal imports
from mvm.commands.pkglist import *
from mvm.commands.enable  import *
from mvm.commands.install import *
from mvm.commands.remove  import *

class MvmCommands(MvmCmdList, MvmCmdEnable, MvmCmdInstall, MvmCmdRemove):
    pass
