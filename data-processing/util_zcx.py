#!/usr/bin/env python
import subprocess
import sys, os

def run_command(args, log_file=None):
    ''' use subprocess (instead of subprocess32) to run system
    command. print stdout to log_file if not empty.
    '''
    cmd=' '.join(args)
    if log_file:
        p=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    else:
        p=subprocess.Popen(cmd,shell=True)
    sys.stdout.write(cmd+('' if not log_file else '>'+log_file)+'\n')
    stdout,stderr=p.communicate()
    if log_file:
        fp=open(log_file,'w')
        fp.write(stdout)
        fp.close()
    return stdout

def make_dir_if_not_exist(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
