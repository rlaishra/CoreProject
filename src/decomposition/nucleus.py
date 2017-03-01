from __future__ import division, print_function
import networkx as nx
import sys

class NucleusDecomposition(object):
    """docstring for NucleusDecomposition."""
    def __init__(self):
        super(NucleusDecomposition, self).__init__()

    def findKClique(self, graph, k, cliques=None):
        pass

    def decomposition(self, graph, r, s):
        if r < 3 or not(r < s):
            return None

        edges = set(graph.edges())
        r_clique = set()
        s_clique = set()
        t_clique = edges.copy()

        for i in xrange(3, s):
            temp = []
            itemp = t_clique.copy()
            for x in t_clique:
                itemp.remove(x)
                for y in itemp:
                    if len(set(x).intersection(y)) >= (i-2):
                        z = list(set(x).union(y).difference(set(x).intersection(y)))      # The nodes that are not shared
                        if (z[0],z[1]) in edges or (z[1], z[0]) in edges:
                            temp.append(list(set(x).union(y)))
                            print(temp)
            temp = list(map(list,set(map(frozenset, temp))))
            print(temp)

if __name__ == '__main__':
    fname = sys.argv[1]

    nc = NucleusDecomposition()
    graph = nx.read_edgelist(fname)
    nc.decomposition(graph, 3, 4)
