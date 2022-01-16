import os
import random

from file_generator.field import Field
from file_generator.generator import Generator

'''
A field for arbitrary data without certain structure.
'''
class Data(Field):
    def __init__(self, name, size, value, relation):
        super().__init__(name, relation)
        self._size = int(size)
        self.name = name
        self._value = value

    def __len__(self):
        return self._size

    def value(self):
        return self._value

    def set_to_relation(self):
        if self._has_relation:
            self._value = bytes(self._parent.resolve_relation(self._relation))

    def mutate(self):
        # replace random char
        idx = random.randrange(0,len(self._value))
        new_value = list(self._value)
        new_value[idx] = random.randint(0,256)
        self._value = bytes(new_value)


class DataGenerator(Generator):
    # maximum length of the default value
    MAX_LENGTH = 20

    def __init__(self, size=None, name=None, value=None, min_size=None, max_size=None):
        super().__init__(name)
        self.name = name
        self._value = value
        self._size = size

        self._max_size = int(max_size) if max_size is not None else DataGenerator.MAX_LENGTH
        self._min_size = int(min_size) if min_size is not None else 0

    def _valid_value(self):
        # if value is not specified, choose at random
        if self._size is not None:
            size = int(self._size)
        else:
            size = random.randint(self._min_size, self._max_size)

        # if value is not specified, choose at random
        if self._value is not None:
            return self._value.encode()
        else:
            return os.urandom(size)

    def get_field(self) -> bytes:
        val = self._valid_value()
        return Data(self._name, len(val), val, self._relation)

