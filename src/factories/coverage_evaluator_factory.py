from evaluators.block_evaluator import BlockEvaluator
from evaluators.edge_evaluator import EdgeEvaluator
class CoverageEvaluatorFactory:
    def create_evaluator(type: str):
        if type == "block":
            return BlockEvaluator()
        elif type == "edge":
            return EdgeEvaluator()
        else:
            raise ValueError('No such coverage type')
