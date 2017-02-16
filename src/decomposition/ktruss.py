from __future__ import division, print_function
import networkx as nx
import sys

class KTruss(object):
    """K-truss decomposition"""
    def __init__(self, graph):
        super(KTruss, self).__init__()
        self.graph = graph

    def decomposition(self, k = 2):
        complete = False
        while not complete:
            complete = True
            for n in self.graph.nodes():
                if nx.triangles(self.graph,n) < k:
                    self.graph.remove_node(n)
                    complete = False
        return self.graph

if __name__ == '__main__':
    fname = sys.argv[1]
    sname = sys.argv[2]
    k = int(sys.argv[3])

    graph = nx.read_edgelist(fname)
    print(graph.number_of_nodes(), graph.number_of_edges())

    truss = KTruss(graph)
    graph = truss.decomposition(k)
    print(graph.number_of_nodes(), graph.number_of_edges())

    nx.write_edgelist(graph, sname, data=False)
