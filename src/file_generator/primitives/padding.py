import random

from file_generator.field import Field
from file_generator.generator import Generator, relation

'''
Used for padding.
'''
class Padding(Field):

    '''
    value - value to padd with.
    alignment - padd until a the size until the padding is a multiple of multiple_of.
    '''
    def __init__(self, name, alignment, value):
        super().__init__(name)

        # set has_relation since set_to_relation have to called on this
        self._has_relation = True

        self._size = 0
        self.name = name
        self._value = value
        self._alignment = alignment

    def __len__(self):
        return self._size

    def value(self):
        return bytes([self._value]*self._size)

    def set_to_relation(self):
        # get offset of self
        rel = Relation('offset', self.name)
        offset = self._parent.resolve_relation(rel)
        self._size = (-offset) % self._alignment

    def mutate(self):
        pass


class PaddingGenerator(Generator):
    '''
    value - value to padd with.
    alignment - padd until a the size until the padding is a multiple of multiple_of.
    '''
    def __init__(self, alignment, name=None, value=0):
        super().__init__(name) 
        self.name = name
        self._value = value
        self._alignment = alignment

    def get_field(self):
        return Padding(self._name, int(self._alignment), int(self._value))
