import os
import random

from file_generator.field import Field
from file_generator.generator import Generator
from file_generator.mutation_report import MutationReport


'''
A field for arbitrary data without certain structure.
'''
class Data(Field):
    def __init__(self, name, size, value, relation):
        super().__init__(name, relation)
        self._size = int(size)
        self._value = value
        self._mutations = [self._bit_flipping, self._swap_byte]

    def __len__(self):
        return self._size

    def value(self):
        return self._value

    def set_to_relation(self):
        if self._has_relation:
            self._value = self._parent.resolve_relation(self._relation).to_bytes(self._size, 'big')

    def mutate(self):
        mut = random.choice(self._mutations)
        return mut()

    # mutations methods
    # ------------------------------------------------------
    def _swap_byte(self):
        if len(self._value) > 0:
            idx = random.randrange(0,len(self._value))
            new_value = list(self._value)
            old_val = new_value[idx]
            new_value[idx] = random.randint(0,255)
            self._value = bytes(new_value)

            return MutationReport(self._name, f'change byte in the index of {idx} from {old_val} to {self._value[idx]}')

    def _bit_flipping(self):
        ratio = random.choice([0.01, 0.1, 0.3])
        bits_to_flip = int((len(self._value) * 8) * ratio) + 1

        mask = [0] * (len(self._value)*8)
        for _ in range(bits_to_flip):
            #flip random bit
            mask[random.randint(0,len(mask)-1)] = 1

        # convert mask to bytes
        mask = bytes([int("".join(map(str, mask[i:i+8])), 2) for i in range(0, len(mask), 8)])

        self._value = bytes([x^y for x,y in zip(self._value,mask)])
        return MutationReport(self._name, f'flipped {ratio} of the bits bits')
    # ------------------------------------------------------


class DataGenerator(Generator):
    # maximum length of the default value
    MAX_LENGTH = 20

    '''
    size - size of the data (in bytes).
    name - id of the object.
    min_size - minimum size of the data.
    max_size - maximum size of the data.
    value - value of the data (as a hex string).
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
        if self._size is not None:
            size = int(self._size)
        else:
            size = random.randint(int(self._min_size), int(self._max_size))

        # if value is not specified, choose at random
        if self._value is not None:
            return bytes.fromhex(self._value)
        else:
            return os.urandom(size)

    def get_field(self) -> bytes:
        val = self._valid_value()
        return Data(self._name, len(val), val, self._relation)

