from __future__ import division, print_function
from decomposition import kcore
from noise import missing
import networkx as nx
import sys
import random
import csv
import numpy as np
from scipy import stats
import os.path
import pickle

class KCoreExperiment(object):
    """docstring for KCoreExperiment."""
    def __init__(self, fname, sname, adjacency=False):
        super(KCoreExperiment, self).__init__()
        self.fname = fname
        self.sname = sname
        self.adj = adjacency
        if not self.adj:
            self.graph = nx.read_edgelist(self.fname)
        else:
            self.graph = nx.read_adjlist(self.fname)
        self.kcore = kcore.KCore(self.graph)
        self.number_of_nodes = self.graph.number_of_nodes()
        self.number_of_edges = self.graph.number_of_edges()


    def readCache(self):
        fname = self.sname + '_core_pickle.pickle'
        if os.path.isfile(fname):
            with open(fname, 'r') as f:
                print('Found cache: ' + fname)
                data = pickle.load(f)
                self.graph = data['graph']
                return data['cnumber']
        return None

    def writeCache(self, cnumber):
        fname = self.sname + '_core_pickle.pickle'
        f = open(fname, 'w')
        data = {'graph': self.graph.copy(), 'cnumber': cnumber}
        pickle.dump(data, f)

    def readData(self):
        if not self.adj:
            self.graph = nx.read_edgelist(self.fname)
        else:
            self.graph = nx.read_adjlist(self.fname)

    def coreNumber(self, can_cache=False):
        if can_cache:
            cnumber = self.readCache()
            if cnumber is None:
                cnumber = self.kcore.coreNumber(self.graph)
                self.writeCache(cnumber)
            return cnumber
        else:
            return self.kcore.coreNumber(self.graph)

    def runExperimentNode(self, step = 5, end = 50):
        cnumber = {0:self.coreNumber(can_cache=True)}

        noise = missing.MissingData()
        size = int(self.graph.number_of_nodes()*step*0.01)

        for i in xrange(1, int(end/step)):
            self.graph = noise.removeRandomNodes(self.graph, size)
            cnumber[i*step] = self.coreNumber()
        return cnumber

    def runExperimentEdges(self, step = 5, end = 50):
        cnumber = {0:self.coreNumber(can_cache=True)}

        noise = missing.MissingData()
        size = int(self.graph.number_of_edges()*step*0.01)

        for i in xrange(1, int(end/step)):
            self.graph = noise.removeRandomEdges(self.graph, size)
            cnumber[i*step] = self.coreNumber()

        return cnumber

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
        fname = self.sname + '_core_' + iden + '.csv'
        with open(fname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['missing', 'correlation', 'pvalue', 'correlation_20', 'pvalue_20', 'correlation_10', 'pvalue_10', 'correlation_5', 'pvalue_5'])
            for d in data:
                writer.writerow(d)

    def saveHistogram(self, data, iden):
        fname = self.sname + '_core_histogram_' + iden + '.csv'
        with open(fname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for d in data:
                writer.writerow(d)

    def runExperiment(self, iter=10, step = 5, end = 50):
        data = []
        histogram = {x:{} for x in xrange(0, end, step)}

        for _ in xrange(0,iter):
            self.readData()
            cnumber = self.runExperimentNode(step, end)
            all_nodes = set([n for n in cnumber[0]])
            for i in cnumber:
                t_data = []

                common_nodes = list(all_nodes.intersection([n for n in cnumber[i]]))
                x1 = [cnumber[0][n] for n in common_nodes]
                x2 = [cnumber[i][n] for n in common_nodes]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [i, tau, p_value]

                common_nodes = self.selectTopN(cnumber[0], common_nodes, self.number_of_nodes * 0.2)
                x1 = [cnumber[0][n] for n in common_nodes]
                x2 = [cnumber[i][n] for n in common_nodes]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [tau, p_value]
                hist, sep = np.histogram(x2, bins=max(x2)-min(x2))
                for s in sep[:-1]:
                    if s not in histogram[i]:
                        histogram[i][s] = []

                for k, v in enumerate(hist):
                    histogram[i][sep[k]].append(v)

                common_nodes = self.selectTopN(cnumber[0], common_nodes, self.number_of_nodes * 0.1)
                x1 = [cnumber[0][n] for n in common_nodes]
                x2 = [cnumber[i][n] for n in common_nodes]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [tau, p_value]

                common_nodes = self.selectTopN(cnumber[0], common_nodes, self.number_of_nodes * 0.05)
                x1 = [cnumber[0][n] for n in common_nodes]
                x2 = [cnumber[i][n] for n in common_nodes]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [tau, p_value]

                data.append(t_data)
                print(t_data)
        hdata = [['core_number'] + ['missing_'+str(i) for i in histogram]]
        for k in xrange(1, int(max([max(histogram[h].keys()) for h in histogram]))):
            t_hdata = [k]
            for i in histogram:
                if k in histogram[i]:
                    t_hdata.append(np.mean(histogram[i][k]))
                else:
                    t_hdata.append(0)
            hdata.append(t_hdata)

        self.saveHistogram(hdata, 'nodes')
        self.saveResults(data, 'nodes')

        data = []
        histogram = {x:{} for x in xrange(0, end, step)}
        for _ in xrange(0,iter):
            self.readData()
            cnumber = self.runExperimentEdges(step, end)
            all_nodes = set([n for n in cnumber[0]])
            for i in cnumber:
                t_data = []
                common_nodes = list(all_nodes.intersection([n for n in cnumber[i]]))
                x1 = [cnumber[0][n] for n in common_nodes]
                x2 = [cnumber[i][n] for n in common_nodes]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [i, tau, p_value]

                common_nodes = self.selectTopN(cnumber[0], common_nodes, self.number_of_nodes * 0.2)
                x1 = [cnumber[0][n] for n in common_nodes]
                x2 = [cnumber[i][n] for n in common_nodes]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [tau, p_value]
                hist, sep = np.histogram(x2, bins=max(x2)-min(x2))
                for s in sep[:-1]:
                    if s not in histogram[i]:
                        histogram[i][s] = []

                for k, v in enumerate(hist):
                    histogram[i][sep[k]].append(v)

                common_nodes = self.selectTopN(cnumber[0], common_nodes, self.number_of_nodes * 0.1)
                x1 = [cnumber[0][n] for n in common_nodes]
                x2 = [cnumber[i][n] for n in common_nodes]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [tau, p_value]

                common_nodes= self.selectTopN(cnumber[0], common_nodes, self.number_of_nodes * 0.05)
                x1 = [cnumber[0][n] for n in common_nodes]
                x2 = [cnumber[i][n] for n in common_nodes]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [tau, p_value]

                data.append(t_data)
                print(t_data)

        hdata = [['core_number'] + ['missing_'+str(i) for i in histogram]]
        #print([histogram[k].keys() for h in histogram])
        for k in xrange(1, int(max([max(histogram[h].keys()) for h in histogram]))):
            t_hdata = [k]
            for i in histogram:
                if k in histogram[i]:
                    t_hdata.append(np.mean(histogram[i][k]))
                else:
                    t_hdata.append(0)
            hdata.append(t_hdata)

        self.saveHistogram(hdata, 'edges')
        self.saveResults(data, 'edges')

"""
def kcore(graph, k = 2):
    cgraph = graph.copy()
    complete = False
    while not complete:
        complete = True
        degree = cgraph.degree()
        for n in degree:
            if degree[n] < k:
                cgraph.remove_node(n)
                complete = False
    return cgraph

def coreNumber(graph):
    pass

def removeNodes(graph, missing):
    cgraph = graph.copy()
    count = int(graph.number_of_nodes() * missing * 0.01)
    remove = random.sample([n for n in graph.nodes()], count)
    cgraph.remove_nodes_from(remove)
    return cgraph

def removeEdges(graph, missing):
    cgraph = graph.copy()
    count = int(graph.number_of_edges() * missing * 0.01)
    remove = random.sample([n for n in graph.edges()], count)
    cgraph.remove_edges_from(remove)
    return cgraph

def saveResults(data, sname, mtype):
    fname = sname + '_' + mtype + '.csv'
    with open(fname, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        for d in data:
            writer.writerow(d)
"""

if __name__ == '__main__':
    fname = sys.argv[1]
    sname = sys.argv[2]
    mtype = sys.argv[3]

    graph_ori = nx.read_edgelist(fname)

    core_nodes = {}
    header = ['missing']

    for k in xrange(2,11,2):
        kcore_1 = kcore(graph_ori, k)
        core_nodes[k] = set([n for n in kcore_1.nodes()])
        header += ['core'+str(k)]

    data = [header]

    for i in xrange(0,10):
        for missing in xrange(0,51,5):
            t_data = [missing]
            for k in xrange(2,11,2):
                print(i, missing, k)
                nodes_1 = core_nodes[k]
                if mtype == 'n':
                    graph_missing = removeNodes(graph_ori, missing)
                elif mtype == 'e':
                    graph_missing = removeEdges(graph_ori, missing)
                kcore_2 = kcore(graph_missing, k)
                nodes_2 = [n for n in kcore_2.nodes()]

                found = len(nodes_1.intersection(nodes_2)) / len(nodes_1)

                t_data.append(found)
            data.append(t_data)

    saveResults(data, sname, mtype)
