import random
import os

from mutators import mutator

# simple mutator that flips random bit
class BitFlippingMutator(mutator.Mutator):
    '''
    xor 2 arrays of bytes
    '''
    def _xor(self, a, b):
        return bytes([x^y for x,y in zip(a,b)])

    '''
    mutate the data
    '''
    def mutate(self, data: bytes):
        mask = [0] * (len(data)*8)
        mask[random.randint(0,len(mask)-1)] = 1

        # convert mask to bytes
        mask = bytes([int("".join(map(str, mask[i:i+8])), 2) for i in range(0, len(mask), 8)])

        return self._xor(data, mask)

# try to set some intresting values
class ExtremeValueMutator(mutator.Mutator):
    '''
    mutate the data
    '''
    def mutate(self, data: bytes):
        # number of bytes to set
        size = random.choice([1,2,4])
        value = random.choice([0, 2**(8*size)-1, 2**(8*size-1)-1,-2**(8*size-1)])
        if value <  0:
            value = value.to_bytes(size, byteorder='little', signed=True)
        else:
            value = value.to_bytes(size, byteorder='little')

        where_to_set = random.randint(0, len(data) - size - 1)
        return data[:where_to_set] + value + data[where_to_set+size:]

# change random byte to random value
class ByteSetMutator(mutator.Mutator):
    '''
    mutate the data
    '''
    def mutate(self, data: bytes):
        idx = random.randrange(0,len(data))
        new_value = list(data)
        new_value[idx] = random.randint(0,255)
        return bytes(new_value)

# insert random byte
class ByteInsertMutator(mutator.Mutator):
    '''
    mutate the data
    '''
    def mutate(self, data: bytes):
        # number of bytes to insert, value is 1 to 4
        size = random.randrange(1, 4)

        # where to insert
        insert_at = random.randrange(0,len(data)+1)

        return data[:insert_at] + os.urandom(size) + data[insert_at:]

# delete random byte
class ByteDeleteMutator(mutator.Mutator):
    '''
    mutate the data
    '''
    def mutate(self, data: bytes):
        # number of bytes to delete, value is 1 to 4
        size = random.randrange(1, 4)

        if len(data) <= size:
            return data

        # where to delete
        delete_at = random.randrange(0,len(data)-size)

        return data[:delete_at] + data[delete_at+size:]

# duplicate chunk of data
class DuplicateMutator(mutator.Mutator):
    '''
    mutate the data
    '''
    def mutate(self, data: bytes):
        # number of bytes to duplicate
        size = random.choice([1,2,4,8])

        if len(data) <= size:
            return data

        # what to duplicate
        dup_at = random.randrange(0,len(data)-size)

        return data[:dup_at + size] + data[dup_at:dup_at + size] + data[dup_at+size:]


