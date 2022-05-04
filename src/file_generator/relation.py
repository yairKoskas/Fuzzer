from importlib import import_module

from file_generator import field
from exception import FuzzerException


'''
Abstract class that holds information about relations.
children should implement the resolve function.
'''
class Relation:

    def __init__(self, type, target_name) -> None:
        self.type = type
        self.target = target_name

    '''
    Resolve the value of the relation given the target field
    '''
    def resolve(self, target : 'field.Field') -> int:
        pass

class SizeRelation(Relation):

    def __init__(self, type, target) -> None:
        super().__init__('size', target)

    '''
    Resolve the value of the relation given the target field
    '''
    def resolve(self, target : 'field.Field') -> int:
        return len(target)

class OffsetRelation(Relation):

    def __init__(self, type, target) -> None:
        super().__init__('offset', target)

    '''
    Resolve the value of the relation given the target field
    '''
    def resolve(self, target : 'field.Field') -> int:
        return target.get_offset()

class AbsOffsetRelation(Relation):

    def __init__(self, type, target) -> None:
        super().__init__('abs_offset', target)

    '''
    Resolve the value of the relation given the target field
    '''
    def resolve(self, target : 'field.Field') -> int:
        return target.get_absolute_offset()

class FunctionRelation(Relation):

    def __init__(self, type, target, module_name, function_name) -> None:
        super().__init__('function', target)
        self._function = self._import_function(module_name, function_name)

    '''
    Resolve the value of the relation given the target field
    '''
    def resolve(self, target : 'field.Field') -> int:
        return self._function(target.value())

    # import function from a module
    def _import_function(self, module_name : str, function_name : str):
        try:
            module = import_module(module_name)
        except Exception:
            raise FuzzerException(f'cannot import module {module_name}')
        if function_name not in dir(module):
            raise FuzzerException(f'function {function_name} does not exist in module {module_name}')

        return getattr(module, function_name)

# a dictionary that maps relation names to their classes
relation_by_name = {
    'size' : SizeRelation,
    'offset' : OffsetRelation,
    'absOffset' : AbsOffsetRelation,
    'function' : FunctionRelation
}