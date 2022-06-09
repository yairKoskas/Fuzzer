from re import L
from file_generator import generator
from file_generator import var
from file_generator import mutation_report

'''
A wrapper for the base generator.
'''
class FileCreator:
    '''
    base_generator - generator for the file format.
    vars - list of variables in the file.
    '''
    def __init__(self, base_generator: generator.Generator, vars: list) -> None:
        self._generator = base_generator
        self._vars = vars

    '''
    create a file and mutate it multiple times.

    mutations - number of the times to mutate the file.

    returns - a tuple of (the file content, list of mutation reports).
    '''
    def create_file(self, mutations: int):
        # set value to all variables
        for v in self._vars:
            v.choose_random_value()

        reports = list()

        # create data for the file and mutate it
        f = self._generator.get_field()
        f.set_to_relation()
        for _ in range(mutations): reports.append(f.mutate())

        return reports, f.value()
