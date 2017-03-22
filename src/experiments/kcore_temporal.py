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
from noise import rewire
import operator

class KCoreExperiment(object):
    """docstring for KCoreExperiment."""
    def __init__(self, fname, sname):
        super(KCoreExperiment, self).__init__()
        self.graph = nx.Graph()
        self.fname = fname
        self.sname = sname
        self.kcore = kcore.KCore(self.graph)
        self.number_of_nodes = self.graph.number_of_nodes()
        self.number_of_edges = self.graph.number_of_edges()
        self.top = [1, 0.2, 0.1, 0.05]                  # Percentage of top nodes consider
        self.ori_graph = None

    def coreNumber(self, can_cache=False):
        if can_cache:
            cnumber = self.readCache()
            if cnumber is None:
                cnumber = self.kcore.coreNumber(self.graph)
                self.writeCache(cnumber)
            return cnumber
        else:
            return self.kcore.coreNumber(self.graph)

    def nextGraph(self, i):
        fname = self.fname + str(i) + '.csv'
        graph = nx.read_edgelist(fname, 'r')
        return graph

    def combineGraphs(self, ori_start, ori_end):
        self.graph = nx.Graph()
        for i in xrange(ori_start, ori_end):
            fname = self.fname + str(i) + '.csv'
            with open(fname, 'r') as f:
                reader = csv.reader(f, delimiter='\t')
                for row in reader:
                    if len(row) > 1:
                        self.graph.add_edge(row[0], row[1])

    def runExp(self, temp_start = 0, temp_end = 10, ori_start = 0, ori_end = 14):
        self.combineGraphs(ori_start, ori_end)
        cnumber = {ori_end:self.coreNumber(can_cache=False)}

        for i in xrange(temp_start, temp_end):
            self.graph = self.nextGraph(i)
            cnumber[i] = self.coreNumber()
        print(len(cnumber))
        return cnumber

    def selectTopN(self, nvalues, keys, n):
        """
        Select the top n keys with the highest values
        """
        data = [(k, nvalues[k]) for k in keys]
        values = sorted(data, key=operator.itemgetter(1), reverse=True)[:n]
        topn = [x[0] for x in values]
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

    def saveResults(self, data, iden):
        fname = self.sname + '_core_' + iden + '.csv'
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
        fname = self.sname + '_core_histogram_' + iden + '.csv'
        with open(fname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for d in data:
                writer.writerow(d)

    def processHistogram(self, histogram, identifier):
        if histogram is None:
            histogram = {p: {x:{} for x in xrange(0, end, step)} for p in self.top}
        for p in histogram:
            hist = histogram[p]
            print(hist)
            hdata = [['core_number'] + ['change_'+str(i) for i in hist]]
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
        if len(x2) == 0:
            return None
        if max(x2) > min(x2):
            hist, sep = np.histogram(x2, bins=max(x2)-min(x2))
            for s in sep[:-1]:
                if s not in histogram[p][i]:
                    histogram[p][i][s] = []

            for k, v in enumerate(hist):
                histogram[p][i][sep[k]].append(v)
        else:
            histogram[p][i][x2[0]] = [len(x2)]

    def newHistogram(self, temp_start, temp_end):
        return {p: {x:{} for x in xrange(temp_start, temp_end)} for p in self.top}

    def expTemporal(self, temp_start = 0, temp_end = 10, ori_start = 0, ori_end = 14):
        data = []
        histogram = self.newHistogram(temp_start, temp_end)

        cnumber = self.runExp(temp_start = 0, temp_end = 10, ori_start = 0, ori_end = 14)
        all_nodes = set([n for n in cnumber[ori_end]])
        for i in cnumber:
            t_data = [i]
            common_nodes = list(all_nodes.intersection([n for n in cnumber[i]]))
            for p in self.top:
                common_nodes = self.selectTopN(cnumber[i], common_nodes,\
                 int(len(cnumber[i]) * p))
                x1 = [cnumber[ori_end][n] for n in common_nodes]
                x2 = [cnumber[i][n] for n in common_nodes]
                tau, p_value = stats.kendalltau(x1, x2)
                t_data += [tau, p_value]
                #self.getHistogram(x2, histogram, i, p)

                data.append(t_data)
            print(t_data)

        #self.processHistogram(histogram, 'temporal')
        self.saveResults(data, 'temporal')

    def runExperiment(self, temp_start = 0, temp_end = 10, ori_start = 0, ori_end = 14):
        self.expTemporal(temp_start = 0, temp_end = 10, ori_start = 0, ori_end = 14)


if __name__ == '__main__':
    fname = sys.argv[1]
    sname = sys.argv[2]

    kcore = KCoreExperiment(fname, sname)
    kcore.runExperiment()
