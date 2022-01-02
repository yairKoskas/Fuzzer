import random

from generator import Generator

'''
A generator for repeating on a generator multiple times.
'''
class Repeat(Generator):
    # max repeatitions for default value
    MAX_TIMES = 20

    '''
    generator - generator to repeat.
    '''
    def __init__(self, generator: Generator, times=None):
        self._generator = generator
        self._times = times


    def valid_value(self):
        if self._times != 0:
            times = self._times
        else:
            times = random.randint(0,Repeat.MAX_TIMES)

        ret = b''
        for _ in range(times):
            ret += self._generator.valid_value()
        
        return ret


    def invalid_value(self):
        if self._times != 0:
            times = self._times
        else:
            times = random.randint(0,Repeat.MAX_TIMES)

        # have only 1 invalid value
        idx = random.randint(0,times)

        ret = b''
        for i in range(times):
            if i == idx:
                ret += self._generator.invalid_value()
            else:
                ret += self._generator.valid_value()
        
        return ret