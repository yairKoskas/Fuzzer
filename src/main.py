import mutation_fuzzer
import bitflip_mutator
import sys
import os

def main():
    if len(sys.argv) < 4:
        print('Usage: python3 main.py [path_to_executable] [corpus] [crash_folder] [ratio] [times]')
        return -1

    
    program, corpus, crash_folder = sys.argv[1], sys.argv[2], sys.argv[3]

    if len(sys.argv) > 4:
        ratio = float(sys.argv[4])
    else:
        ratio = 0.01

    if len(sys.argv) > 5:
        times = int(sys.argv[5])
    else:
        times = 1


    if not os.path.isfile(program) or not os.access(program, os.X_OK):
        print('File doesn\'t exist or isn\'t executable')
        return -1

    if not os.path.isdir(crash_folder):
        os.mkdir(crash_folder)
    mutator = bitflip_mutator.BitFlippingMutator(ratio)
    fuzzer = mutation_fuzzer.MutationFuzzer(program, mutator, crash_folder)
    fuzzer.fuzz_corpus(corpus, times)

if __name__ == "__main__":
    main()