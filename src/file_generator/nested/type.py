import random

from file_generator.field import ParentField
from file_generator.generator import Generator, Relation

'''
custom type, combine a group of generators.
'''
class Type(ParentField):
    def __init__(self, name, fields):
        super().__init__(name)
        self.name = name
        self._children = fields
        self._child_names = [f.name for f in self._children]

        # set the parents of all children to self
        for f in self._children:
            f.set_parent(self)

    def __len__(self):
        return sum(len(f) for f in self._children)

    def value(self):
        ret = b''
        for f in self._children:
            ret += f.value()

        return ret

    def mutate(self):
        # mutate random field
        if len(self._children) > 0:
            idx = random.randint(0,len(self._children)-1)
            self._children[idx].mutate()

    # return the size of an element by name
    def _get_size_by_name(self, name):
        if name == 'father':
            return len(self)
            
        field = self._children[self._child_names.index(name)]
        return len(field)

    # return offset of an element by name
    def _get_offset_by_name(self, name):
        idx = self._child_names.index(name)
        return sum(len(f) for f in self._children[:idx])

    # return absolute offset of an element by name
    def _get_abs_offset_by_name(self, name):
        if self._parent is None:
            return self._get_offset_by_name(name)

        rel = Relation("absOffset", self.name)
        return self._parent.resolve_relation(rel) + self._get_offset_by_name(name)

    def resolve_relation(self, relation):
        if relation.type == "size":
            return self._get_size_by_name(relation.target)
        if relation.type == "offset":
            return self._get_offset_by_name(relation.target)
        if relation.type == "absOffset":
            return self._get_abs_offset_by_name(relation.target)
        
        raise Exception('relation type not supported')

    def set_to_relation(self):
        for f in self._children:
            f.set_to_relation()


class TypeGenerator(Generator):

    def __init__(self, generators: list, name=None):
        super().__init__(name)
        self.name = name
        self._generators = generators


    def get_field(self) -> bytes:
        fields = [gen.get_field() for gen in self._generators]
        return Type(self._name, fields)

    '''
    copy the generator with different name
    '''
    def copy_with_name(self, name):
        return TypeGenerator(self._generators, name)
