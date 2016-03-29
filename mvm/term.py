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
    cons_error(txt)

