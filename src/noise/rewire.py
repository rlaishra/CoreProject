"""
Rewire edges while preserving the degree distribution
"""

from __future__ import division
import networkx as nx
import random
import sys
import numpy as np

class RewireEdges(object):
    def __init__(self):
        super(RewireEdges, self).__init__()

    def nextNode(self, graph, current = None):
        if current is not None:
            neighbors = set(graph.neighbors(current))
            for _ in xrange(0, graph.number_of_nodes()):
                u = random.choice(graph.nodes())
                if u not in neighbors and len(graph.neighbors(u)) > 0:
                    return u

        # If none of the candidates are suitable, select any from graph
        return random.choice(graph.nodes())

    def rewire(self, graph, num):
        # Select an ranom node with degree greater than 0
        remove = random.sample(graph.edges(), num)
        nodes = [n for e in remove for n in e]
        edges = []
        while len(nodes) > 0:
            u = random.choice(nodes)
            nodes.remove(u)
            v = random.choice(nodes)
            nodes.remove(v)
            edges.append((u,v))
        graph.add_edges_from(edges)
        return graph

if __name__ == '__main__':
    fname = sys.argv[1]
    graph = nx.read_edgelist(fname)
    print(np.histogram([x for _,x in graph.degree().iteritems()]))
    re = RewireEdges()
    re.rewire(graph, 100)
    print(np.histogram([x for _,x in graph.degree().iteritems()]))
