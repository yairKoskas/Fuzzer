from file_generator.primitives import data
from file_generator.primitives import int
from file_generator.primitives import str
from file_generator import type

mapping = {
    'int': int.Int,
    'str': str.Str,
    'type': type.Type,
    'data': data.Data,
    # currently, no custom mapping - will add custom generators later
}


class GeneratorFactory:

    @staticmethod
    def get_generator(_type: type):
        generator = mapping.get(_type, None)
        return generator
