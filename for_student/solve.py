from collections import deque


"""
    Solves the problem defined in the statement for adj an adjacency list of the dispersion dynamics of rumors in LLN
        adj is a list of length equal to the number of kots
        adj[i] gives a list of kots touched by i with direct edges (0-based indexing)

    You are free to change the code below and to not use the precompleted part. The code is based on the high-level description at https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm
    You can also define other sub-functions or import other datastructures from the collections library
"""
def solve(adj):
    scc = tarjan(adj)
    N = len(scc)
    influx = [0]*N
    for i in range(len(adj)):
        for j in adj[i]:
            if scc[i] != scc[j]:
                influx[scc[j]] += 1
                
    source = sum(1 for i in influx if i == 0)
    return source


class Node:
    def __init__(self, id, next):
        self.id = id
        self.index = None
        self.lowlink = None
        self.onStack = False
        self.next = next
                    
def tarjan(adj):
    # Number of nodes
    N = len(adj)
    
    # Initialization
    nodes = [Node(i, adj[i]) for i in range(N)]
    index = [0]
    stack = []
    SCC_list = [0]
    dico = {}
    
    for n in nodes:
        if n.index == None:
            strongconnect(n, nodes, index, stack, SCC_list, dico)
    
    return dico
            
def strongconnect(n, nodes, index, stack, SCC_list, dico):
    n.index = index[0]
    n.lowlink = index[0]
    index[0] += 1
    stack.append(n)
    n.onStack = True
    
    for i in n.next:
        if nodes[i].index == None:
            strongconnect(nodes[i], nodes, index, stack, SCC_list, dico)
            n.lowlink = min(n.lowlink, nodes[i].lowlink)
        elif nodes[i].onStack:
            n.lowlink = min(n.lowlink, nodes[i].index)
    
    if n.lowlink == n.index:
        while True:
            w = stack.pop()
            w.onStack = False
            dico[w.id] = SCC_list[0]
            if w.id == n.id:
                break
        SCC_list[0] += 1
    