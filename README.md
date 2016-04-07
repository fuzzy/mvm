# What is MVM
MVM is a version manager. That was simple right? What does it do? Well, if you are familiar with projects like RVM, and VirtualEnv, Multipy and others, then you know what MVM does. The big thing (to me at least) is that it will manage multiple versions of any package. It is data driven, you describe how to build the package with a json file.

# Installing MVM

The 2 methods officially supported for installation are:
* From the git repository.

```
git clone https://github.com/fuzzy/mvm.git
cd mvm ; sudo ./setup.py install
```

* Using pip via PyPI

```
pip install mvm
```

At this point some instructions are printed out, nice and bold, colorful, hard to miss. But just in case one did (hey, these things happen), I'll repeat them below:

You will want to add the following to your ~/${SHELL}rc:

```
export MVM_SESSION_ID=$(mvm-session)
export MVM_GLOBAL_DIR=${HOME}/.mvm/sessions/global
export MVM_SESSION_DIR=${HOME}/.mvm/sessions/local/${MVM_SESSION_ID}

test ! -d ${MVM_GLOBAL_DIR} && mkdir -p ${MVM_GLOBAL_DIR}
test ! -d ${MVM_SESSION_DIR} && mkdir -p ${MVM_SESSION_DIR}

export PATH=${MVM_GLOBAL_DIR}/bin:${MVM_GLOBAL_DIR}/sbin:${MVM_SESSION_DIR}/bin:${MVM_SESSION_DIR}/sbin:${PATH}
```

And the following to ~/.bash_logout, or ~/.logout for csh, ksh, sh, or ~/.zlogout for zsh

```
test ! -z "${MVM_SESSION_DIR}" && test -d ${MVM_SESSION_DIR} && rm -rf ${MVM_SESSION_DIR}
```

If you haven't already done so, now is the time to

```
rm -rf ~/.mvm/packages/pkgspecs
git clone http://github.com/fuzzy/mvmspecs.git ~/.mvm/packages/pkgspecs
```

# Using MVM

#### Showing help and version information

```
$ mvm help # or mvm with no arguments
Usage: mvm command <opt> <...> <PACKAGESPEC>

disable   	Disable usage of a given package.
       -g	Disable in the global profile.
enable    	Enable a given package.
       -g	Enable in the global profile.
help      	Show this help screen.
install   	Install a given package.
       -f	Force installation (possibly overwriting files)
       -c	Clean any previous installation out before installing.
       -v	Show compiler messages.
list      	List installed or available packages.
       -a	Show available packages.
remove    	Remove a given package.
version   	Show the version.

Example: mvm install -c -v python-2.7.11
$ mvm version
mvm (Myriad Version Manager) v0.2.1
```

#### Listing installed packages

```
$ mvm list
Installed Packages:

Python   (3.5.1)
Bash     (4.34.3.30)

* = Session, * = Global
```

I would like to note, that those asterisks are color coded in the terminal output. To quote the prophet, "I'm mad, I'm not ill".

#### Listing available packages

```
$ mvm list -a
Available Packages:

Bash     (2.05b, 4.3.30, 4.3, 4.4-beta)
Lua      (5.0.3, 5.1.5, 5.2.4, 5.3.2)
Nim      (latest)
Perl     (5.12.5, 5.14.4, 5.16.3, 5.18.4, 5.20.3, 5.22.1)
Python   (2.5.6, 2.6.9, 2.7.11, 3.1.5, 3.2.6, 3.3.6, 3.4.4, 3.5.1)
Ruby     (1.9.3-p551, 2.0.0-p648, 2.1.10, 2.2.4, 2.3.0)
Slang    (2.3.0)
Tcl      (8.6.5)
Tk       (8.6.5)
```

## Installing packages

```
$ mvm install python-3.5.1
>> https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tar.xz
>> 14.10MB in 33s @ 437.66KB/sec
>> Extracting Python-3.5.1.tar.xz
>> Configuring.
>> Compiling.
>> Installing.
```

## Enabling packages

```
$ mvm enable lua-2.3.0
```

## Disabling packages

```
$ mvm disable lua-2.3.0
```

## Uninstalling packages

```
$ mvm remove python-3.5.1
```
