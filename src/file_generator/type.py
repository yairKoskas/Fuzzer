import random

from generator import Generator

'''
custom type, combine a group of generators.
'''


class Type(Generator):
    '''
    generators - list of generators
    '''

    def __init__(self, generators: list):
        self._generators = generators

    def valid_value(self):
        ret = b''
        for gen in self._generators:
            ret += gen.valid_value()

        return ret

    def invalid_value(self):
        # choose one generator to have invalid value
        idx = random.randint(0, len(self._generators))

        ret = b''
        for i, gen in enumerate(self._generators):
            if i == idx:
                ret += gen.invalid_value()
            else:
                ret += gen.valid_value()

        return ret
