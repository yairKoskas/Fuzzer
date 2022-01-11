# Fuzzer

currently works ony on programs that gets a file path as a first argument.

## usage

### mutation fuzzing

python3 src/main_mutate.py [path_to_executable] [corpus] [crash_folder] [times]

- path_to_executable - path to program to run.
- corpus - path to directory with all the files to fuzz.
- crash_folder - path to save the files that caused the .program to crash.
- times - times to fuzz the whole curpos.

### generation fuzzing

python3 src/main_mutate.py [path_to_executable] [temaplate_file] [crash_folder] [times]

- path_to_executable - path to program to run.
- corpus - path to directory with all the files to fuzz.
- temaplate_file - path to template file with the file format specifications.
- times - times to fuzz the whole curpos.

