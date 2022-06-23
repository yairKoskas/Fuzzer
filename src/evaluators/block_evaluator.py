import subprocess
import sys

from evaluators.coverage_evaluator import CoverageEvaluator
from utils.drcov import parse_coverage
from typing import Set, Tuple
import frida
import time
import os

modules = []
bbs = []


def check_pid(pid):
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def on_message(msg, data):
    payload = msg['payload']
    global modules
    global bbs
    if 'map' in payload:
        modules.append(payload['map'])
    else:
        bbs.append(data)


class BlockEvaluator(CoverageEvaluator):

    def __init__(self, program):
        super().__init__(program)
        self.frida_device = None
        self.frida_script = None
        self.frida_session = None
        self.pid = -1
        with open('src/evaluators/scripts/frida_coverage.js', 'r') as f:
            self.script_code = f.read()

    def get_coverage(self, path, args, timeout) -> Tuple[Set, int]:
        self.frida_device = frida.get_device('local')
        process = subprocess.Popen([path] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.pid = process.pid
        self.frida_session = self.frida_device.attach(self.pid)
        self.frida_script = self.frida_session.create_script(self.script_code)
        self.frida_script.on('message', on_message)
        self.frida_script.load()
        start = time.time()
        while check_pid(self.pid) and time.time() - start < timeout:
            pass
        process.kill()
        process.communicate()
        coverage_data = bbs
        exitcode = process.returncode
        print('Exitcode: ' + str(exitcode))
        return parse_coverage(coverage_data), exitcode
