from __future__ import division, print_function
import numpy as np
import networkx as nx
import sys
import csv
from pprint import pprint

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
        slope = -1 if np.polyfit(range(0, len(x)), x, 1)[0] < 0 else 1
        print(slope)
        change = 0

        # Normalize
        if min(x) == max(x):
            return -1
        x_min = min(x)
        x_max = max(x) - x_min
        x = [(v - x_min)/x_max for v in x]

        for i in xrange(1, len(x)):
            u = x[i-1]
            v = x[i]

            if slope*(v-u) < 0 and u != 0:
                #print(u,v)
                c = np.abs((u-v)/u)
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

    """
    l1 = [i for i in xrange(0,100)] + [20000]*100
    l2 = [i for i in xrange(0,10)] + [3,5,9,0,10]
    l3 = range(1000,100,-1)
    l4 = range(10, 100)
    l5 = range(0,10) + [50] + range(11,20)

    change = stats.monotonic(l3)
    print(change)

    change = stats.monotonic(l4)
    print(change)

    change = stats.monotonic(l2)
    print(change)

    change = stats.monotonic(l1)
    print(change)

    change = stats.monotonic(l5)
    print(change)
    """

    fname = sys.argv[1]
    cdata = []
    with open(fname, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        for r in reader:
            cdata.append(r)

    data = [[],[],[]]
    for d in cdata[1:]:
        data[0].append(float(d[1]))
        data[1].append(float(d[3]))
        data[2].append(float(d[5]))

    change1 = stats.monotonic(data[0])
    change2 = stats.monotonic(data[1])
    change3 = stats.monotonic(data[2])

    print(change1, change2, change3)
