from file_generator import generator

'''
An abstract class that represents a field in a file format (might be complex type field).
Essentially each Field object is equivalent to a certain generator, but has value which you can operate on.
'''
class Field:
    def __init__(self, name=None, relation=None) -> None:
        self._relation = relation
        self._has_relation = relation is not None
        self._name = name
        self._parent = None

    '''
    size of the value that the field holds
    '''
    def __len__(self):
        pass

    '''
    get the current value, in bytes
    '''
    def value(self) -> bytes:
        pass

    '''
    change the current value of the field (after the change it night be invalid)
    '''
    def mutate(self):
        pass

    '''
    change the value to match the relation
    '''
    def set_to_relation(self):
        pass

    '''
    return True if the object has a relation
    '''
    def has_relation(self):
        return self._has_relation

    '''
    get the relation of the generator
    '''
    def get_relation(self) -> 'generator.Relation':
        if self._has_relation:
            return self._relation

    def set_parent(self, parent: 'ParentField'):
        self._parent = parent

'''
A field that have children fields that he have to reslove relations for
'''
class ParentField(Field):
    def __init__(self, name=None, relation=None) -> None:
        super().__init__(name, relation)

        # a paren field should always be called with set_to_relation (to resolve its children relations)
        self._has_relation = True

    '''
    get a relation and return the required value for this relation.
    '''
    def resolve_relation(self, relation:'generator.Relation') -> int:
        pass