import generator_parser

parser = generator_parser.GeneratorParser(r'templateFormat/examples/bmp-24.xml')
print(parser.generators[1].valid_value())