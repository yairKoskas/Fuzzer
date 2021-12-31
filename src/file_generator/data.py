import os
import random

from generator import Generator

'''
A generator for arbitrary data without certain structure.
'''
class Data(Generator):
    # maximum length of the default value
    MAX_LENGTH = 20

    def __init__(self, size=None, value=None):
        self._value = value
        self._size = size


    def valid_value(self):
        # if value is not specified, choose at random
        if self._size is not None:
            size = self._size
        else:
            size = random.randint(0,Data.MAX_LENGTH+1)
        
        # if value is not specified, choose at random
        if self._value is not None:
            return self._value.encode()
        else:
            return os.urandom(size)


    def invalid_value(self):
        size = random.randint(0,Data.MAX_LENGTH+1)
        return os.urandom(size)
