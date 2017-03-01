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
from noise import rewire
import operator

class KTrussExperiment(object):
    """docstring for KCoreExperiment."""
    def __init__(self, fname, sname, adjacency=False, mode='111'):
        super(KTrussExperiment, self).__init__()
        self.fname = fname
        self.sname = sname
        self.adj = adjacency
        """
        1st digit for random node deletion,
        2nd digit for random edge deletion,
        3rd digit for random rewiring preserving degree dist
        """
        self.mode = mode
        if not self.adj:
            self.graph = nx.read_edgelist(self.fname)
        else:
            self.graph = nx.read_adjlist(self.fname)
        self.ktruss = ktruss.KTruss(self.graph)
        self.number_of_nodes = self.graph.number_of_nodes()
        self.number_of_edges = self.graph.number_of_edges()
        self.top = [1, 0.2, 0.1, 0.05]                  # Percentage of top nodes consider

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
            self.graph = noise.removeRandomNodes(self.graph, size)
            tnumber[i*step] = self.trussNumber()

        return tnumber

    def runExperimentEdges(self, step = 5, end = 50, mode = 0):
        """
        mode
            0   random edge delete
            1   random edge rewiring
        """
        tnumber = {0:self.trussNumber(can_cache=True)}
        size = int(self.graph.number_of_edges()*step*0.01)

        if mode == 0:
            noise = missing.MissingData()
        elif mode == 1:
            noise = rewire.RewireEdges()

        for i in xrange(1, int(end/step)):
            if mode == 0:
                self.graph = noise.removeRandomEdges(self.graph, size)
            elif mode == 1:
                self.graph = noise.rewire(self.graph, size)
            tnumber[i*step] = self.trussNumber()

        return tnumber

    def selectTopN(self, nvalues, keys, n):
        """
        Select the top n keys with the highest values
        """
        data = [(k, nvalues[k]) for k in keys]
        data = sorted(data, key=operator.itemgetter(1), reverse=True)[:n]
        topn = [x[0] for x in data]
        return topn

    def resultsMean(self, data):
        cdata = {}
        for d in data:
            if d[0] not in cdata:
                cdata[d[0]] = [[] for _ in self.top]
            for i in xrange(0, len(self.top)):
                cdata[d[0]][i].append(d[2*i + 1])
        mdata = []
        for i in cdata:
            d = [i]
            for l in cdata[i]:
                d += [np.mean(l), np.std(l)]
            mdata.append(d)
        return mdata

    def saveMeanResults(self, data, iden):
        data = self.resultsMean(data)
        fname = self.sname + '_truss_mean_' + iden + '.csv'
        with open(fname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            header = ['change']
            for p in self.top:
                v = str(int(p*100))
                header += ['correlation_'+v, 'std_'+v]
            writer.writerow(header)
            for d in data:
                writer.writerow(d)

    def saveResults(self, data, iden):
        fname = self.sname + '_truss_' + iden + '.csv'
        with open(fname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            header = ['change']
            for p in self.top:
                v = str(int(p*100))
                header += ['correlation_'+v, 'pvalue_'+v]
            writer.writerow(header)
            for d in data:
                writer.writerow(d)

    def saveHistogram(self, data, iden):
        fname = self.sname + '_truss_histogram_' + iden + '.csv'
        with open(fname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for d in data:
                writer.writerow(d)

    def processHistogram(self, histogram, identifier):
        if histogram is None:
            histogram = {p: {x:{} for x in xrange(0, end, step)} for p in self.top}
        for p in histogram:
            hist = histogram[p]
            hdata = [['truss_number'] + ['change_'+str(i) for i in hist]]
            for k in xrange(1, int(max([max(hist[h].keys()) for h in hist]))):
                t_hdata = [k]
                for i in hist:
                    if k in hist[i]:
                        t_hdata.append(np.mean(hist[i][k]))
                    else:
                        t_hdata.append(0)
                hdata.append(t_hdata)
            self.saveHistogram(hdata, identifier+'_top_'+str(int(p*100)))

    def getHistogram(self, x2, histogram, i, p):
        if max(x2) > min(x2):
            hist, sep = np.histogram(x2, bins=max(x2)-min(x2))
            for s in sep[:-1]:
                if s not in histogram[p][i]:
                    histogram[p][i][s] = []

            for k, v in enumerate(hist):
                histogram[p][i][sep[k]].append(v)
        else:
            histogram[p][i][x2[0]] = [len(x2)]

    def newHistogram(self, step, end):
        return {p: {x:{} for x in xrange(0, end, step)} for p in self.top}

    def expRandomMissingNodes(self, iter, step, end):
        data = []
        histogram = self.newHistogram(step, end)
        for _ in xrange(0,iter):
            self.readData()
            tnumber = self.runExperimentNode(step, end)
            all_edges = set([e for e in tnumber[0]])
            for i in tnumber:
                t_data = [i]
                common_edges = list(all_edges.intersection([e for e in tnumber[i]]))
                for p in self.top:
                    common_nodes = self.selectTopN(tnumber[0], common_edges,\
                     self.number_of_edges * p)
                    x1 = [tnumber[0][n] for n in common_edges]
                    x2 = [tnumber[i][n] for n in common_edges]
                    tau, p_value = stats.kendalltau(x1, x2)
                    t_data += [tau, p_value]
                    self.getHistogram(x2, histogram, i, p)

                data.append(t_data)
                print(t_data)

        self.saveMeanResults(data, 'nodes_delete_random')
        self.processHistogram(histogram, 'nodes_delete_random')
        self.saveResults(data, 'nodes_delete_random')


    def expRandomMissingEdges(self, iter, step, end):
        data = []
        histogram = self.newHistogram(step, end)
        for _ in xrange(0,iter):
            self.readData()
            tnumber = self.runExperimentEdges(step, end)
            all_edges = set([e for e in tnumber[0]])
            for i in tnumber:
                t_data = [i]
                common_edges = list(all_edges.intersection([e for e in tnumber[i]]))
                for p in self.top:
                    common_edges = self.selectTopN(tnumber[0], common_edges,\
                     int(self.number_of_edges * p))
                    x1 = [tnumber[0][n] for n in common_edges]
                    x2 = [tnumber[i][n] for n in common_edges]
                    tau, p_value = stats.kendalltau(x1, x2)
                    t_data += [tau, p_value]
                    self.getHistogram(x2, histogram, i, p)

                data.append(t_data)
                print(t_data)

        self.saveMeanResults(data, 'edges_delete_random')
        self.processHistogram(histogram, 'edges_delete_random')
        self.saveResults(data, 'edges_delete_random')

    def expRandomMissingEdges(self, iter, step, end):
        data = []
        histogram = self.newHistogram(step, end)
        for _ in xrange(0,iter):
            self.readData()
            tnumber = self.runExperimentEdges(step, end)
            all_edges = set([e for e in tnumber[0]])
            for i in tnumber:
                t_data = [i]
                common_edges = list(all_edges.intersection([e for e in tnumber[i]]))
                for p in self.top:
                    common_edges = self.selectTopN(tnumber[0], common_edges,\
                     int(self.number_of_edges * p))
                    x1 = [tnumber[0][n] for n in common_edges]
                    x2 = [tnumber[i][n] for n in common_edges]
                    tau, p_value = stats.kendalltau(x1, x2)
                    t_data += [tau, p_value]
                    self.getHistogram(x2, histogram, i, p)

                data.append(t_data)
                print(t_data)

        self.saveMeanResults(data, 'edges_delete_random')
        self.processHistogram(histogram, 'edges_delete_random')
        self.saveResults(data, 'edges_delete_random')

    def expRandomRewireEdges(self, iter, step, end):
        data = []
        histogram = self.newHistogram(step, end)
        for _ in xrange(0,iter):
            self.readData()
            tnumber = self.runExperimentEdges(step, end, mode=1)
            all_edges = set([e for e in tnumber[0]])
            for i in tnumber:
                t_data = [i]
                common_edges = list(all_edges.intersection([e for e in tnumber[i]]))
                for p in self.top:
                    common_edges = self.selectTopN(tnumber[0], common_edges,\
                     int(self.number_of_edges * p))
                    x1 = [tnumber[0][n] for n in common_edges]
                    x2 = [tnumber[i][n] for n in common_edges]
                    tau, p_value = stats.kendalltau(x1, x2)
                    t_data += [tau, p_value]
                    self.getHistogram(x2, histogram, i, p)

                data.append(t_data)
                print(t_data)

        self.saveMeanResults(data, 'edges_rewire_random')
        self.processHistogram(histogram, 'edges_rewire_random')
        self.saveResults(data, 'edges_rewire_random')

    def runExperiment(self, iter=10, step = 5, end = 50):
        if self.mode[0] is '1':
            print('Noise: \t Random node deletion')
            self.expRandomMissingNodes(iter, step, end)
        if self.mode[1] is '1':
            print('Noise: \t Random edge deletion')
            self.expRandomMissingEdges(iter, step, end)
        if self.mode[2] is '1':
            print('Noise: \t Random edge rewire preserving degree dist')
            self.expRandomRewireEdges(iter, step, end)

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
