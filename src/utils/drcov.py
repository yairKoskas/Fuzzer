import struct


class Module:
    base: int
    end: int

    def __init__(self, base, end):
        self.base = base
        self.end = end
        self.length = end - base


class Block:
    start: int
    end: int
    module: Module

    def __init__(self, start: int, end: int, module: Module):
        self.start = start
        self.end = end
        self.module = module

    def __hash__(self):
        return int(str(self.start) + str(self.end) + str(self.module))


def parse_coverage(coverage):
    blocks_str = b''.join(coverage)
    bb_blocks = [blocks_str[i:i+8] for i in range(0, len(blocks_str), 8)]
    blocks = set()
    for block in bb_blocks:
        start, size, mod_id = struct.unpack("<IHH", block)
        blocks.add(Block(start, start + size, mod_id))
    return blocks

