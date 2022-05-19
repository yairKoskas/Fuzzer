from file_generator.primitives import data
from file_generator.primitives import int
from file_generator.primitives import str
from file_generator.nested import type
from file_generator.primitives import padding
from file_generator.primitives import none

mapping = {
    'int': int.IntGenerator,
    'str': str.StrGenerator,
    'type': type.TypeGenerator,
    'data': data.DataGenerator,
    'padding': padding.PaddingGenerator,
    'none': none.NoneGenerator
}


class GeneratorFactory:

    @staticmethod
    def get_generator(_type: type):
        generator = mapping.get(_type, None)
        return generator
