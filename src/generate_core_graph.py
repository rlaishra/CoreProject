"""
Generate a random graph where all the nodes belong to the k shell
but have different degrees

That is all the nodes belong to the k core but not (k+i) core
"""

from __future__ import division, print_function

import networkx as nx
import sys
import random
import numpy as np

def baseGraph(n, k):
    """
    Generates a graph where all the nodes are in the k shell
    and there is the minimum number of edges
    """
    graph = nx.Graph()
    graph.add_nodes_from(range(0,n))

    while True:
        core = nx.core_number(graph)
        max_core = max(core.values())
        min_core = min(core.values())

        #print('Core Numbers \t Min:{} \t Max: {}'.format(min_core, max_core))

        if min_core == k:
            break
        elif min_core < max_core:
            un = [u for u in core if core[u] == min_core]
            vn = [u for u in core if core[u] == max_core]
            u = random.choice(un)
            v = random.choice(vn)
            # print('Min Nodes: \t', un)
            # print('Max Nodes: \t', vn)
            # u = random.choice([u for u in core if core[u] == min_core])
            # v = random.choice([u for u in core if core[u] == max_core])
            # print('Edge: \t {},{}'.format(u,v))
            edge = (u,v)
        else:
            edge = random.sample(core.keys(),2)

        graph.add_edge(edge[0], edge[1])

    return graph

def increaseAvgDegree(graph, a, d):
    """
    Add edges to graph to increase the average degree
    without increasing the core number of any node
    """
    core = nx.core_number(graph)
    while True:
        degrees = nx.degrees(graph)
        mdegree = np.mean(degrees)

        if mdegree >= d:
            break
        else:
            u = sorted(degrees, key=degrees.get)[0]
            neighbors = set(graph.neighbors(u))
            c = [x for x in graph.nodes() if x not in neighbors and x != u]
            c = [x for x in c if len(neighbors.intersection(nx.neighbors(x)))\
             < core_number(u) ]


if __name__ == '__main__':
    n = int(sys.argv[1])
    k = int(sys.argv[2])
    d = float(sys.argv[3])

    graph = baseGraph(n,k)

    print(nx.core_number(graph))
    print(nx.to_numpy_matrix(graph))
