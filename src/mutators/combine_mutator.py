import random
import os

from mutators import mutator

# combine multiple mutators
class CombinetMutator(mutator.Mutator):

    '''
    parameters:
    mutators - list of mutators to combine
    '''
    def __init__(self, mutators:list):
        self.mutators = mutators
    '''
    mutate the data
    '''
    def mutate(self, data: bytes):
        times_to_mutate = random.choice([1,2,4,8,16,32])
        for _ in range(times_to_mutate):
            # choose mutator
            mutator = random.choice(self.mutators)
            data = mutator.mutate(data)

        return data


