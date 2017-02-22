from __future__ import division, print_function
import numpy as np
import networkx as nx

class Statistics(object):
    """docstring for Statistics."""
    def __init__(self):
        super(Statistics, self).__init__()

    def degreeDistribution(self, graph):
        degree = nx.degree(graph)
        dist = {}
        for n in degree:
            if degree[n] not in dist:
                dist[degree[n]] = 0
            dist[degree[n]] += 1
        total = graph.number_of_nodes()
        dist = {n: dist[n]/total for n in dist}
        return dist
