from file_generator import generator_parser
import sys

path = sys.argv[1]
parser = generator_parser.GeneratorParser(path)
a = parser.generators['file'].valid_value()

with open('output.bmp', 'wb') as f:
    f.write(a)