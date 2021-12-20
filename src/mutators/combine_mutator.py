import random
import os

# combine 2 mutators
class CombinetMutator:

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
        # choose mutator
        mutator = random.choice(self.mutators)
        return mutator.mutate(data)


