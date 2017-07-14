from __future__ import division, print_function
import networkx as nx
import sys
import random

def readGraph(fname):
    graph = nx.read_edgelist(fname)
    return graph

def degeneracyCore(graph):
    cn = nx.core_number(graph)
    val = sorted(list(set([cn[n] for n in cn])), reverse=True)
    deg = [n for n in cn if cn[n] in val[:5]]
    return deg

def newEdges(graph, nodes):
    cedges = graph.edges()
    nedges = []

    while len(nedges) < 0.02 * len(cedges):
        e = random.sample(nodes, 2)
        if e not in cedges:
            nedges.append((e[0], e[1]))
    return nedges

def addEdges(graph, edges):
    graph.add_edges_from(edges)
    return graph

def saveGraph(graph, sname):
    nx.write_edgelist(graph, sname, data=False)

if __name__ == '__main__':
    fname = sys.argv[1]
    sname = sys.argv[2]

    graph = readGraph(fname)
    deg = degeneracyCore(graph)
    edges = newEdges(graph, deg)
    graph = addEdges(graph, edges)
    saveGraph(graph, sname)
