# What is MVM
MVM is a version manager. That was simple right? What does it do? Well, if you are familiar with projects like RVM, and VirtualEnv, Multipy and others, then you know what MVM does. The big thing (to me at least) is that it will manage multiple versions of any package. It is data driven, you describe how to build the package with a json file.

# Installing MVM

The 2 methods officially supported for installation are:
* From the git repository.

>
> git clone https://github.com/fuzzy/mvm.git
> cd mvm ; sudo ./setup.py install
>

* Using pip via PyPI

>
> pip install mvm
>

At this point some instructions are printed out, nice and bold, colorful, hard to miss. But just in case one did (hey, these things happen), I'll repeat them below:

At this point, if you have installed manually from the git repo, you will want to add the following to your ~/${SHELL}rc:

>
> export MVM_SESSION_ID=$(mvm-session)
> export MVM_GLOBAL_DIR=${HOME}/.mvm/sessions/global
> export MVM_SESSION_DIR=${HOME}/.mvm/sessions/local/${MVM_SESSION_ID}
>
> test ! -d ${MVM_GLOBAL_DIR} && mkdir -p ${MVM_GLOBAL_DIR}
> test ! -d ${MVM_SESSION_DIR} && mkdir -p ${MVM_SESSION_DIR}
>
> export PATH=${MVM_GLOBAL_DIR}/bin:${MVM_GLOBAL_DIR}/sbin:${MVM_SESSION_DIR}/bin:${MVM_SESSION_DIR}/sbin:${PATH}
>

And the following to ~/.bash_logout, or ~/.logout for csh, ksh, sh, or ~/.zlogout for zsh

>
> test ! -z "${MVM_SESSION_DIR}" && test -d ${MVM_SESSION_DIR} && rm -rf ${MVM_SESSION_DIR}
>

If you haven't already done so, now is the time to

>
> rm -rf ~/.mvm/packages/pkgspecs
> git clone http://github.com/fuzzy/mvmspecs.git ~/.mvm/packages/pkgspecs
>

# Using MVM

* TODO

## Showing help and version information

* TODO

## Listing installed packages

* TODO

## Listing available packages

* TODO

## Installing packages

* TODO

## Enabling packages

* TODO

## Disabling packages

* TODO
