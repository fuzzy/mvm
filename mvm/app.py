# Stdlib imports
import os
import sys
import json
import socket
import multiprocessing

# Internal imports
from mvm.term            import *
from mvm.config          import *
from mvm.session         import *
from mvm.commands        import *

class Mvm(MvmConfig, MvmSession, MvmCommands):

    _majorVer = 0
    _minorVer = 1
    _patchLvl = 3

    sysInfo   = Edict({
        'os': {
            'name': os.uname()[0],
            'vers': os.uname()[2],
            'arch': os.uname()[-1:][0],
            'cpus': multiprocessing.cpu_count()
        },
        'hostname': socket.gethostname(),
        'username': os.getenv('USER'),
        'homedir':  os.getenv('HOME'),
        'path':     os.getenv('PATH')
    })

    SessionID = os.getenv('MVM_SESSION_ID')

    def __init__(self, args):
        if self.SessionID == None:
            print('%s: There is a problem, either your shell is not' % red('FATAL ERROR'))
            print('%s: picking up the MVM init files, or MVM has been' % red('FATAL ERROR'))
            print('%s: otherwise misconfigured.' % red('FATAL ERROR'))
            sys.exit(1)
        self._handlers = {}
        self._readConfig()
        self._startSession()
        self._argParse(args)

    def showVersion(self):
        print('%s (%s%s %s%s %s%s) v%s.%s.%s' % (cyan('mvm'),
                                                 cyan('M'),
                                                 white('yriad'),
                                                 cyan('V'),
                                                 white('ersion'),
                                                 cyan('M'),
                                                 white('anager'),
                                                 yellow(str(self._majorVer)),
                                                 yellow(str(self._minorVer)),
                                                 yellow(str(self._patchLvl))))

    def showHelp(self):
        print('%s%s: %s %s <%s> <%s> <%s>\n' % (cyan('U'),
                                                white('sage'),
                                                os.path.basename(sys.argv[0]),
                                                white('command'),
                                                yellow('opt'),
                                                yellow('...'),
                                                purple('PACKAGESPEC')))
        commands = list(self.config.arguments.keys())
        commands.sort()
        for cmd in commands:
            if self.config.arguments[cmd]['handler'] != 'None':
                print('%s\t%s' % (white('%-10s' % cmd),
                                  self.config.arguments[cmd]['help']))
                if 'options' in self.config.arguments[cmd].keys():
                    for arg in self.config.arguments[cmd]['options']:
                        print('%5s%s\t%s' % (' ', yellow('%5s' % arg[0]), arg[1]))
        print('\n%s%s: %s %s %s %s %s' % (cyan('E'),
                                          white('xample'),
                                          os.path.basename(sys.argv[0]),
                                          white('install'),
                                          yellow('-c'),
                                          yellow('-v'),
                                          purple('python-2.7.11.json')))
        sys.exit(1)

    def _argParse(self, args):
        if len(args) > 1:

            if args[1] not in self.config.arguments.keys():
                self.showHelp()
            else:
                # We really don't need the program name
                args.pop(0)

                # ok, we have a valid command, now let's see if we
                # have a valid handler
                if self.config.arguments[args[0]]['handler']:
                    # it appears so, so let's record our handler
                    command      = args[0]
                    handlerObj   = self.config.arguments[args[0]]['handler']
                else:
                    # it appears not, so let's bitch about it.
                    raise(ValueError, 'Handler for this command not yet implimented.')
                args.pop(0)

                # We can start building our handler reference
                handlerStr       = 'self.%s(' % handlerObj
                endItem          = ''
                # Now let's care about our suboptions
                for arg in args:
                    if arg[0] == '-':
                        valid = False
                        for opt in self.config.arguments[command].options:
                            if opt[0] == arg:
                                valid = True
                        if valid:
                            for opt in self.config.arguments[command].options:
                                if opt[0] == arg:
                                    handlerStr += '%s=%r,' % (opt[2][0], opt[2][1])
                        else:
                            warn('%s is not a valid option. Ignored.' % arg)
                    else:
                        endItem  = arg
                if endItem != '':
                    handlerStr  += 'arg="%s")' % endItem
                else:
                    if handlerStr[-1:][0] == ',':
                        tmpStr       = '%s)' % handlerStr[:-1]
                        handlerStr   = tmpStr
                    else:
                        handlerStr += ')'
                # And finally, let's handle the shit
                eval(handlerStr)

        else:
            self.showHelp()
