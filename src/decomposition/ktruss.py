from __future__ import division, print_function
import networkx as nx
import sys

class KTruss(object):
    """K-truss decomposition"""
    def __init__(self, graph):
        super(KTruss, self).__init__()
        self.graph = graph.copy()

    def decomposition(self, graph=None, k = 3):
        """
        Returns the subgraph with the nodes whose core number are greater
        than k
        """
        if graph is None:
            graph = self.graph
        complete = False
        while not complete:
            complete = True
            remove = []
            # Nodes with degree less than k-2 cannot have edges in k-truss
            degree = graph.degree()
            node_remove = []
            for n in degree:
                if degree[n] < k - 2:
                    node_remove.append(n)
            graph.remove_nodes_from(node_remove)

            # Truss number of remaining
            for e in graph.edges():
                triangles = len(list(nx.common_neighbors(graph, e[0], e[1])))
                if triangles < k - 2:
                    remove.append(e)
                    complete = False
            graph.remove_edges_from(remove)
            print('k: {} \t Edges removed: {} \t Edges left: {}'.format(k,\
             len(remove), graph.number_of_edges()))
        return graph

    def trussNumber(self, graph=None):
        if graph is None:
            graph = self.graph
        else:
            graph = graph.copy()

        tnumber = {}
        k = 3

        while graph.number_of_edges() > 0:
            graph = self.decomposition(graph, k)
            for e in graph.edges():
                tnumber[e] = k
            k += 1
        return tnumber

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
