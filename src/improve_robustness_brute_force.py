"""
Add edges between the high core number nodes to improve the robustness
"""

from __future__ import division, print_function
import networkx as nx
import numpy as np
import sys
import random

def readGraph(fname):
    graph = nx.read_edgelist(fname)
    return graph

def addEdges(graph, e):
    cn =nx.core_number(graph)
    nodes = sorted(cn, key=cn.get, reverse=True)[:int(graph.number_of_nodes()*0.1)]
    core = np.array(cn.values())

    i = 0

    print('Number of candidates: {}'.format(len(nodes)))

    while len(nodes) > 2 and i < e:
        u = nodes.pop(0)
        c = [v for v in nodes if v not in graph.neighbors(u)]
        for v in nodes:
            graph.add_edge(u,v)
            tcore = nx.core_number(graph)
            tcore = np.array(tcore.values())

            diff = np.linalg.norm(core - tcore)

            if diff > 0:
                graph.remove_edge(u,v)
            else:
                i += 1
                print(i, u, v, cn[u], cn[v])
            if i >= e:
                break
    return graph

if __name__ == '__main__':
    fname = sys.argv[1]
    sname = sys.argv[2]

    nedges = xrange(0,11)

    for e in nedges:
        tsname = sname + e + '.csv'
        graph = readGraph(fname)
        print(nx.info(graph))
        graph = addEdges(graph, e)
        print(nx.info(graph))
        nx.write_edgelist(graph, sname)
