#!/usr/bin/env python

from gi.repository.Gdk import Screen

def X_is_running():
    '''Returns true if X.org is running'''
    try:
        if Screen().get_default():
            return True
    except RuntimeError:
        pass
    return False

if __name__ == "__main__":
    if X_is_running():
        print "X is running"
    else:
        print "X is not running"
