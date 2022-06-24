import sys
import os
import json
import argparse

# add current working directory to path, used for function feature
sys.path.append(os.getcwd())

from fuzzers import mutation_fuzzer
from mutators import simple_mutators
from mutators import combine_mutator
import mutators.combine_mutator as combine_mutator
from fuzzers import generator_fuzzer
from fuzzers import covergae_fuzzer
from exception import FuzzerException


'''
main function for generation fuzzing
'''
def main_generate(args):
    template_file = args.input

    try:
        fuzzer = generator_fuzzer.GeneratorFuzzer(args.program, template_file, args.crash_folder, args.timeout, args.extension, args.args, args.non_crashing_codes)
        fuzzer.fuzz_multiple(args.times if args.times >= 0 else 'inf')
    except FuzzerException as e:
        print(f'error: {str(e)}')
        return -1

'''
main function for blackbox mutaion fuzzing.
'''
def main_mutate(args):
    corpus = args.input

    mutator = combine_mutator.CombinetMutator(
        [simple_mutators.BitFlippingMutator(),
        simple_mutators.ByteDeleteMutator(),
        simple_mutators.ByteInsertMutator(),
        simple_mutators.ExtremeValueMutator(),
        simple_mutators.ByteSetMutator(),
        simple_mutators.DuplicateMutator()])

    try:
        fuzzer = mutation_fuzzer.MutationFuzzer(args.program, mutator, args.crash_folder, args.timeout, args.extension, args.args, args.non_crashing_codes)
        fuzzer.fuzz_corpus(corpus, args.times if args.times >= 0 else 'inf')
    except FuzzerException as e:
        print(f'error: {str(e)}')
        return -1

'''
main function for blackbox mutaion fuzzing.
'''
def main_coverage(args):
    corpus = args.input

    mutator = combine_mutator.CombinetMutator(
        [simple_mutators.BitFlippingMutator(),
        simple_mutators.ByteDeleteMutator(),
        simple_mutators.ByteInsertMutator(),
        simple_mutators.ExtremeValueMutator(),
        simple_mutators.ByteSetMutator(),
        simple_mutators.DuplicateMutator()])

    try:
        fuzzer = covergae_fuzzer.CoverageFuzzer(args.program, mutator, args.crash_folder, args.timeout, args.extension, args.args, args.non_crashing_codes, args.coverage)
        fuzzer.fuzz_corpus(corpus, args.times if args.times >= 0 else 'inf')
    except FuzzerException as e:
        print(f'error: {str(e)}')
        return -1

def main():
    main_parser = argparse.ArgumentParser(description='Fuzzer')
    main_parser.add_argument('-p', '--program', type=str, required=True,
                        help='path to target program.')
    main_parser.add_argument('-t', '--type', type=str, required=True,
                        help='type of the fuzzer, can be mutation, generation or coverage')
    main_parser.add_argument('-c', '--crash_folder', type=str, default='./crash',
                        help='path to save the files that caused the program to crash.')
    main_parser.add_argument('--times', type=int, default=-1,
                        help='number of iterations of fuzzing. -1 for infinty.')
    main_parser.add_argument('--timeout', type=int, default=5,
                        help='stop the target program after a certain amount of seconds if program don\'t halt.')
    main_parser.add_argument('-i', '--input', type=str, required=True,
                        help='path to corpus directory or template format file.')
    main_parser.add_argument('-e', '--extension', type=str, default='txt',
                        help='extension of the input files.')
    main_parser.add_argument('-a', '--args', type=str, nargs='+', default=['<fuzzed>'],
                        help='arguments to pass to the target program. \"<fuzzed>\" will be replaced by the fuzzed file.')
    main_parser.add_argument('--non_crashing_codes', type=int, nargs='+', default=[],
                        help='return codes that are not considered as a crash (except 0 and 1).')
    main_parser.add_argument('-cov', '--coverage', type=str, required=False,
                        help='code coverage type for coverage-based fuzzing.')


    args = main_parser.parse_args()
    args.args = list(map(lambda s: s.lstrip(), args.args))

    if not os.path.isfile(args.program) or not os.access(args.program, os.X_OK):
        print('File doesn\'t exist or isn\'t executable')
        return -1

    if not os.path.isdir(args.crash_folder):
        os.mkdir(args.crash_folder)

    if args.type == 'mutation' or args.type == 'mut':
        return main_mutate(args)
    elif args.type == 'generation' or args.type == 'gen':
        return main_generate(args)
    elif args.type == 'coverage' or args.type == 'cov':
        return main_coverage(args)
    else:
        print(f'fuzzing type {args.type} not supported')
        return -1


if __name__ == "__main__":
    main()
