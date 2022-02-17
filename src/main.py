import string
import sys
import os
import json
import argparse

from fuzzers import mutation_fuzzer
import mutators.bitflip_mutator as bitflip_mutator
import mutators.bitinsert_mutator as bitinsert_mutator
import mutators.combine_mutator as combine_mutator
from fuzzers import generator_fuzzer


'''
main function for generation fuzzing
'''
def main_generate(args):
    template_file = args.input
    fuzzer = generator_fuzzer.GeneratorFuzzer(args.program, template_file, args.crash_folder, args.timeout)
    fuzzer.fuzz_multiple(args.times if args.times >= 0 else 'inf')

'''
main function for blackbox mutaion fuzzing.
'''
def main_mutate(args):
    corpus = args.input

    mutator = combine_mutator.CombinetMutator(
        [bitinsert_mutator.BitInsertMutator(), bitflip_mutator.BitFlippingMutator()])

    fuzzer = mutation_fuzzer.MutationFuzzer(args.program, mutator, args.crash_folder, args.timeout)
    fuzzer.fuzz_corpus(corpus, args.times if args.times >= 0 else 'inf')

def main():
    main_parser = argparse.ArgumentParser(description='Fuzzer')
    main_parser.add_argument('-p', '--program', type=str, required=True,
                        help='path to target program.')
    main_parser.add_argument('-t', '--type', type=str, required=True,
                        help='type of the fuzzer, can be mutation or generation')
    main_parser.add_argument('-c', '--crash_folder', type=str, default='./crash',
                        help='path to save the files that caused the program to crash.')
    main_parser.add_argument('--times', type=int, default=-1,
                        help='number of iterations of fuzzing. -1 for infinty.')
    main_parser.add_argument('--timeout', type=int, default=5,
                        help='stop the target program after a certain amount of seconds if program don\'t halt.')
    main_parser.add_argument('-i', '--input', type=str, required=True,
                        help='path to corpus directory or template format file.')

    args = main_parser.parse_args()

    if not os.path.isfile(args.program) or not os.access(args.program, os.X_OK):
        print('File doesn\'t exist or isn\'t executable')
        return -1

    if not os.path.isdir(args.crash_folder):
        os.mkdir(args.crash_folder)

    if args.type == 'mutation' or args.type == 'mut':
        main_mutate(args)
    elif args.type == 'generation' or args.type == 'gen':
        main_generate(args)
    else:
        print(f'fuzzing type {args.type} not supported')
        return -1


if __name__ == "__main__":
    main()
