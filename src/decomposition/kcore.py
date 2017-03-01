from __future__ import division, print_function
import networkx as nx
import sys

class KCore(object):
    """K-core decomposition"""
    def __init__(self, graph):
        super(KCore, self).__init__()
        self.graph = graph.copy()

    def decomposition(self, graph=None, k = 2):
        """
        Returns the subgraph with the nodes whose core number are greater
        than k
        """
        if graph is None:
            graph = self.graph
        complete = False
        while not complete:
            degree = graph.degree()
            remove = [n for n in degree if degree[n] < k]
            complete = len(remove) < 1
            graph.remove_nodes_from(remove)
            print('k: {} \t Nodes removed: {} \t Nodes left: {}'.format(k,\
             len(remove), graph.number_of_nodes()))
        return graph

    def coreNumber(self, graph=None):
        if graph is None:
            graph = self.graph
        else:
            graph = graph.copy()

        cnumber = {}
        k = 1
        while graph.number_of_nodes() > 0:
            graph = self.decomposition(graph, k)
            for n in graph.nodes():
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
