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

    def kendalltau(self, l1, l2):
        # Variation of kendall tau that do not discard ties
        if not(len(l1) == len(l2)):
            return False
        n = len(l1)
        s = 0
        for i in xrange(0, n):
            u1 = l1[i]
            u2 = l2[i]
            for j in xrange(i+1, n):
                v1 = l1[j]
                v2 = l2[j]
                # Concordant
                if (u1 == v1 and u2 == v2) or (u1 < v1 and u2 < v2) or (u1 > v1 and u2 > v2):
                    s += 1
                else:
                    s -= 1
        cor = s/(n*(n-1)*0.5)
        return cor

if __name__ == '__main__':
    stats = Statistics()
    l1 = [i for i in xrange(0,100)] + [20000]*100
    l2 = [i for i in xrange(0,100,)] + [10000]*50 + [30000]*50

    cor = stats.kendallTau(l1,l2)
    print(cor)
