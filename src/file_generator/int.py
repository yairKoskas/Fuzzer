import random

from generator import Generator


class Int(Generator):

    def __init__(self, size, name=None, value=None, endian='little'):
        self._size = size
        self.name = name
        self._value = value
        self._endian = endian

    def valid_value(self) -> bytes:
        # if value is not specified, choose at random
        if self._value is None:
            value = random.randint(0, 2 ** self._size)
        else:
            value = self._value

        return value.to_bytes(self._size, byteorder=self._endian)

    def invalid_value(self):
        value = random.randint(0, 2 ** self._size)
        return value.to_bytes(self._size, byteorder=self._endian)
