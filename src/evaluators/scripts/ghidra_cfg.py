from ghidra.util.graph import DirectedGraph
from ghidra.util.graph import Edge
from ghidra.util.graph import Vertex

def get_address(offset):
    return currentProgram.getAddressFactory().getDefaultAddressSpace().getAddress(offset)


def get_cfg(program):
        # convert to rpc call to ghidra API
	digraph = DirectedGraph()
	listing = currentProgram.getListing()
	fm = currentProgram.getFunctionManager()

	funcs = fm.getFunctions(True)
	for func in funcs: 
		digraph.add(Vertex(func))
	
		entryPoint = func.getEntryPoint()
		instructions = listing.getInstructions(entryPoint, True)
		for instruction in instructions:
			addr = instruction.get_address()
			oper = instruction.getMnemonicString()
			if oper == "CALL":
				flows = instruction.getFlows()
				if len(flows) == 1:
					target_addr = "0x{}".format(flows[0])
					digraph.add(Edge(Vertex(func), Vertex(fm.getFunctionAt(getAddress(target_addr)))))

	edges = digraph.edgeIterator()
	return digraph
