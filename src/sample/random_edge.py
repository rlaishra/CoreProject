import networkx as nx
import random

class RandomEdge(object):
    """docstring for RandomEdge."""
    def __init__(self, graph):
        super(RandomEdge, self).__init__()
        self.graph = graph
        self.edges = set(list(self.graph.edges()))

    def getSample(self, graph, num):
        edges = list(graph.edges())
        self.edges = self.edges.difference(edges)
        edges = random.sample(self.edges, num)
        graph.add_edges_from(edges)
        return graph
