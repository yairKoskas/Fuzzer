# Fuzzer

currently works ony on programs that gets a file path as a first argument.

## usage

python3 src/main.py [path_to_executable] [corpus] [crash_folder] [ratio] [times]

- path_to_executable - path to program to run.
- corpus - path to directory with all the files to fuzz.
- crash_folder - path to save the files that caused the .program to crash.
- ratio - proportion of bits that are changing while mutating the files.
- times - times to fuzz the whole curpos.

