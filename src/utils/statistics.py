from __future__ import division, print_function
import numpy as np
import networkx as nx
import sys

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

    def monotonic(self, x):
        change = 0

        # Normalize
        x_min = min(x)
        x_max = max(x) - x_min
        x = [(v - x_min)/x_max for v in x]

        for i in xrange(1, len(x)-1):
            u = x[i-1]
            v = x[i]
            w = x[i+1]
            if (u > v and v < w) or (u < v and v > w):
                m = (u + w)/2
                c = np.abs(m - v)
                change += c*c
        return change/len(x)

    def increasing(self, x):
        change = 0
        count = 0
        # Normalize
        #x_min = min(x)
        #x_max = max(x) - x_min
        #x = [(v - x_min)/x_max for v in x]

        for i in xrange(1, len(x)):
            u = x[i-1]
            v = x[i]
            if u < v:
                change += (v - u)
                count += 1
        return change

if __name__ == '__main__':
    stats = Statistics()
    l1 = [i for i in xrange(0,100)] + [20000]*100
    l2 = [i for i in xrange(0,10)] + [3,5,9,0,10]

    change = stats.monotonic(l2)
    print(change)
