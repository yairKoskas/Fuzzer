from file_generator import generator
from file_generator import mutation_report

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
    return a report on the exact mutation that was done
    '''
    def mutate(self) -> mutation_report.MutationReport:
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
    get the offset of the field in the parent field
    '''
    def get_offset(self):
        return self._parent.get_offset_by_name(self._name)

    '''
    get the absolute offset of the field in the file
    '''
    def get_absolute_offset(self):
        return self._parent.get_abs_offset_by_name(self._name)

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

    '''
    get the offset of a child element by name
    '''
    def get_offset_by_name(self, name):
        pass

    '''
    get the absolute offset of a child element by name
    '''
    def get_abs_offset_by_name(self, name):
        pass


    '''
    access a child field by name
    '''
    def __getitem__(self, name):
        pass
    
    '''
    check if have child with name
    '''
    def __contains__(self, name):
        pass