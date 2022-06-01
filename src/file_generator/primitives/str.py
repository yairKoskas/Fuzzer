import random
import string

from file_generator.field import Field
from file_generator.generator import Generator
from file_generator.mutation_report import MutationReport

class Str(Field):
    def __init__(self, name, size, value, relation):
        super().__init__(name, relation)
        self._size = int(size)
        self._value = value

    def __len__(self):
        return self._size

    def value(self):
        return self._value.encode()

    def set_to_relation(self):
        if self._has_relation:
            self._value = str(self._parent.resolve_relation(self._relation))

    def mutate(self):
        # replace random char
        idx = random.randrange(0,len(self._value))
        new_value = list(self._value)
        new_value[idx] = random.choice(string.ascii_letters + string.digits)
        self._value = ''.join(new_value)

        return MutationReport(self._name, f'changed char at index {idx} to {self._value[idx]}')


class StrGenerator(Generator):
    # maximum length of the default value
    MAX_LENGTH = 20

    '''
    size - size of the string.
    min_size - minimum size of the string.
    max_size - minimum size of the string.
    value - value of the string.
    '''
    def __init__(self, size=None, name=None, value=None, min_size=0, max_size=MAX_LENGTH):
        super().__init__(name)
        self._value = value
        self._size = size

        self._max_size = max_size
        self._min_size = min_size

    '''
    generate value for the field
    '''
    def _valid_value(self):
        # if value is not specified, choose at random
        size = int(self._size) if self._size is not None else random.randint(int(self._min_size), int(self._max_size))

        # if value is not specified, choose at random
        if self._value is not None:
            return str(self._value)
        else:
            value = ''.join(random.choices(string.ascii_letters + string.digits, k=size))

        return value

    def get_field(self) -> bytes:
        val = self._valid_value()
        return Str(self._name, len(val), val, self._relation)

