from __future__ import division, print_function
import networkx as nx
import sys

class KCore(object):
    """K-core decomposition"""
    def __init__(self, graph):
        super(KCore, self).__init__()
        self.graph = graph

    def decomposition(self, k = 2):
        """
        Returns the subgraph with the nodes whose core number are greater
        than k
        """
        complete = False
        while not complete:
            complete = True
            degree = self.graph.degree()
            for n in degree:
                if degree[n] < k:
                    self.graph.remove_node(n)
                    complete = False
        return self.graph

    def coreNumber(self):
        cnumber = {n:0 for n in self.graph.nodes()}
        k = 1
        while self.graph.number_of_nodes() > 0:
            self.graph = self.decomposition(k)
            for n in self.graph.nodes():
                cnumber[n] = k
            k += 1
        return cnumber

if __name__ == '__main__':
    fname = sys.argv[1]
    sname = sys.argv[2]
    k = int(sys.argv[3])

    graph = nx.read_edgelist(fname)
    print(graph.number_of_nodes(), graph.number_of_edges())

    kcore = KCore(graph)
    graph = kcore.decomposition(k)
    print(graph.number_of_nodes(), graph.number_of_edges())

    nx.write_edgelist(graph, sname, data=False)
