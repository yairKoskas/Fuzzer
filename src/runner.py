import os
from pdb import runeval
import sys
import signal
import subprocess

class Runner:

    '''
    run a program with given arguments and check is it crashed.

    parametrs:
    path - path to the program to run.
    args - list of arguments to the program.

    returns: the return code of the program.
    '''
    def run(self, path, args, timeout):
        if not os.path.isfile(path) or not os.access(path, os.X_OK):
            raise Exception('File doesn\'t exist or isn\'t executable')

        proc = subprocess.Popen([path] + args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        # wait for process to finish, if it didn't finish in a certain amout of time, terminate it.
        try:
            pass
            proc.wait(timeout)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
            return 1

        proc.wait()
        return proc.returncode