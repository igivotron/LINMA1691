from collections import deque


class Edge:
    def __init__(self, u, v, capa, weight, residual=None):
        self.u = u
        self.v = v
        self.capa = capa  # capacity that there is left to the edge
        self.weight = weight  # weight of the edge
        self.residual = residual  # corresponding edge in the residual graph


def create_graph(capacities, costs, green_sources: dict, gas_centrals: dict, consumers: dict):

    # TODO
    N = len(capacities)
    graph = [[] for _ in range(N)]

    def add_edge(u, v, cost, capa):
        edge = Edge(u, v, capa, cost)
        graph[u].append(edge)
    
    for i in range(N):
        for j in range(N):
            if capacities[i][j] > 0:
                add_edge(i, j, capacities[i][j], costs[i][j])

    s = 0
    t = 0
    

    return s, t, graph


def get_residual(graph):

    # TODO
    for u in range(len(graph)):
        for edge in graph[u]:
            v = edge.v
            edge.residual = Edge(v, u, 0, -edge.weight, edge)
            graph[v].append(edge.residual)

    graph_residual = graph
    return graph_residual


def min_cost_max_flow(s, t, graph_residual):
    # TODO
    N = len(graph_residual)

    def BellmanFord():
        dist = [float('inf') for _ in range(N)]
        path = [[]for _ in range(N)]
        dist[s] = 0
        path[s] = []
        inqueue = [False for _ in range(N)]
        q = deque([s])
        inqueue[s] = True
        while q:
            u = q.popleft()
            inqueue[u] = False
            for edge in graph_residual[u]:
                if edge.capa > 0 and dist[edge.v] > dist[u] + edge.weight:
                    dist[edge.v] = dist[u] + edge.weight
                    path[edge.v] = path[u] + [edge]
                    if not inqueue[edge.v]:
                        inqueue[edge.v] = True
                        q.append(edge.v)

        if path[t] == []:
            return None
        return path[t]

    maximum_flow = 0
    minimum_cost = 0
    while True:
        path = BellmanFord()
        if path is None:
            break
        min_capa = min(edge.capa for edge in path)
        for edge in path:
            edge.capa -= min_capa
        maximum_flow += min_capa
        minimum_cost += min_capa * sum(edge.weight for edge in path)
    return maximum_flow, minimum_cost
