from fuzzers import generator_fuzzer

import sys
import os


def main():
    if len(sys.argv) < 4:
        print('Usage: python3 main.py [path_to_executable] [template file] [crash_folder] [times]')
        return -1

    program, template_file, crash_folder = sys.argv[1], sys.argv[2], sys.argv[3]

    if len(sys.argv) > 4:
        times = int(sys.argv[4])
    else:
        times = 'inf'

    if not os.path.isfile(program) or not os.access(program, os.X_OK):
        print('File doesn\'t exist or isn\'t executable')
        return -1

    if not os.path.isdir(crash_folder):
        os.mkdir(crash_folder)


    fuzzer = generator_fuzzer.GeneratorFuzzer(program, template_file, crash_folder)
    fuzzer.fuzz_multiple(times)


if __name__ == "__main__":
    main()
