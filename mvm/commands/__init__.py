from mvm.commands.pkglist import *
from mvm.commands.enable  import *
from mvm.commands.install import *

class MvmCommands(MvmCmdList, MvmCmdEnable, MvmCmdInstall):
    pass
