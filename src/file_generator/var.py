import random

'''
A variable that can be used to chose integer values for fields.
Variables should generate value before a generator generates a field.
'''
class Var:

    def __init__(self, name, min_val=None, max_val=None):
        self._name = name

        self._max_val = int(max_val) if max_val is not None else 256**4
        self._min_val = int(min_val) if min_val is not None else 0

        self.choose_value()
        self._current_value = 0

    '''
    Generate a valid value for the variable and save it in the current state of the variable.
    '''
    def choose_value(self):
        self._current_value = random.randint(self._min_val,self._max_val)

    def set_value(self, val):
        self._current_value = val

    '''
    Get the current value of the variable as an int.
    '''
    def __int__(self):
        return self._current_value