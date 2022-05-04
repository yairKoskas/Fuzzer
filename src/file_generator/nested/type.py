import random
import functools

from file_generator.field import ParentField
from file_generator.generator import Generator, relation
from exception import FuzzerException
from file_generator.mutation_report import MutationReport


'''
custom type, combine a group of generators.
'''
class Type(ParentField):
    def __init__(self, name, fields):
        super().__init__(name)
        self.name = name
        self._children = fields
        self._child_names = [f.name for f in self._children]

        self._mutations = [self._mutate_child, self._delete_child]
        self._weights = [7, 1]

        # set the parents of all children to self
        for f in self._children:
            f.set_parent(self)

    def __len__(self):
        return sum(len(f) for f in self._children)

    def value(self):
        ret = functools.reduce(lambda a, b: a+b.value(), self._children, b'')

        return ret

    # return the size of an element by name
    def _get_size_by_name(self, name):
        if name == 'father':
            return len(self)
            
        field = self._children[self._child_names.index(name)]
        return len(field)

    # return offset of an element by name
    def get_offset_by_name(self, name):
        idx = self._child_names.index(name)
        return sum(len(f) for f in self._children[:idx])

    # return absolute offset of an element by name
    def get_abs_offset_by_name(self, name):
        if self._parent is None:
            return self.get_offset_by_name(name)

        return self._parent.get_abs_offset_by_name(self.name) + self._get_offset_by_name(name)

    def resolve_relation(self, relation):
        # look for the target
        target_name = relation.target

        if target_name == 'father':
            target = self
        else:
            target = self._children[self._child_names.index(target_name)]

        return relation.resolve(target)

    def set_to_relation(self):
        for f in self._children:
            f.set_to_relation()

    def mutate(self):
        mut = random.choices(self._mutations, weights=self._weights)[0]
        return mut()

    # mutations methods
    # ------------------------------------------------------

    # delete random child
    def _delete_child(self):
        if len(self._children) > 0:
            idx = random.randint(0, len(self._children)-1)
            deleted_child = self._children.pop(idx)
            return MutationReport(self.name, f'deleted {deleted_child.name}')

    # mutate random child
    def _mutate_child(self):
        if len(self._children) > 0:
            idx = random.randint(0,len(self._children)-1)
            report = self._children[idx].mutate()

            if report is not None:
                report.add_parent(self.name)
                return report
    # ------------------------------------------------------


class TypeGenerator(Generator):

    def __init__(self, generators: list, name=None):
        super().__init__(name)
        self.name = name
        self._generators = generators


    def get_field(self) -> bytes:
        fields = [gen.get_field() for gen in self._generators]
        fields = list(filter(None, fields))
        return Type(self._name, fields)

    '''
    copy the generator with different name
    '''
    def copy_with_name(self, name):
        return TypeGenerator(self._generators, name)
