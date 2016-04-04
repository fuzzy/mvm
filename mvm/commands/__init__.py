from mvm.commands.pkglist import *
from mvm.commands.enable  import *
from mvm.commands.install import *
from mvm.commands.remove  import *

class MvmCommands(MvmCmdList, MvmCmdEnable, MvmCmdInstall, MvmCmdRemove):
    pass
