# overview of different tools that can achieve code coverage for fuzzing without source code

## qemu
AFL supports binary only instrumentation using a slightly modified version of the qemu emulator, which injects the AFL instrumentation every time a new block is read by qemu.

links:<br>
- AFL qemu-mode: https://github.com/google/AFL/tree/master/qemu_mode

## frida
Frida is a dynamic instrumentation tool that is used by a lot of fuzzers. Some fuzzers use frida to activate an event when it encounters a new block (usually good for achieving basic block coverage), and some actually instrument the code by injecting some code to each block during runtime.
Frida also have python binding.

links:<br>
- frida: https://frida.re/
- AFL++ frida-mode: https://github.com/AFLplusplus/AFLplusplus/tree/stable/frida_mode
- frizzer: https://github.com/demantz/frizzer
- fpicker: https://github.com/ttdennis/fpicker/

## dynamoRio
Another dynamic instrumentation tool. beside its API dynamoRio also have prebuilt code coverage tool (https://dynamorio.org/page_drcov.html), but it supports only basic block coverage.

links:
- dynamoRio: https://dynamorio.org/
- winafl: https://github.com/googleprojectzero/winafl
- afl-dynamorio: https://github.com/vanhauser-thc/afl-dynamorio

## intel pintool
Similar to frida, but works only on intel processors and considered slower. used by aflpin project (https://github.com/mothran/aflpin).

## retorwrite
Retrowrite can statically write afl-like instrumentation. The adventage is much faster execution time than dynamic instrumentation, but it requires a lot of unreasonable assumptions on the binary (symbol table, PIE, and doesnt use C++ exceptions).

links:
- retorwrite: https://github.com/HexHive/retrowrite