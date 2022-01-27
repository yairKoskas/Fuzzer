import random

from file_generator.field import Field
from file_generator.generator import Generator

class Int(Field):
    def __init__(self, name, size, endian, value, relation):
        super().__init__(name, relation) 
        self._size = int(size)
        self.name = name
        self._value = value
        self._endian = endian

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
        if random.randint(0,2):
            # take an extreme value to test edge cases
            extreme_vals = [0, 2**self._size-1, 2**(self._size-1)-1,-2**(self._size-1)]
            self._value = random.choice(extreme_vals)
        else:
            # take random value
            self._value = random.randint(0, 2**self._size-1)


class IntGenerator(Generator):

    def __init__(self, size, min_val=0, max_val=None, name=None, value=None, endian='little'):
        super().__init__(name) 
        self._size = size
        self.name = name
        self._value = value
        self._value = value
        self._endian = endian
        self._max_val = max_val
        self._min_val = min_val

    def _valid_value(self):
        # if value is not specified, choose at random
        if self._value is not None:
            value = int(self._value)
        else:
            max_val = int(self._max_val) if self._max_val is not None else 256**int(self._size)
            value = random.randint(int(self._min_val),max_val)

        return value

    def get_field(self):
        return Int(self._name, int(self._size), self._endian, self._valid_value(), self._relation)
