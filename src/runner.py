import os
import uuid
from pdb import runeval
import sys
import signal
import shutil
import subprocess
from factories.coverage_evaluator_factory import CoverageEvaluatorFactory
from evaluators import power_plan_evaluator


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
    def run(self, path, args, timeout, saved_states, corpus):
        if not os.path.isfile(path) or not os.access(path, os.X_OK):
            raise Exception('File doesn\'t exist or isn\'t executable')
        states, proc_code = self.coverage_evaluator.get_coverage(path, args, timeout)
        power_plan_value = power_plan_evaluator.get_value_percentage(states, saved_states)
        if len(states - saved_states) > 0:
            # save the new states in the set
            print(f'Coverage: Added {len(states - saved_states)} blocks')
            saved_states |= states
            # signal to the fuzzer that the program reached a new state
            shutil.copy(args[0], corpus)
        return proc_code, power_plan_value
