from ..file_generator import str, int, type, data
from ..utils import singleton

mapping = {
    'int': int.Int,
    'str': str.Str,
    'type': type.Type,
    'data': data.Data
}


class GeneratorFactory(metaclass=singleton.Singleton):

    @staticmethod
    def get_generator(_type: type):
        generator = mapping.get(_type, None)
        if not generator:
            raise ValueError(f'Generator for type: {_type} does not exist')
        return generator
