import random
import functools

from file_generator.field import Field, ParentField
from file_generator.generator import Generator

'''
A generator for repeating on a generator multiple times.
'''
class Repeat(ParentField):
    def __init__(self, name, fields):
        super().__init__(name)
        self.name = name
        self._children = fields

        self._mutations = [self._mutate_child, self._mutate_child, self._delete_child]

        # set the parents of all children to self
        for f in self._children:
            f.set_parent(self)

    def __len__(self):
        return sum(len(f) for f in self._children)

    def value(self):
        ret = functools.reduce(lambda a, b: a+b.value(), self._children, b'')

        return ret

    def resolve_relation(self, relation):
        return self._parent.resolve_relation(relation)

    def set_to_relation(self):
        for f in self._children:
            f.set_to_relation()

    def mutate(self):
        mut = random.choice(self._mutations)
        mut()

    # mutations methods
    # ------------------------------------------------------

    # delete random child
    def _delete_child(self):
        if len(self._children) > 0:
            idx = random.randint(0, len(self._children)-1)
            self._children.pop(idx)

    # mutate random child
    def _mutate_child(self):
        if len(self._children) > 0:
            idx = random.randint(0,len(self._children)-1)
            self._children[idx].mutate()
    # ------------------------------------------------------


class RepeatGenerator(Generator):
    # max repeatitions for default value
    MAX_TIMES = 20

    '''
    generator - generator to repeat.
    name - id of the object.
    times - numbers of times to repeat duplicate the generator.
    max_times - maximum numbers of times to repeat duplicate the generator.
    min_times - minimum numbers of times to repeat duplicate the generator.
    '''
    def __init__(self, generator: Generator, name=None, times=None, max_times=MAX_TIMES, min_times=0):
        super().__init__(name)
        self.name = name
        self._generator = generator
        self._times = times
        self._max_times = max_times
        self._min_times = min_times

    def get_field(self) -> bytes:
        times = int(self._times) if self._times is not None else random.randint(int(self._min_times), int(self._max_times))
        fields = [self._generator.get_field() for _ in range(times)]
        return Repeat(self._name, fields)