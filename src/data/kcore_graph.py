"""
Add peaks or remove peaks from the k-core histogram of a base graph and save the results
"""
from __future__ import division, print_function
import networkx as nx
import numpy as np
from decomposition import kcore
from experiments import kcore as kexp
from experiments import histogram
from noise import missing
import csv

class KCoreGraph(object):
    """docstring for KCoreGraph."""
    def __init__(self, base, sname, adjacency=False):
        super(KCoreGraph, self).__init__()
        self.sname = sname
        if adjacency:
            self.graph = nx.read_adjlist(base)
        else:
            self.graph = nx.read_edgelist(base)
        self.cnumber = kcore.KCore(self.graph).coreNumber()
        self.top = [1, 0.2, 0.1]
        self.ori_graph = self.graph.copy()

    def resetGraph(self):
        self.graph = self.ori_graph.copy()

    def removeNodes(self, nodes, count, save=False):
        remove = np.random.choice(nodes, size=count, replace=False)
        nodes = [n for n in nodes if n not in remove]
        self.graph.remove_nodes_from(remove)
        if save:
            nx.write_edgelist(self.graph, self.sname, delimiter='\t', data=False)
        return self.graph, nodes

    def addPeak(self, k, nodes, edges, count, lst, ext_nodes):
        nodes += ['n_'+str(i) for i in xrange(lst,lst+count)]
        ni_count = np.random.randint(k,high=k+10,size=len(nodes))
        no_count = np.random.randint(0,high=10,size=len(nodes))
        for i, n in enumerate(nodes):
            candidates = list(nodes).remove(n)
            ni = np.random.choice(candidates, size=ni_count[i], replace=False)
            no = np.random.choice(ext_nodes, size=no_count[i], replace=False)
            edges += [(n, u) for u in ni]
            edges += [(n, u) for u in no]

        graph = self.graph.copy()
        graph.add_edge_from(edges)
        return graph, nodes, edges, lst + count

    def saveData(self, data, t='removed'):
        with open(self.sname, 'w') as f:
            writer = csv.writer(f,delimiter=',')
            header = [t+'_core', 'frac'] + ['error_'+str(i) for i in self.top] + \
             ['std_'+str(i*10) for i in self.top] +\
             ['core', 'count', 'degree', 'clustering', 'components']
            writer.writerow(header)
            for d in data:
                writer.writerow(d)

    def runExpRemoveNodes(self, k):
        """
        Remove fractions of top k nodes
        """
        step = 1
        fracs = [i for i in xrange(0, 20, step)]
        data = []
        for _c in xrange(0,5):
            self.resetGraph()
            nodes = [n for n in self.cnumber if self.cnumber[n] == k]
            count = int(len(nodes)*step/100)
            for f in fracs:
                print(_c, f, len(nodes), count)
                self.graph, nodes = self.removeNodes(nodes, count)

                kcore_exp = kexp.KCoreExperiment(self.graph, None, ftype='object', top=self.top)
                _, _, _, error = kcore_exp.expRandomMissingEdges(5, 10, 50)

                exp = histogram.KCoreHistogram(self.graph, None, ftype='object')
                cdata = exp.runExperiment()
                data += [[k,f] + [e[0] for e in error] + [e[1] for e in error] + d for d in cdata]

        self.saveData(data)

    def runExpAddPeak(self, k):
        """
        Add a peak at given core number
        """
        step = 1
        fracs = [i for i in xrange(0, 10, step)]
        data = []
        ext_nodes = [n for n in self.cnumber if self.cnumber[n] == k]
        count = int(len(ext_nodes)*step/100)
        for _c in xrange(0,5):
            lst = 0
            edges = []
            in_nodes = []
            for f in fracs:
                print(_c, f, len(nodes), count)
                graph, in_nodes, edges, lst = self.addPeak(k, in_nodes, edges, count, lst, ext_nodes)

                kcore_exp = kexp.KCoreExperiment(graph, None, ftype='object', top=self.top)
                _, _, _, error = kcore_exp.expRandomMissingEdges(5, 10, 50)

                exp = histogram.KCoreHistogram(graph, None, ftype='object')
                cdata = exp.runExperiment()
                data += [[k,f] + [e[0] for e in error] + [e[1] for e in error] + d for d in cdata]

        self.saveData(data, t='added')
