"""
Add edges between the high core number nodes to improve the robustness
"""

from __future__ import division, print_function
import networkx as nx
import numpy as np
import sys
import random
import time

def readGraph(fname):
    graph = nx.read_edgelist(fname)
    graph.remove_edges_from(graph.selfloop_edges())
    return graph

def addEdges(graph, ne, edges, vedges, id=None):
    cn =nx.core_number(graph)
    core = np.array(cn.values())

    i = 0

    while len(edges) > 0:
        e = edges.pop(0)

        graph.add_edge(e[0],e[1])
        tcore = nx.core_number(graph)
        tcore = np.array(tcore.values())

        diff = np.linalg.norm(core - tcore)

        if diff > 0:
            graph.remove_edge(e[0], e[1])
        else:
            i += 1
            #print(id, i, e[0], e[1], cn[e[0]], cn[e[1]], vedges[e])

        if i >= ne:
            break
    return graph, edges


def possibleEdges(graph):
    core = nx.core_number(graph)
    nodes = set(graph.nodes())

    vedges = {}
    while len(nodes) > 2:
        u = nodes.pop()
        n = nodes.difference(graph.neighbors(u))
        for v in n:
            vedges[(u,v)] = core[u]*core[v]
    edges = sorted(vedges, key=vedges.get, reverse=True)

    return edges, vedges

if __name__ == '__main__':
    fname = sys.argv[1]
    sname = sys.argv[2]

    t0 = time.time()
    t = []

    nedges = xrange(1,11)

    graph = readGraph(fname)
    edges, vedges = possibleEdges(graph)
    count = graph.number_of_edges()/100

    tsname = sname + '0.csv'
    nx.write_edgelist(graph, tsname)

    print('Number of possible edges: {}'.format(len(edges)))

    ne = int(count)

    for e in nedges:
        tsname = sname + str(e) + '.csv'
        #graph = readGraph(fname)
        print(nx.info(graph))
        graph, edges = addEdges(graph, ne, edges, vedges, e)
        print(nx.info(graph))
        nx.write_edgelist(graph, tsname)
        
        t1 = time.time()
        t.append(t1-t0)
        print('Time: {}'.format(t[-1]))
    print('time',t)
