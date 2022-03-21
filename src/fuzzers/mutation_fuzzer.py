import runner
import os

from mutators.mutator import Mutator


class MutationFuzzer:
    """
    program - path to program to fuzz
    mutator - mutator to mutate the data with
    crash_folder - folder to save the files that casued crash
    timeout - timeout for running the program in seconds
    extension - extension of the files to fuzz
    args - arguments to the program
    non_crashing_codes - list of return codes that are not considered as a crash
    """
    def __init__(self, program: str, mutator : Mutator, crash_folder: str, timeout: int, extension: str, args: list,non_crashing_codes: list):
        self.timeout = timeout
        self.mutator = mutator
        self.program = program
        self.crashes = 0
        self.crash_folder = crash_folder
        self.runner = runner.Runner()
        # 0 and 1 never considered as a crash
        self.non_crashing_codes = [0,1] + non_crashing_codes

        # temporary file to save fuzzed files at
        self.temp_file = f'./temp.{extension}'

        # args to the target program
        self.args = [arg if arg != '<fuzzed>' else self.temp_file for arg in args]

    '''
    fuzz a specific file
    returns - True if fuzzed file caused crash and False otherwise
    '''
    def fuzz_file(self, file: str):
        if not os.path.isfile(file):
            raise Exception('File doesn\'t exist')

        with open(file, 'rb') as f:
            content = f.read()

        with open(self.temp_file, 'wb') as f:
            f.write(self.mutator.mutate(content))

        retcode = self.runner.run(self.program, self.args, self.timeout, self.saved_states)

        # copy content to the crashed folder if neccesary
        if retcode not in self.non_crashing_codes:
            print(f'found crash with exit code {retcode}')
            with open(self.temp_file, 'rb') as f1:
                crash_path = os.path.join(self.crash_folder, str(self.crashes))
                self.crashes += 1
                with open(crash_path, 'wb') as f2:
                    f2.write(f1.read())

            return True

        return False

    '''
    fuzz a whole corpus

    parameters:
    corpus - path to folder where the corpus files are
    times - number of times to fuzz the corpus
    '''
    def fuzz_corpus(self, corpus: str, times: int):
        if times == 'inf':
            while True:
                # catch when user terminates by cntrl+c
                try:
                    for file in os.listdir(corpus):

                        file = os.fsdecode(file)
                        path = os.path.join(corpus, file)
                        if os.path.isfile(path):
                            self.fuzz_file(path)
                except KeyboardInterrupt:
                    break

        else:
            for _ in range(times):
                for file in os.listdir(corpus):

                    file = os.fsdecode(file)
                    path = os.path.join(corpus, file)
                    if os.path.isfile(path):
                        self.fuzz_file(path)
