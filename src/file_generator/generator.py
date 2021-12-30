

'''
An interface for generator.
A generator can generate bytes arbitrary or by some rules, 
it can also use other generators to generate data recursivly.
Support generating valid data and also mutating it.
'''
class Generator:
    '''
    Upon initialization, always holds valid data (or 'dummy' data if waiting to resolve a relation)
    '''
    def __init__(self) -> None:
        pass

    '''
    Return the size of data generated, in bytes.
    '''
    def __len__(self) -> int:
        return 0

    '''
    Get the current data of the genrator.
    '''
    def value(self) -> bytes:
        pass

    '''
    Mutate the current data of the generator (might be invalid afterwards).
    '''
    def mutate(self):
        pass
