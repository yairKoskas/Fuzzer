import random

from file_generator.generator_parser import GeneratorParser
from pathlib import Path
import runner
import os


class GeneratorFuzzer:
    """
        program - program to fuzz
        template_format - path to template format file
        crash_folder - folder to save the files that casued crash
        """

    def __init__(self, program: Path, template_format: Path, crash_folder: Path):
        self.template_format = template_format
        self.program = program
        self.crashes = 0
        self.crash_folder = crash_folder
        self.runner = runner.Runner()

        self.parser = GeneratorParser(self.template_format)

    '''
    fuzz a specific file
    returns - True if fuzzed file caused crash and False otherwise
    '''

    def fuzz_file(self, file: str):
        if not os.path.isfile(file):
            raise Exception('File doesn\'t exist')

        with open(file, 'rb') as f:
            content = f.read()

        # temporary file to save fuzzed files at
        temp_file = './temp'

        with open(temp_file, 'wb') as f:
            temp = b''
            for gen in self.parser.generators:
                if random.randint(0, 2):
                    temp += self.parser.generators[gen].valid_value()
                else:
                    temp += self.parser.generators[gen].invalid_value()
            f.write(temp)

        retcode = self.runner.run(self.program, [temp_file])

        # copy content to the crashed folder if neccesary
        if retcode != 0 and retcode != 1:
            with open(temp_file, 'rb') as f1:
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
        for _ in range(times):
            for file in os.listdir(corpus):

                file = os.fsdecode(file)
                path = os.path.join(corpus, file)
                if os.path.isfile(path):
                    self.fuzz_file(path)