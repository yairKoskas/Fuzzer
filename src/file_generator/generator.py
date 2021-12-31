

'''
An interface for generator.
A generator can generate bytes arbitrary or by some rules, 
it can also use other generators to generate data recursivly.
Support generating valid data and also mutating it.
'''
class Generator:
    def __init__(self) -> None:
        pass

    '''
    Get valid value.
    '''
    def valid_value(self) -> bytes:
        pass

    '''
    Get (maybe) invalid value.
    '''
    def invalid_value(self) -> bytes:
        pass
