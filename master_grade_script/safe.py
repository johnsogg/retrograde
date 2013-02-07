#!/usr/bin/env python

import signal
import subprocess
from sys import argv, exit, stdout
import os

class TakingTooLong(Exception):
    pass

def alarm_handler(signum, frame):
    raise TakingTooLong

def run_thing(cmd):
    rc = 0
    print "Running process: " + cmd
    proc = subprocess.Popen(
        cmd,
        stderr=stdout, #subprocess.STDOUT,
        stdout=stdout, # subprocess.PIPE,
        shell=True)
    try:
        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(5) # in seconds
        stdoutdata, stderrdata = proc.communicate()
        rc = proc.returncode
        signal.alarm(0)
    except TakingTooLong:
        print "Process took too long. Killing it."
        # Wisdom from http://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
        # says I should kill process using the os.killpg (stands for kill process group)
        # This is because my process is the shell (shell=True). Killing the group kills
        # all child processes as well (and what I need is the child process).
        pid = proc.pid
        # proc.kill()
        os.killpg(pid, signal.SIGKILL)
        print "Killed process group starting with " + str(pid)
        rc = -1
    return rc


if __name__ == "__main__":
    cmd = " ".join(argv[1:])
    print "cmd: "+ cmd
    return_code = run_thing(cmd)
    exit(return_code)
# sys.exit(41)
