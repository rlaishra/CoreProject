import networkx as nx
import random

class MissingData(object):
    """docstring for MissingData."""
    def __init__(self):
        super(MissingData, self).__init__()

    def removeRandomNodes(self, graph, num):
        remove = random.sample([n for n in graph.nodes()], num)
        graph.remove_nodes_from(remove)
        return graph

    def removeRandomEdges(self, graph, num):
        remove = random.sample([e for e in graph.edges()], num)
        graph.remove_edges_from(remove)
        return graph
