from evaluators.coverage_evaluator import CoverageEvaluator
from utils.drcov import parse_coverage
from typing import Set
import frida
import time


class BlockEvaluator(CoverageEvaluator):

    def __init__(self, program):
        super().__init__(program)
        with open('src/evaluators/scripts/frida_block_coverage.js', 'r') as f:
            self.script_code = f.read()

    def get_coverage(self, path, args, timeout) -> Set:
        self.pid = frida.spawn(path, args)
        self.frida_session = frida.attach(self.pid)
        self.frida_script = self.frida_session.create_script(self.script_code)
        self.frida_script.load()
        self.frida_script.exports.clearcoverage()
        self.frida_script.exports.settarget()
        self.frida_session.resume()
        start = time.time()
        while time.time() - start < timeout:
            stalker_attached, stalker_finished = self.frida_script.exports.checkstalker()
        if not stalker_finished:
            print("Stalker didn't finish after timeout, couldn't get coverage")

            # todo check if crashed, if it crashed, return the exit code, else return 1

        coverage_data = self.frida_script.exports.getcoverage()
        print(coverage_data)
        return parse_coverage(coverage_data)  # , exitcode

