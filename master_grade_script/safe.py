#!/usr/bin/env python

import signal
import subprocess
from sys import argv, exit, stdout

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
        pid = proc.pid
        proc.kill()
        print "Killed process " + str(pid)
        rc = -1
    return rc


if __name__ == "__main__":
    cmd = " ".join(argv[1:])
    print "cmd: "+ cmd
    return_code = run_thing(cmd)
    exit(return_code)
# sys.exit(41)
