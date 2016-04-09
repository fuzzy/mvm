#!/usr/bin/env python

# Stdlib imports
import os
import sys
from setuptools import setup

# Internal imports
from mvm.term import *

def append(fr, to):
    to.write(open(fr).read())

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='mvm',
      version='0.3.0',
      author="Mike 'Fuzzy' Partin",
      author_email='fuzzy@fumanchu.org',
      description='MVM is a tool for managing multiple versions of....anything. Think rvm+virtualenv+luaenv+goenv+allTheOtherEnvs and then go even further. Manage multiple versions of vim, or hexdump, wget if you want too.',
      license='BSD',
      keywords='setuptools deployment installation distutils',
      url='https://github.com/fuzzy/mvm',
      long_description=read('README.md'),
      classifiers=["Development Status :: 2 - Pre-Alpha",
                   "Topic :: Utilities",
                   "Topic :: System :: Systems Administration",
                   "Topic :: System :: Software Distribution",
                   "Topic :: System :: Operating System",
                   "Topic :: System :: Installation/Setup",
                   "License :: OSI Approved :: BSD License",
                   "Environment :: Console",
                   "Intended Audience :: System Administrators",
                   "Intended Audience :: Developers",
                   "Intended Audience :: Ender Users/Desktop",
                   "Operating System :: POSIX",],
      packages=['mvm', 'mvm.commands'],
      scripts=['bin/mvm', 'bin/mvm-session'],
      data_files=[('/etc', ['etc/mvm.cfg']),
                  ('/etc/mvm.d', ['etc/mvm.d/arguments.json'])])

if sys.argv[1] == 'install':
    if sys.stdout.isatty():
        shell = os.getenv('SHELL')
    else:
        shell = 'bash'
    prompt    = '%s%s' % (cyan('>'), white('>'))
    print('\n%s %s' % (prompt, yellow('At this point, if you have installed manually')))
    print('%s %s' % (prompt, yellow('from the git repo, you will want to')))
    print('%s %s' % (prompt, yellow('add the following to your ~/%src:\n' % os.path.basename(shell))))
    print(white(read('./shells/mvm-%s-login.sh' % os.path.basename(shell))))
    print('%s %s' % (prompt, yellow('And the following to ~/.bash_logout')))
    print('%s %s\n' % (prompt, yellow('(or ~/.logout [csh,ksh,sh], or ~/.zlogout [zsh])')))
    print(white(read('./shells/mvm-%s-logout.sh' % os.path.basename(shell))))
    print('%s %s' % (prompt, yellow("If you haven't already done so, now is the time to")))
    print('%s %s' % (prompt, yellow("rm -rf ~/.mvm/packages/pkgspecs")))
    print('%s %s' % (prompt, yellow("git clone http://github.com/fuzzy/mvmspecs.git ~/.mvm/packages/pkgspecs")))

