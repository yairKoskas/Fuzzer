import os
from pdb import runeval
import sys
import signal
import subprocess
from factories.coverage_evaluator_factory import CoverageEvaluatorFactory

class Runner:

    '''
    run a program with given arguments and check is it crashed.

    parametrs:
    path - path to the program to run.
    args - list of arguments to the program.

    returns: the return code of the program.
    '''
    def run(self, path, args, timeout, saved_states=None):
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


class CoverageRunner:
    def __init__(self, coverage_type, program):
        self.coverage_evaluator = CoverageEvaluatorFactory.create_evaluator(coverage_type, program)
    '''
    run a program with given arguments and check is it crashed.

    parametrs:
    path - path to the program to run.
    args - list of arguments to the program.

    returns: the return code of the program.
    '''
    def run(self, path, args, timeout, saved_states):
        if not os.path.isfile(path) or not os.access(path, os.X_OK):
            raise Exception('File doesn\'t exist or isn\'t executable')
        states, proc_code = self.coverage_evaluator.get_coverage(path, args, timeout)
        if len(states - saved_states) > 0:
            # save the new states in the set
            saved_states |= states
            # signal to the fuzzer that the program reached a new state
            proc_code = 2
        return proc_code
