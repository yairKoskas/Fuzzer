import uuid

from evaluators.coverage_evaluator import CoverageEvaluator
import runner
import os


class CoverageFuzzer:
    """
    program - program to fuzz
    mutator - mutator to mutate the text with
    crash_folder - folder to save the files that casued crash
    """

    def __init__(self, program: str, mutator, crash_folder: str, timeout: int, extension: str, args: list, coverage_type: str=None):
        self.timeout = timeout
        self.mutator = mutator
        self.program = program
        self.crashes = 0
        self.crash_folder = crash_folder
        self.saved_states = set()
        if coverage_type:
            self.runner = runner.CoverageRunner(coverage_type, program)
        else:
            self.runner = runner.Runner()

        # temporary file to save fuzzed files at
        self.temp_file = f'./temp.{extension}'

        # args to the target program
        self.args = [arg if arg != '<fuzzed>' else self.temp_file for arg in args]

    '''
    fuzz a specific file
    returns - True if fuzzed file caused crash and False otherwise
    '''
    def fuzz_file(self, file: str, corpus: str=None):
        if not os.path.isfile(file):
            raise Exception('File doesn\'t exist')

        with open(file, 'rb') as f:
            content = f.read()

        with open(self.temp_file, 'wb') as f:
            f.write(self.mutator.mutate(content))

        # todo: make wrapper object around self.runner.run return value so this will be less ugly
        if type(self.runner) == runner.CoverageRunner:
            retcode, power_plan = self.runner.run(self.program, self.args, self.timeout, self.saved_states, corpus)
        else:
            self.runner.run(self.program, self.args, self.timeout)
        # copy content to the crashed folder if neccesary
        if retcode != 0 and retcode != 1:
            with open(self.temp_file, 'rb') as f1:
                # todo, make file have powerplan value (add json field?)
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
        new_corpus = f'/tmp/temporary_corpus_{uuid.uuid4()}'
        os.system(f'cp -r {os.path.abspath(corpus)} {new_corpus}')
        if times == 'inf':
            while True:
                for file in os.listdir(new_corpus):

                    file = os.fsdecode(file)
                    path = os.path.join(new_corpus, file)
                    if os.path.isfile(path):
                        self.fuzz_file(path, new_corpus)

        else:
            for _ in range(times):
                for file in os.listdir(new_corpus):

                    file = os.fsdecode(file)
                    path = os.path.join(new_corpus, file)
                    if os.path.isfile(path):
                        self.fuzz_file(path, new_corpus)
            os.rmdir(f'{new_corpus}')
