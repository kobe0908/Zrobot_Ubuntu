#!/usr/bin/env python

from subprocess import Popen, PIPE
def execute(cmd):
    '''Shells out and executes the command, returning error code'''
    proc = Popen(cmd, stdout=PIPE, stdin=PIPE, shell=True)
    stdout, stderr = proc.communicate()
    return proc.returncode

