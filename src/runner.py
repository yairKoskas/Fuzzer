import os
import sys
import signal
from subprocess import Popen, PIPE

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

        proc = Popen([path] + args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        stdout_data, stderr_data = proc.communicate()    # currently not supporting user input
        proc.poll()
        return proc.returncode
        
