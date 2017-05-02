from __future__ import division, print_function
#from sample import random_edge
from pprint import pprint
import networkx as nx
import numpy as np
import random
import sys
#from utils import statistics

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

class KCore(object):
    """docstring for KCore."""
    def __init__(self, fname, sname):
        super(KCore, self).__init__()
        self.fname = fname
        self.sname = sname

    def readGraph(self):
        self.graph = nx.read_edgelist(self.fname)

    def correlation(self, ocnumber, ncnumber):
        x1 = []
        x2 = []

        for n in ncnumber:
            x1.append(ncnumber[n])
            x2.append(ocnumber[n])

        # kendall tau
        cor = self.kendalltau(x1,x2)
        return cor

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

    def runExperimentEdges(self, iter):
        self.readGraph()
        end = int(self.graph.number_of_edges()*0.95)
        step = int(self.graph.number_of_edges()*0.01)

        ori_cnumber = nx.core_number(self.graph)

        for _ in xrange(0, iter):
            graph = nx.Graph()
            sample = RandomEdge(self.graph)

            for i in xrange(1, 95):
                graph = sample.getSample(graph, step)
                cnumber = nx.core_number(graph)
                cor = self.correlation(ori_cnumber, cnumber)
                print(i, cor)

if __name__ == '__main__':
    fname = sys.argv[1]
    sname = sys.argv[2]

    kcore = KCore(fname, sname)
    kcore.runExperimentEdges(1)
