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

    def __init__(self, program: Path, template_format: Path, crash_folder: Path, timeout: int, extension: str, args: list):
        self.timeout = timeout
        self.template_format = template_format
        self.program = program
        self.crashes = 0
        self.crash_folder = crash_folder
        self.runner = runner.Runner()

        self.parser = GeneratorParser(self.template_format)
        self.file_creator = self.parser.get_creator()

        # temporary file to save fuzzed files at
        self.temp_file = f'./temp.{extension}'

        # args to the target program
        self.args = [arg if arg != '<fuzzed>' else self.temp_file for arg in args]
    '''
    fuzz a specific file
    returns - True if fuzzed file caused crash and False otherwise
    '''

    def fuzz_once(self):
        
        with open(self.temp_file, 'wb') as f:
            f.write(self.file_creator.create_file(random.choice([0,1,2,4,8,16,32])))

        retcode = self.runner.run(self.program, self.args, self.timeout)

        # copy content to the crashed folder if neccesary
        if retcode != 0 and retcode != 1:
            with open(self.temp_file, 'rb') as f1:
                crash_path = os.path.join(self.crash_folder, str(self.crashes))
                self.crashes += 1
                with open(crash_path, 'wb') as f2:
                    f2.write(f1.read())

            return True

        return False


    '''
    fuzz multiple times

    parameters:
    times - number of times to generate file
    '''

    def fuzz_multiple(self, times: int):
        if times == 'inf':
            while True:
                self.fuzz_once()

        else:
            for _ in range(times):
                self.fuzz_once()