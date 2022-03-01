# Grey-box fuzzing
Grey-box fuzzing is the middleground between white-box fuzzing and black-box fuzzing. Unlike black-box fuzzing, it uses knowledge about the program, but not full program analysis like white-box fuzzing.

## Code coverage
The most common form of grey-box fuzzing is based around maximizing code coverage.<br>
There are a lot of different algorithms to improve code coverage but most of them are based around maintaining a test corpus (or sometimes a single test sample), mutating it, and evolving the corpus to achieve maximum code coverage.<br>
Code coverage can be measured in different criteria, for example: How much statements of the program has been executed (Statement coverage)? How much edges in the control-flow graph been executed (edge-based)?<br>
Most fuzzers achieves the code coverage information by either injecting to the program during compilation time pieces of code that tells us which paths have been chosen, or by running the program using a debugger, virtual machine or different instrumeation tools (the second way usually results in a slower running time compared to the first but can be used also without the source code).

## example - AFL algorithm in a nutshell
AFL measures code coverge by measuring How much edges in the control-flow graph been executed and how mich times, it doing it by injecting pieces of code at the start of each block that marks the edge the program is executing (by checking the current and previous block).<br>
AFL starts with a test corpus provided by the user, mutating it, and each time a new mutated test exeuting a new edge, this test is added to the corpus.<br>
AFL also uses some other methods to improve the chance of revealing new edges:
- removing tests: once in a while, AFL run an algorithm in order to minimize the size of the corpus, while maintaining the same amount of overall coverage.
- priority unique tests: AFL doesn't waste the same amount of time fuzzing each file in the corpus. instead it prioritizes fuzzing tests which executes paths that are executed less by other tests in the corpus.