from file_generator import generator_parser
import sys

path = sys.argv[1]
parser = generator_parser.GeneratorParser(path)
a = parser.generators['file'].get_field()
a.set_to_relation()

with open('output.bmp', 'wb') as f:
    f.write(a.value())