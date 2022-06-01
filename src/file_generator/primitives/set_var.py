import string
from file_generator.generator import Generator

'''
This is pseudo-generator used only to change a variable value.
'''
class SetVarGenerator(Generator):
    '''
    value - value to set the variable.
    vars - dictionary of global variables.
    var_name - name of the variable to set.
    '''
    def __init__(self, value : int, vars : dict, var_name : string, name=None):
        super().__init__(name)
        self._value = value
        self._vars = vars
        self._var_name = var_name

    def get_field(self) -> bytes:
        self._vars[self._var_name].set_value(int(self._value))
        return None