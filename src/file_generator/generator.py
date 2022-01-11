from file_generator import field

'''
A class that holds information about relations.
'''
class Relation:

    def __init__(self, type, target) -> None:
        self.type = type
        self.target = target

'''
An interface for generator.
A generator can represents an element in the template format XMl file.
Can return Field class which holds actual value.
'''
class Generator:
    def __init__(self, name=None) -> None:
        self._relation = None
        self._has_relation = False
        self._name = name

    '''
    return field object with a valid value.
    '''
    def get_field(self):
        pass

    '''
    return True if the object has a relation
    '''
    def has_relation(self):
        return self._has_relation

    '''
    set the relation of the generator
    '''
    def set_relation(self, relation: 'Relation'):
        self._has_relation = True
        self._relation = relation

    '''
    get the relation of the generator
    '''
    def get_relation(self) -> 'Relation':
        if self._has_relation:
            return self._relation
