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

def addEdges(graph, ne, edges, vedges):
    cn =nx.core_number(graph)
    core = np.array(cn.values())

    i = 0
    for e in edges:
        graph.add_edge(e[0],e[1])
        tcore = nx.core_number(graph)
        tcore = np.array(tcore.values())

        diff = np.linalg.norm(core - tcore)

        if diff > 0:
            graph.remove_edge(e[0], e[1])
        else:
            i += 1
            print(i, e[0], e[1], cn[e[0]], cn[e[1]], vedges[e])

        if i >= en:
            break
    return graph

def possibleEdges(graph):
    core = nx.core_number(graph)
    nodes = graph.nodes()

    vedges = {}
    while len(nodes) > 2:
        u = nodes.pop()
        for v in nodes:
            vedges[(u,v)] = core[u]*core[v]
    edges = sorted(vedges, key=vedges.get, reverse=True)

    return edges, vedges

if __name__ == '__main__':
    fname = sys.argv[1]
    sname = sys.argv[2]

    nedges = xrange(0,11)
    count = graph.number_of_edges()/100

    graph = readGraph(fname)
    edges, vedges = possibleEdges(graphs)

    for e in nedges:
        tsname = sname + str(e) + '.csv'
        ne = int(count * e)

        graph = readGraph(fname)
        print(nx.info(graph))
        graph = addEdges(graph, ne, edges, vedges)
        print(nx.info(graph))
        nx.write_edgelist(graph, tsname)
