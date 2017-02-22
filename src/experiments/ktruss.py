from __future__ import division, print_function
from decomposition import ktruss
from noise import missing
import networkx as nx
import sys
import random
import csv
import numpy as np
from scipy import stats
import pickle
import os.path

class KTrussExperiment(object):
    """docstring for KCoreExperiment."""
    def __init__(self, fname, sname, adjacency=False):
        super(KTrussExperiment, self).__init__()
        self.fname = fname
        self.sname = sname
        self.adj = adjacency
        if not self.adj:
            self.graph = nx.read_edgelist(self.fname)
        else:
            self.graph = nx.read_adjlist(self.fname)
        self.ktruss = ktruss.KTruss(self.graph)
        self.number_of_nodes = self.graph.number_of_nodes()
        self.number_of_edges = self.graph.number_of_edges()

    def readCache(self):
        fname = self.sname + '_truss_pickle.pickle'
        if os.path.isfile(fname):
            with open(fname, 'r') as f:
                print('Found cache: ' + fname)
                data = pickle.load(f)
                self.graph = data['graph']
                return data['tnumber']
        return None

    def writeCache(self, tnumber):
        fname = self.sname + '_truss_pickle.pickle'
        f = open(fname, 'w')
        data = {'graph': self.graph.copy(), 'tnumber': tnumber}
        pickle.dump(data, f)


    def readData(self):
        if not self.adj:
            self.graph = nx.read_edgelist(self.fname)
        else:
            self.graph = nx.read_adjlist(self.fname)

    def trussNumber(self, can_cache=False):
        if can_cache:
            tnumber = self.readCache()
            if tnumber is None:
                tnumber = self.ktruss.trussNumber(self.graph)
                self.writeCache(tnumber)
            return tnumber
        else:
            return self.ktruss.trussNumber(self.graph)

    def runExperimentNode(self, step = 5, end = 50):
        tnumber = {0:self.trussNumber(can_cache=True)}

        noise = missing.MissingData()
        size = int(self.graph.number_of_nodes()*step*0.01)

        for i in xrange(1, int(end/step)):
            print('Missing Nodes: ',i * size)
            self.graph = noise.removeRandomNodes(self.graph, size)
            tnumber[i*step] = self.trussNumber()

        return tnumber

    def runExperimentEdges(self, step = 5, end = 50):
        tnumber = {0:self.trussNumber(can_cache=True)}

        noise = missing.MissingData()
        size = int(self.graph.number_of_edges()*step*0.01)

        for i in xrange(1, int(end/step)):
            print('Missing Edges: ',i * size)
            self.graph = noise.removeRandomEdges(self.graph, size)
            tnumber[i*step] = self.trussNumber()

        return tnumber

    def selectTopN(self, nvalues, keys, n):
        """
        Select the top n keys with the highest values

        Sometime returns more than n if there are ties
        """
        values = set([nvalues[k] for k in keys])
        topn = []

        while len(topn) < n and len(values) > 0:
            topval = max(values)
            for k in keys:
                if nvalues[k] == topval:
                    topn.append(k)
            values.remove(topval)

        return topn

    def saveResults(self, data, iden):
        fname = self.sname + '_truss_' + iden + '.csv'
        with open(fname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['missing', 'correlation', 'pvalue', 'correlation_20', 'pvalue_20', 'correlation_10', 'pvalue_10', 'correlation_5', 'pvalue_5'])
            for d in data:
                writer.writerow(d)

    def runExperiment(self, iter=10, step = 5, end = 50):
        data = []
        for _ in xrange(0,iter):
            self.readData()
            tnumber = self.runExperimentNode(step, end)
            all_edges = set([e for e in tnumber[0]])
            for i in tnumber:
                t_data = []
                common_edges = list(all_edges.intersection([e for e in tnumber[i]]))
                x1 = [tnumber[0][n] for n in common_edges]
                x2 = [tnumber[i][n] for n in common_edges]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [i, tau, p_value]

                common_edges = self.selectTopN(tnumber[0], common_edges, self.number_of_edges * 0.2)
                x1 = [tnumber[0][n] for n in common_edges]
                x2 = [tnumber[i][n] for n in common_edges]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [tau, p_value]

                common_edges = self.selectTopN(tnumber[0], common_edges, self.number_of_edges * 0.1)
                x1 = [tnumber[0][n] for n in common_edges]
                x2 = [tnumber[i][n] for n in common_edges]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [tau, p_value]

                common_edges = self.selectTopN(tnumber[0], common_edges, self.number_of_edges * 0.05)
                x1 = [tnumber[0][n] for n in common_edges]
                x2 = [tnumber[i][n] for n in common_edges]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [tau, p_value]

                data.append(t_data)
                print(t_data)
        self.saveResults(data, 'nodes')

        data = []
        for _ in xrange(0,iter):
            self.readData()
            tnumber = self.runExperimentEdges(step, end)
            all_edges = set([e for e in tnumber[0]])
            for i in tnumber:
                t_data = []
                common_edges = list(all_edges.intersection([e for e in tnumber[i]]))
                x1 = [tnumber[0][n] for n in common_edges]
                x2 = [tnumber[i][n] for n in common_edges]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [i, tau, p_value]

                common_edges = self.selectTopN(tnumber[0], common_edges, self.number_of_edges * 0.2)
                x1 = [tnumber[0][n] for n in common_edges]
                x2 = [tnumber[i][n] for n in common_edges]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [tau, p_value]

                common_edges = self.selectTopN(tnumber[0], common_edges, self.number_of_edges * 0.1)
                x1 = [tnumber[0][n] for n in common_edges]
                x2 = [tnumber[i][n] for n in common_edges]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [tau, p_value]

                common_edges = self.selectTopN(tnumber[0], common_edges, self.number_of_edges * 0.05)
                x1 = [tnumber[0][n] for n in common_edges]
                x2 = [tnumber[i][n] for n in common_edges]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [tau, p_value]

                data.append(t_data)
                print(t_data)
        self.saveResults(data, 'edges')

if __name__ == '__main__':
    """
    fname = sys.argv[1]
    sname = sys.argv[2]
    mtype = sys.argv[3]

    graph_ori = nx.read_edgelist(fname)

    core_nodes = {}
    header = ['missing']

    for k in xrange(2,11,2):
        ktruss_1 = ktruss(graph_ori, k)
        core_nodes[k] = set([n for n in ktruss_1.nodes()])
        header += ['truss'+str(k)]

    data = [header]

    for i in xrange(0,10):
        for missing in xrange(0,51,5):
            t_data = [missing]
            for k in xrange(2,11,2):
                print(i,missing, k)
                nodes_1 = core_nodes[k]
                if mtype == 'n':
                    graph_missing = removeNodes(graph_ori, missing)
                elif mtype == 'e':
                    graph_missing = removeEdges(graph_ori, missing)
                ktruss_2 = ktruss(graph_missing, k)
                nodes_2 = [n for n in ktruss_2.nodes()]

                found = len(nodes_1.intersection(nodes_2)) / len(nodes_1)

                t_data.append(found)
            data.append(t_data)

    saveResults(data, sname, mtype)
    """
