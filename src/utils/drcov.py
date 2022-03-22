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


def parse_coverage(coverage, modules):
    bbs = set()
    for bb_list in coverage:
        start = int(bb_list[0], 16)
        end   = int(bb_list[1], 16)
        module = None
        for m in modules:
            if start > m["base"] and end < m["end"]:
                module = m
                break
        if module == None:
            #log.debug("block @0x%x does not belong to any module!" % start)
            continue
        bbs.add(Block(start, end, module))
    return bbs