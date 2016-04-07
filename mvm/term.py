# Author: Mike 'Fuzzy' Partin
# Copyright: (c) 2016-2018
# Email: fuzzy@fumanchu.org
# License: See LICENSE.md for details

# Stdlib imports
import math
import datetime

def red(txt):
    return '\033[1;31m%s\033[0m' % txt

def green(txt):
    return '\033[1;32m%s\033[0m' % txt

def yellow(txt):
    return '\033[1;33m%s\033[0m' % txt

def blue(txt):
    return '\033[1;34m%s\033[0m' % txt

def purple(txt):
    return '\033[1;35m%s\033[0m' % txt

def cyan(txt):
    return '\033[1;36m%s\033[0m' % txt

def white(txt):
    return '\033[1;37m%s\033[0m' % txt

# Console messages
# TODO: the framework for this, should take cues from the config file
#       and if no console output is desired, do the right thing, as
#       well as logging to file. But that will come later.

def debug(txt):
    print('%s: %s' % (cyan('DEBUG'), txt))

def info(txt):
    print('%s: %s' % (green('INFO'), txt))

def warn(txt):
    print('%s: %s' % (yellow('WARN'), txt))

def error(txt):
    print('%s: %s' % (red('ERROR'), txt))

def fatal(txt):
    error(txt)

def OutputWord(word):
    return '%s%s' % (cyan(word[0].upper()), white(word[1:].lower()))

def lineOut(txt):
    print('%s%s %s' % (cyan('>'), white('>'), txt))

def humanTime(amount):
    secs  = float(datetime.timedelta(seconds=amount).total_seconds())
    units = [("d", 86400), ("h", 3600), ("m", 60), ("s", 1)]
    parts = []
    for unit, mul in units:
        if secs / mul >= 1 or mul == 1:
            if mul > 1:
                n = int(math.floor(secs / mul))
                secs -= n * mul
            else:
                n = secs if secs != int(secs) else int(secs)
            parts.append("%s%s" % (n, unit)) #, "" if n == 1 else "s"))
    return "".join(parts)

# This function turns a size (given in bytes) into
# a human readable string

def humanSize(size):
    if size <= 1024:
        return '%dB' % size
    else:
        smap = {1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB', 5: 'PB'}
        mod  = 1
        while mod <= len(smap.keys()):
            if size >= (1024 ** mod) and size < (1024 ** (mod+1)):
                return '%.02f%s' % ((float(size) / float(1024.00 ** float(mod))), smap[mod])
            mod += 1
