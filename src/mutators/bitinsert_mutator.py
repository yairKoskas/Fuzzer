import random
import os

# simple mutator that insert random bytes in the array
class BitInsertMutator:

    '''
    parameters:
    insert_size - tuple (a,b), means that we insert strings in length of size a to b
    '''
    def __init__(self, insert_size=(1,5)):
        self.insert_size_start = insert_size[0]
        self.insert_size_end = insert_size[1]

    '''
    mutate the data
    '''
    def mutate(self, data: bytes):
        # number of bytes to insert
        size = random.randrange(self.insert_size_start, self.insert_size_end)

        # where to insert
        insert_at = random.randrange(0,len(data)+1)

        return data[:insert_at] + os.urandom(size) + data[insert_at:]


