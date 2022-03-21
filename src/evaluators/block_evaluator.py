from coverage_evaluator import CoverageEvaluator
from typing import Set


class BlockEvaluator(CoverageEvaluator):

    def __init__(self):
        super().__init__()

    def get_coverage(self, path, inp) -> Set:
        super().get_coverage(inp)
    
    def attach_and_get_coverage(self, pid) -> Set:
        super().attach_and_get_coverage(pid)
