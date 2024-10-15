from collections import deque


"""
    Solves the problem defined in the statement for adj an adjacency list of the dispersion dynamics of rumors in LLN
        adj is a list of length equal to the number of kots
        adj[i] gives a list of kots touched by i with direct edges (0-based indexing)

    You are free to change the code below and to not use the precompleted part. The code is based on the high-level description at https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm
    You can also define other sub-functions or import other datastructures from the collections library
"""

def countSources(scc, adj):
    N = max(scc.values()) +1
    n = len(adj)
    flux = [1]*N
    for i in range(n):
        for j in adj[i]:
            if scc[i] != scc[j]:
                flux[scc[j]] = 0
    sources = sum(flux)
    return sources

"""
    Transpose the adjacency matrix
        Construct a new adjacency matrix by inverting all the edges: (x->y) becomes (y->x) 
"""
def transpose(adj):
    t = []
    N = len(adj)
    for i in range(N):
        t.append([])
    for i in range(N):
        for j in adj[i]:
            t[j].append(i)
    return t


def solve(adj):
    # adjacency of the graph and its transpose
    adj_out = adj
    adj_in = transpose(adj_out)

    # number of nodes
    N = len(adj_in)

    # is a node already visited?
    visited = [False]*N
    # list of node to process in the second step
    L = []
    # queue of nodes to process with their associated status (i,False/True) i is the node index and True/False describes if we are appending the node to L or not when processing it
    q = deque()

    ### loop on every node and launch a visit of its descendants
    for x in range(N):
        
        if not visited[x]:
            q.append((x,False))

        while q:
            x,to_append = q.pop()

            if to_append:
                L.append(x)
            
            if not visited[x]:
                visited[x] = True
                q.append((x,True))

                for n in adj_out[x]:
                    if not visited[n]:
                        q.append((n,False))

    ### reverse the list to obtain the post-order
    L.reverse()


    ### find the strongly connected components
    
    visited = [False]*N
    scc = {}
    comp = 0

    for x in L:
        if not visited[x]:
            number_of_node = 0
            q.append((x,False))

            while q:
                x, to_append = q.pop()

                if to_append:
                    scc[x] = comp
                    number_of_node += 1
                
                if not visited[x]:
                    visited[x] = True
                    q.append((x,True))

                    for n in adj_in[x]:
                        if not visited[n]:
                            q.append((n,False))

            if number_of_node:
                comp += 1
                
    return countSources(scc, adj_out)



