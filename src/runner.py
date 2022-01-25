import os
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
    def run(self, path, args):
        if not os.path.isfile(path) or not os.access(path, os.X_OK):
            raise Exception('File doesn\'t exist or isn\'t executable')

        proc = subprocess.Popen([path] + args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_data, stderr_data = proc.communicate()    # currently not supporting user input
        proc.poll()
        return proc.returncode