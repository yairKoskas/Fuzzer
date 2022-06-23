## code coverage logic
Each time the fuzzed program is running, 
a certain number of code blocks are reached via the input given to it.
<br>In order to maximize the code coverage (the number of blocks the program reaches), 
we counted the number of blocks reached in each run of the program.
<br>We used frida Stalker in order to get the coverage information.
This is done by attaching the stalker to all of the threads, 
and sending each block the program enters to the fuzzer's handler.
<br>This way, we get all of the blocks touched in a single run.
<br>So now, Each time a certain input we mutated cause a change in the block coverage 
(like reaching a block we never reached before), We add the mutated input to the corpus, in order to reach a maximum number of blocks.
<br>In conclusion, the flow looks like this:
1. Run the program and attach the frida Stalker to it (works with both the generation based fuzzing and the mutation based fuzzing)
2. Wait for the program to end
3. The program crashed? Add the new input to the corpus
4. The program reached a new block? Add the new input to the corpus
5. Repeat
