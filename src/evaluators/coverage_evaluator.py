from typing import Set


class CoverageEvaluator:

    program: str
    possible_states: Set

    """
    @brief constructor
    @param program path to program
    """
    def __init__(self, program):
        self.program = program

    """
    @brief returns the set of states the input has reached in the program
    @param inp input to the program
    @return Set of states
    """
    def get_coverage(self, inp) -> Set:
        pass
    
    """
    @brief attaches to an already spawned process and monitors the code coverage
    @param pid the pid of the process to attach to
    @return Set of states
    """
    def attach_and_get_coverage(self, pid) -> Set:
        pass
