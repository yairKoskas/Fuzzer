import random

from file_generator.field import Field
from file_generator.generator import Generator

'''
A generator for choosing random generator from a list.
'''
class ChoiceGenerator(Generator):
    '''
    generators - list of generators
    '''
    def __init__(self, generators: list, name=None):
        super().__init__(name)
        self.name = name
        self._generators = generators


    def get_field(self) -> Field:
        gen = random.choice(self._generators)

        return gen.get_field()