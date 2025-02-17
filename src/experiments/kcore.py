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
from utils import statistics

class KCoreExperiment(object):
    """docstring for KCoreExperiment."""
    def __init__(self, fname, sname, adjacency=False, mode='111', ftype='file', top=None):
        super(KCoreExperiment, self).__init__()
        self.fname = fname
        self.sname = sname                      # If sname is none retults are turned not saved
        self.adj = adjacency
        """
        1st digit for random node deletion,
        2nd digit for random edge deletion,
        3rd digit for random rewiring preserving degree dist
        """
        self.mode = mode
        if ftype == 'file':                             # ftype can be file on graph. if graph fname is a networkx graph object
            if not self.adj:
                self.graph = nx.read_edgelist(self.fname)
                self.graph.remove_edges_from(self.graph.selfloop_edges())
            else:
                self.graph = nx.read_adjlist(self.fname)
                self.graph.remove_edges_from(self.graph.selfloop_edges())
            self.ori_graph = None
        else:
            self.graph = fname.copy()
            self.ori_graph = fname.copy()

        self.kcore = kcore.KCore(self.graph)
        self.number_of_nodes = self.graph.number_of_nodes()
        self.number_of_edges = self.graph.number_of_edges()
        if top is None:
            self.top = [x/100 for x in range(100,1,-5)]            # Percentage of top nodes consider
        else:
            self.top = top
        self.stats = statistics.Statistics()

    def readCache(self):
        if self.sname is None:
            return None
        fname = self.sname + '_core_pickle.pickle'
        if os.path.isfile(fname):
            with open(fname, 'r') as f:
                print('Found cache: ' + fname)
                data = pickle.load(f)
                self.graph = data['graph']
                return data['cnumber']
        return None

    def writeCache(self, cnumber):
        if self.sname is None:
            return None
        fname = self.sname + '_core_pickle.pickle'
        f = open(fname, 'w')
        data = {'graph': self.graph.copy(), 'cnumber': cnumber}
        pickle.dump(data, f)

    def readData(self):
        if self.ori_graph is None:
            if not self.adj:
                self.ori_graph = nx.read_edgelist(self.fname)
                self.ori_graph.remove_edges_from(self.ori_graph.selfloop_edges())
            else:
                self.ori_graph = nx.read_adjlist(self.fname)
                self.ori_graph.remove_edges_from(self.ori_graph.selfloop_edges())
        self.graph = self.ori_graph.copy()

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

    def runExperimentEdges(self, step = 5, end = 50, mode=0, sname=None):
        """
        mode
            0   random edge delete
            1   random edge rewiring
        """
        #cnumber = {0:self.coreNumber(can_cache=True)}
        cnumber = {0:nx.core_number(self.graph)}
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
            cnumber[i*step] = nx.core_number(self.graph)

        #    if i*step % 10 == 0:
        #        nx.write_edgelist(self.graph, self.sname + '_' + str(i*step) + '.edgelist', data=False)
        return cnumber

    def selectTopN(self, nvalues, keys, n):
        """
        Select the top n keys with the highest values
        """
        data = [(k, nvalues[k]) for k in keys]
        #print('A',len(keys), len(data), len(nvalues))
        values = sorted(data, key=operator.itemgetter(1), reverse=True)[:n]
        topn = [x[0] for x in values]
        cn = nvalues[topn[-1]]
        i = 0
        while n + i < len(values) and values[n+i][1] == cn:
            topn.append(values[n+i][0])
            i += 1
        #print('B',n,len(topn))
        return topn

    def resultsMean(self, data):
        cdata = {d[1]:[[] for _ in self.top] for d in data}
        
        for d in data:
            for i in xrange(0, len(self.top)):
                cdata[d[1]][i].append(d[i + 2])
        
        mdata = []
        for i in cdata:
            d = [i]
            for l in cdata[i]:
                x = [x for x in l if not np.isnan(x)]
                if len(x) > 0:
                    d += [np.mean(x), np.std(x)]
                else:
                    d += [0,0]
            mdata.append(d)
        return mdata

    def saveMeanResults(self, data, iden):
        data = self.resultsMean(data)
        fname = self.sname + '_core_mean_' + iden + '.csv'
        with open(fname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            header = ['change']
            for p in self.top:
                v = str(int(p*100))
                header += ['correlation_mean_'+v, 'correlation_std_'+v]
            writer.writerow(header)
            for d in data:
                writer.writerow(d)

    def saveResults(self, data, iden):
        fname = self.sname + '_core_' + iden + '.results'
        with open(fname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            header = ['exp','change']
            for p in self.top:
                v = str(int(p*100))
                header += ['correlation_'+v]
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
            cnumber = self.runExperimentNode(step, end)
            all_nodes = set([n for n in cnumber[0]])
            for i in cnumber:
                t_data = [i]
                common_nodes = list(all_nodes.intersection([n for n in cnumber[i]]))
                for p in self.top:
                    common_nodes = self.selectTopN(cnumber[i], common_nodes,\
                     int(self.number_of_nodes * p))
                    x1 = [cnumber[0][n] for n in common_nodes]
                    x2 = [cnumber[i][n] for n in common_nodes]
                    k_tau, k_p_value = stats.kendalltau(x1, x2, nan_policy='omit')
                    s_tau, s_p_value = stats.spearmanr(x1, x2)
                    #tau = self.stats.kendalltau(x1,x2)
                    #p_value = 0
                    t_data += [k_tau, k_p_value, s_tau, s_p_value]
                    #self.getHistogram(x2, histogram, i, p)

                data.append(t_data)
                print(t_data)
            # Least square error
            ls_x = []
            ls_y = []
            for r in data[-1]:
                ls_x.append(r[0])
                ls_y.append(r[1])
            v = np.polyfit(ls_x, ls_y, 1)
            print(v[1][0])

        self.saveMeanResults(data, 'nodes_delete_random')
        #self.processHistogram(histogram, 'nodes_delete_random')
        self.saveResults(data, 'nodes_delete_random')

    def expRandomMissingEdges(self, iter, step, end):
        data = []

        for _i in xrange(0,iter):
            print('Experiment {} of {}'.format(_i, iter))
            self.readData()
            cnumber = self.runExperimentEdges(step, end, mode=0)
            all_nodes = set([n for n in cnumber[0]])
            for i in cnumber:
                t_data = [_i, i]
                for p in self.top:
                    cnodes = self.selectTopN(cnumber[0], all_nodes,\
                     int(self.number_of_nodes * p))
                    x1 = [cnumber[0][n] for n in cnodes]
                    x2 = [cnumber[i][n] for n in cnodes]
                    k_tau, _ = stats.kendalltau(x1, x2, nan_policy='omit')
                    #k_tau = self.stats.kendalltau(x1, x2)
                    t_data.append(k_tau)
                data.append(t_data)
            
        self.saveMeanResults(data, 'edges_delete_random')
        self.saveResults(data, 'edges_delete_random')

    def expRandomRewireEdges(self, iter, step, end):
        data = []
        histogram = self.newHistogram(step, end)

        for _ in xrange(0,iter):
            self.readData()
            cnumber = self.runExperimentEdges(step, end, mode=1)
            all_nodes = set([n for n in cnumber[0]])
            for i in cnumber:
                t_data = [i]
                common_nodes = list(all_nodes.intersection([n for n in cnumber[i]]))
                for p in self.top:
                    common_nodes = self.selectTopN(cnumber[i], common_nodes,\
                     int(self.number_of_nodes * p))
                    x1 = [cnumber[0][n] for n in common_nodes]
                    x2 = [cnumber[i][n] for n in common_nodes]
                    tau, p_value = stats.kendalltau(x1, x2)
                    #tau = self.stats.kendalltau(x1, x2)
                    #p_value = 0
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
