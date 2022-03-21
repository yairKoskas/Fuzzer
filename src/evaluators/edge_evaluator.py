from coverage_evaluator import CoverageEvaluator
from typing import Set


class EdgeEvaluator(CoverageEvaluator):

    def __init__(self, program):
        super().__init__(program)

    def get_coverage(self, inp) -> Set:
        super().get_coverage(inp)
    
    def attach_and_get_coverage(self, pid) -> Set:
        super().attach_and_get_coverage(pid)
