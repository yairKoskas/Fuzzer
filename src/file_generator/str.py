import random
import string

from generator import Generator


class Str(Generator):
    # maximum length of the default value
    MAX_LENGTH = 20

    def __init__(self, size=None, value=None):
        self._init_value = value

        # if value is not specified, choose at random
        if size is not None:
            self._size = size
        else:
            self._size = random.randint(0,Str.MAX_LENGTH+1)
        
        # if value is not specified, choose at random
        if value is not None:
            self._value = value
            self._size = len(value)
        else:
            self._value = ''.join(random.choices(string.ascii_letters + string.digits, k = self._size))    

    def __len__(self) -> int:
        return self._size

    def value(self) -> bytes:
        return self._value


    def mutate(self):
        # not implemented yet
        pass
