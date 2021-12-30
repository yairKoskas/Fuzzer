import random

from generator import Generator


class Int(Generator):

    def __init__(self, size, value=None, endian='little'):
        self._size = size
        self._init_value = value
        self._endian = endian
        
        # if value is not specified, choose at random
        if value == None:
            self._value = random.randint(0,2**size)
        else:
            self._value = value

    def __len__(self) -> int:
        return self._size

    def value(self) -> bytes:
        return self._value.to_bytes(self._size, byteorder=self._endian)


    def mutate(self):
        # not implemented yet
        pass
