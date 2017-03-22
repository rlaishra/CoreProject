from __future__ import division, print_function
from decomposition import nucleus
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

class NucleusExperiment(object):
    """docstring for KCoreExperiment."""
    def __init__(self, fname, sname, adjacency=False, mode='111'):
        super(NucleusExperiment, self).__init__()
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
        self.nucleus = nucleus.NucleusDecomposition()
        self.number_of_nodes = self.graph.number_of_nodes()
        self.number_of_edges = self.graph.number_of_edges()
        self.ori_graph = None

    def readCache(self):
        fname = self.sname + '_nucleus_pickle.pickle'
        if os.path.isfile(fname):
            with open(fname, 'r') as f:
                print('Found cache: ' + fname)
                data = pickle.load(f)
                self.graph = data['graph']
                return data['nucleii']
        return None

    def writeCache(self, nucleii):
        fname = self.sname + '_nucleus_pickle.pickle'
        f = open(fname, 'w')
        data = {'graph': self.graph.copy(), 'nucleii': nucleii}
        pickle.dump(data, f)


    def readData(self):
        #self.graph = nx.complete_graph(10)
        #self.graph.add_edges_from([(12,13),(12,14),(12,15),(13,14),(13,15),(14,15)])
        #return True
        if self.ori_graph is None:
            if not self.adj:
                self.ori_graph = nx.read_edgelist(self.fname)
            else:
                self.ori_graph = nx.read_adjlist(self.fname)
        self.graph = self.ori_graph.copy()

    def getNucleii(self, r=3, s=4, can_cache=False):
        if can_cache:
            nucleii = self.readCache()
            if nucleii is None:
                nucleii = self.nucleus.decomposition(self.graph, r, s)
                self.writeCache(nucleii)
            return nucleii
        else:
            return self.nucleus.decomposition(self.graph, r, s)

    def runExperimentNode(self, r=3, s=4, step = 10, end = 50):
        nucleii = {0:self.getNucleii(r,s,can_cache=True)}

        noise = missing.MissingData()
        size = int(self.graph.number_of_nodes()*step*0.01)

        for i in xrange(1, int(end/step)):
            self.graph = noise.removeRandomNodes(self.graph, size)
            print(size, 'nodes', self.graph.number_of_nodes())
            nucleii[i*step] = self.getNucleii(r,s)

        return nucleii

    def runExperimentEdges(self, r=3, s=4, step = 10, end = 50, mode = 0):
        """
        mode
            0   random edge delete
            1   random edge rewiring
        """
        nucleii = {0:self.getNucleii(r,s,can_cache=True)}
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
            nucleii[i*step] = self.getNucleii(r,s)

        return nucleii

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
                cdata[d[0]] = []
            cdata[d[0]].append(d[1])
        mdata = []
        for i in cdata:
            d = [i, np.mean(cdata[i]), np.std(cdata[i])]
            mdata.append(d)
        return mdata

    def saveMeanResults(self, data, iden):
        data = self.resultsMean(data)
        fname = self.sname + '_nucleus_mean_' + iden + '.csv'
        with open(fname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            header = ['change', 'jaccard_mean', 'jaccard_std']
            writer.writerow(header)
            for d in data:
                writer.writerow(d)

    def saveResults(self, data, iden):
        fname = self.sname + '_nucleus_' + iden + '.csv'
        with open(fname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            header = ['change', 'jaccard']
            writer.writerow(header)
            for d in data:
                writer.writerow(d)

    def similarity(self, nucleii_ori, nucleii_new):
        total = len(set().union(*nucleii_new))
        weights = [len(n)/total for n in nucleii_new]
        similarity = []
        for i, j in enumerate(nucleii_new):
            sim = []
            nucleus_1 = j
            for nucleus_2 in nucleii_ori:
                print(nucleus_1)
                print(nucleus_2)
                print('inter',len(set(nucleus_1).intersection(nucleus_2)))
                print('union',len(set(nucleus_1).union(nucleus_2)))
                sim.append(len(set(nucleus_1).intersection(nucleus_2))\
                /len(set(nucleus_1).union(nucleus_2)))
            similarity.append(weights[i]*max(sim))
        return np.sum(similarity)


    def expRandomMissingNodes(self, iter, step, end, r, s):
        data = []
        for _ in xrange(0,iter):
            self.readData()
            nucleii = self.runExperimentNode(r, s, step, end)
            for i in nucleii:
                t_data = [i, self.similarity(nucleii[0], nucleii[i])]
                data.append(t_data)
                print(t_data)

        self.saveMeanResults(data, 'nodes_delete_random_r_'+str(r)+'_s_'+str(s))
        self.saveResults(data, 'nodes_delete_random_r_'+str(r)+'_s_'+str(s))


    def expRandomMissingEdges(self, iter, step, end, r, s):
        data = []
        for _ in xrange(0,iter):
            self.readData()
            nucleii = self.runExperimentEdges(r, s, step, end, 0)
            for i in nucleii:
                t_data = [i, self.similarity(nucleii[0], nucleii[i])]
                data.append(t_data)
                print(t_data)

        self.saveMeanResults(data, 'edges_delete_random_r_'+str(r)+'_s_'+str(s))
        self.saveResults(data, 'edges_delete_random_r_'+str(r)+'_s_'+str(s))

    def expRandomRewireEdges(self, iter, step, end, r, s):
        data = []
        for _ in xrange(0,iter):
            self.readData()
            nucleii = self.runExperimentEdges(r, s, step, end, 1)
            for i in nucleii:
                t_data = [i, self.similarity(nucleii[0], nucleii[i])]
                data.append(t_data)
                print(t_data)

        self.saveMeanResults(data, 'edges_rewire_random_r_'+str(r)+'_s_'+str(s))
        self.saveResults(data, 'edges_rewire_random_r_'+str(r)+'_s_'+str(s))

    def runExperiment(self, iter=10, step = 5, end = 50, r = 3, s = 4):
        if self.mode[0] is '1':
            print('Noise: \t Random node deletion')
            self.expRandomMissingNodes(iter, step, end, r, s)
        if self.mode[1] is '1':
            print('Noise: \t Random edge deletion')
            self.expRandomMissingEdges(iter, step, end, r, s)
        if self.mode[2] is '1':
            print('Noise: \t Random edge rewire preserving degree dist')
            self.expRandomRewireEdges(iter, step, end, r, s)

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
