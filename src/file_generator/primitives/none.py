import random
from typing_extensions import Self

from file_generator.field import Field
from file_generator.generator import Generator
from file_generator.mutation_report import MutationReport

'''
Basically does nothing
'''
class NoneGenerator(Generator):

    def __init__(self, name=None):
        super().__init__(name) 
        self.name = name

    def get_field(self):
        return None