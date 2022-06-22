import random

from file_generator.generator_parser import GeneratorParser
from file_generator import mutation_report

from pathlib import Path
import runner
import os


class GeneratorFuzzer:
    
    """
    program - path to program to fuzz
    template_format - path to template format file
    crash_folder - folder to save the files that casued crash
    timeout - timeout for running the program in seconds
    extension - extension of the files to fuzz
    args - arguments to the program
    non_crashing_codes - list of return codes that are not considered as a crash
    """
    def __init__(self, program: Path, template_format: Path, crash_folder: Path, timeout: int, extension: str, args: list, non_crashing_codes: list):
        self.timeout = timeout
        self.template_format = template_format
        self.program = program
        self.crashes = 0
        self.crash_folder = crash_folder
        self.runner = runner.Runner()
        self.extension = extension
        # 0 and 1 never considered as a crash
        self.non_crashing_codes = [0,1] + non_crashing_codes

        self.parser = GeneratorParser(self.template_format)
        self.file_creator = self.parser.get_creator()

        # temporary file to save fuzzed files at
        self.temp_file = f'./temp.{extension}'

        # args to the target program
        self.args = [arg if arg != '<fuzzed>' else self.temp_file for arg in args]

    '''
    save the crash report contains the file content after mutation and the mutation report
    '''
    def crash_report(self, crash_file: Path, reports : list):
        with open(crash_file, 'rb') as f1:
            # write crash file
            crash_path = os.path.join(self.crash_folder, f'{str(self.crashes)}.{self.extension}')
            with open(crash_path, 'wb') as f2:
                f2.write(f1.read())

            # write crash report
            report_path = os.path.join(self.crash_folder, f'report_{str(self.crashes)}.txt')
            with open(report_path, 'w') as f2:
                f2.write('\n'.join([str(report) for report in reports]))

            self.crashes += 1

    '''
    fuzz a specific file
    returns - True if fuzzed file caused crash and False otherwise
    '''
    def fuzz_once(self):
        
        with open(self.temp_file, 'wb') as f:
            mutation_amount = random.choice([0,1,2,4,8,16,32])
            reports, content = self.file_creator.create_file(mutation_amount)
            f.write(content)

        retcode = self.runner.run(self.program, self.args, self.timeout)

        # copy content to the crashed folder if neccesary
        if retcode not in self.non_crashing_codes:
            self.crash_report(self.temp_file, reports)
            print(f'found crash with exit code {retcode}')

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
                # catch when user terminates by cntrl+c
                try:
                    self.fuzz_once()
                except KeyboardInterrupt:
                    break

        else:
            for _ in range(times):
                self.fuzz_once()