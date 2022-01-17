from file_generator import generator_parser

import sys
import os


# simple main file to generate valid file to test template file
def main():
    if len(sys.argv) < 2:
        print('Usage: python3 main.py [template file] [extension]')
        return -1

    template_file, extension = sys.argv[1], sys.argv[2]

    pars = generator_parser.GeneratorParser(template_file)

    content = pars.generators['file'].get_field()
    content.set_to_relation()
    with open(f'output.{extension}', 'wb') as f:
        f.write(content.value())

    


if __name__ == "__main__":
    main()
