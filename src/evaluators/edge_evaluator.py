from evaluators.coverage_evaluator import CoverageEvaluator
from evaluators.scripts.ghidra_cfg import get_cfg
from collections import defaultdict
from typing import Set

class EdgeEvaluator(CoverageEvaluator):

    def __init__(self, program):
        super().__init__(program)
        self._graph = get_cfg(program)

    def get_coverage(self, inp) -> Set:
        # use the same frida script for the block but use it on the graph instead
        super().get_coverage(inp)
    
    def attach_and_get_coverage(self, pid) -> Set:

        super().attach_and_get_coverage(pid)
