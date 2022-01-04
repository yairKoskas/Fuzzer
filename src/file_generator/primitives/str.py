import random
import string

from file_generator.generator import Generator


class Str(Generator):
    # maximum length of the default value
    MAX_LENGTH = 20

    def __init__(self, name=None, size=None, value=None):
        self.name = name
        self._value = value
        self._size = size

    def valid_value(self):
        # if value is not specified, choose at random
        if self._size is not None:
            size = self._size
        else:
            size = random.randint(0, Str.MAX_LENGTH + 1)

        # if value is not specified, choose at random
        if self._value is not None:
            return self._value.encode()
        else:
            value = ''.join(random.choices(string.ascii_letters + string.digits, k=size))
            return value.encode()

    def invalid_value(self):
        size = random.randint(0, Str.MAX_LENGTH + 1)
        value = ''.join(random.choices(string.ascii_letters + string.digits, k=size))
        return value.encode()
