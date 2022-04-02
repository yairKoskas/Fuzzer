from evaluators.block_evaluator import BlockEvaluator
from evaluators.edge_evaluator import EdgeEvaluator
class CoverageEvaluatorFactory:
    def create_evaluator(type: str, program: str):
        if type == "block":
            return BlockEvaluator(program)
        elif type == "edge":
            return EdgeEvaluator(program)
        else:
            raise ValueError('No such coverage type')
