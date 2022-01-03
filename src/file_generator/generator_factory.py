import data
import int
import str
import type

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
