from fuzzers import mutation_fuzzer
import mutators.bitflip_mutator as bitflip_mutator
import mutators.bitinsert_mutator as bitinsert_mutator
import mutators.combine_mutator as combine_mutator

import sys
import os

def main():
    if len(sys.argv) < 4:
        print('Usage: python3 main.py [path_to_executable] [corpus] [crash_folder] [times]')
        return -1

    
    program, corpus, crash_folder = sys.argv[1], sys.argv[2], sys.argv[3]

    if len(sys.argv) > 4:
        times = int(sys.argv[4])
    else:
        times = 1


    if not os.path.isfile(program) or not os.access(program, os.X_OK):
        print('File doesn\'t exist or isn\'t executable')
        return -1

    if not os.path.isdir(crash_folder):
        os.mkdir(crash_folder)

    
    mutator = combine_mutator.CombinetMutator([bitinsert_mutator.BitInsertMutator(), bitflip_mutator.BitFlippingMutator()])

    fuzzer = mutation_fuzzer.MutationFuzzer(program, mutator, crash_folder)
    fuzzer.fuzz_corpus(corpus, times)

if __name__ == "__main__":
    main()