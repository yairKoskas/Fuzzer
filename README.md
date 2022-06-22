# Fuzzer

A fuzzer that targets exeutable programs that gets as input binary file formats (e.g bmp,png,jpeg...).

## requirements
- python version 3.8+
- The packages in the requirements.txt file.

## targets
The target have to be a single-process executable file that accept a file as one of its arguments. Note that the program identify a crash by checking the exit code (a crash is considered to be an exit code different from 0 or 1).

## usage

To run the fuzzer, run the file `src/main.py` using python with the following arguments.<br>
Required arguments:
- `--program` (or `-p`): Path to the fuzzing target.
- `--type` (or `-t`): Type of fuzzing, valid options are `mutation` (or `mut`) and `generation` (or `gen`) for details see [types of fuzzing](#types-of-fuzzing).
- `--input` (or `-i`): Different for each fuzzing type.
<br><br>
Optional arguments:
- `--crash_folder` (or `-c`): path to save the files that caused the program to crash (default is `./crash`).
- `--times`: number of iterations of fuzzing, if set to -1, fuzzing will not stop automatically and have to be stopped manually (default is -1).
- `--timeout`: stop the target program after a certain amount of seconds if program don't halt, used to prevent the fuzzer from wasting too much time on one file (default is 5).
- `--extension` (or `-e`): extention of the fuzzed file format (default is `txt`).
- `--args` (or `-a`): list of arguments to pass to the target program. `<fuzzed>` will be replaced by the fuzzed file. (default is `<fuzzed>`, i.e a program that gets the fuzzed file as the first argument).
- `--non_crashing_codes`: list of exit codes (except 0 and 1) that fuzzer should not consider as a crash. 

During the fuzzing, each file that cause the program to crash will be written to the folder specified in `crash_folder`, if the files where generated from a template, then also a report of the mutaion locations will be added to same directory.<br>
In order to stop the fuzzing, press cnrl+c.


## types of fuzzing
### generation-based smart fuzzing

Generation fuzzing genreates files from scratch using a user-defined template, and then mutating the files generated in a "smart" way using the knowledge about the structure of the file.

In order to use this mode, the user have to define the structure of the fuzzed format in a xml type format ( for specification of the format see [here](templateFormat/specification.md)).

In the templateFormat directory there are examples of templates for the for the inage formats: BMP, JPEG, PNG.

The argumant `--input` contains the path to template file.

You can generate non-mutated files in order to test your template using the `main_test_template` script (the result will be written into `output.<extention>`)

### mutation-based fuzzing

Mutation fuzzing get a corpus of files in the format the target program gets, it takes the files from the corpus and make random mutations to them.

The argumant `--input` contains the path to a corpus with sample files of the required format.