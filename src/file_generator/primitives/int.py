import random
from typing_extensions import Self

from file_generator.field import Field
from file_generator.generator import Generator
from file_generator.mutation_report import MutationReport

class Int(Field):
    '''
    size - size of the integer (in bytes).
    name - id of the object.
    value - value of the integer.
    endian - endianness of the integer (must be 'little' or 'big').
    '''
    def __init__(self, name, size, endian, value, relation):
        super().__init__(name, relation) 
        self._size = int(size)
        self._value = value
        self._endian = endian
        self._mutations = [self._random_value, self._extreme_value, self._inc_or_dec_value]

    def __len__(self):
        return self._size

    def value(self):
        if self._value <  0:
            return self._value.to_bytes(self._size, byteorder=self._endian, signed=True)

        return self._value.to_bytes(self._size, byteorder=self._endian)

    def set_to_relation(self):
        if self._has_relation:
            self._value = self._parent.resolve_relation(self._relation)


    def mutate(self):
        mut = random.choice(self._mutations)
        return mut()
            

    # mutations methods
    # ------------------------------------------------------

    # edge cases
    def _extreme_value(self):
        # 0 and signed\unsigned max\min int
        extreme_vals = [0, 2**(8*self._size)-1, 2**(8*self._size-1)-1,-2**(8*self._size-1)]

        old_val = self._value
        self._value = random.choice(extreme_vals)
        return MutationReport(self._name, f'change value from {old_val} to {self._value}')

    def _random_value(self):
        old_val = self._value
        self._value = random.randint(0, 256**self._size-1)
        return MutationReport(self._name, f'change value from {old_val} to {self._value}')

    # increment or decrement by a small amount
    def _inc_or_dec_value(self):
        # this is common values which might cause problem
        candidates = [1,-1, 2,-2,4,-4,8,-8,16,-16]

        amount = random.choice(candidates)

        if self._value >= 256**self._size-amount or self._value < -amount:
            return

        old_val = self._value
        self._value += amount
        return MutationReport(self._name, f'change value from {old_val} to {self._value} by increamenting by {amount}')
    # ------------------------------------------------------


class IntGenerator(Generator):
    '''
    size - size of the integer (in bytes).
    name - id of the object.
    min_val - minimum value of the integer.
    max_val - maximum value of the integer.
    value - value of the integer.
    endian - endianness of the integer (must be 'little' or 'big').
    '''
    def __init__(self, size, min_val=0, max_val=None, name=None, value=None, endian='little'):
        super().__init__(name) 
        self._size = size
        self._value = value
        self._endian = endian
        self._max_val = max_val
        self._min_val = min_val

    '''
    generate value for the field
    '''
    def _valid_value(self):
        # if value is not specified, choose at random
        if self._value is not None:
            value = int(self._value)
        else:
            max_val = int(self._max_val) if self._max_val is not None else 256**int(self._size) - 1
            value = random.randint(int(self._min_val),max_val)

        return value

    def get_field(self):
        return Int(self._name, int(self._size), self._endian, self._valid_value(), self._relation)
