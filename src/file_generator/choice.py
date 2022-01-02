import os
import random

from generator import Generator

'''
A generator for choosing random generator from a list.
'''
class Choice(Generator):

    '''
    generators - list of generators
    '''
    def __init__(self, generators: list):
        self._generators = generators


    def valid_value(self):
        gen = random.choice(self._generators)
        
        return gen.valid_value()


    def invalid_value(self):
        gen = random.choice(self._generators)
        
        return gen.invalid_value()