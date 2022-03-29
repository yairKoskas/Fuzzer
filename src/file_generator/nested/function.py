import random
from importlib import import_module

from file_generator.field import Field, ParentField
from file_generator.generator import Generator
from exception import FuzzerException


'''
A function that acts on some data.
'''
class Function(ParentField):
    def __init__(self, name, field, function):
        super().__init__(name)
        self.name = name
        self._child = field
        self._function = function

        # set the parents of all children to self
        self._child.set_parent(self)

        self._value = self._function(self._child.value())
        if not isinstance(self._value, bytes):
            raise FuzzerException('function must return bytes object')

        self._mutations = [self._mutate_child, self._mutate_data]

    def __len__(self):
        return len(self._value)

    def value(self):
        return self._value

    def resolve_relation(self, relation):
        return self._parent.resolve_relation(relation)

    def set_to_relation(self):
        self._child.set_to_relation()

        self._value = self._function(self._child.value())
        if not isinstance(self._value, bytes):
            raise FuzzerException('function must return bytes object')

    def mutate(self):
        mut = random.choice(self._mutations)
        mut()

    # mutations methods
    # ------------------------------------------------------

    # mutate data itself
    def _mutate_data(self):
        if len(self._value) > 0:
            idx = random.randrange(0,len(self._value))
            new_value = list(self._value)
            new_value[idx] = random.randint(0,255)
            self._value = bytes(new_value)

    # mutate child and activate function
    def _mutate_child(self):
        self._child.mutate()

        self._value = self._function(self._child.value())
        if not isinstance(self._value, bytes):
            raise FuzzerException('function must return bytes object')
    # ------------------------------------------------------


class FunctionGenerator(Generator):

    '''
    generator - generator to activate the function on.
    name - id of the object.
    module_name - name of the module where the function located.
    function_name - name of the function.
    '''
    def __init__(self, generator: Generator, module_name : str, function_name : str, name=None):
        super().__init__(name)
        self.name = name
        self._generator = generator
        self._function = self._import_function(module_name, function_name)

    # import function fro a module
    def _import_function(self, module_name : str, function_name : str):
        try:
            module = import_module(module_name)
        except Exception:
            raise FuzzerException(f'cannot import module {module_name}')
        if function_name not in dir(module):
            raise FuzzerException(f'function {function_name} does not exist in module {module_name}')

        return getattr(module, function_name)

    def get_field(self) -> Function:
        return Function(self.name, self._generator.get_field(), self._function)