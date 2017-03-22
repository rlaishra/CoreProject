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


class CoreMinEdgesExperiments(object):
    """docstring for CoreMinEdgesExperiments."""
    def __init__(self, fname, sname):
        super(CoreMinEdgesExperiments, self).__init__()
        self.fname = fname
        self.sname = sname
        self.graph = nx.read_edgelist(self.fname)
        self.kcore = kcore.KCore(self.graph)
        self.number_of_nodes = self.graph.number_of_nodes()
        self.number_of_edges = self.graph.number_of_edges()

    def coreNumber(self, can_cache=False):
        return self.kcore.coreNumber(self.graph)

    def getSubGraph(self, nodes):
        sg = nx.Graph()
        for n1 in nodes:
            neighbors = list(set(self.graph.neighbors(n1)).intersection(nodes))
            edges = [(n1, n) for n in neighbors]
            sg.add_edges_from(edges)
        return sg

    def edgesCount(self, nodes):
        count = 0
        for n1 in nodes:
            neighbors = list(set(self.graph.neighbors(n1)).intersection(nodes))
            count += len(neighbors)
        return count

    def topNodes(self, cnumber):
        # Returns the top count nodes with highest core number
        values = set([cnumber[n] for n in cnumber])
        values = sorted(values, reverse=True)
        #values = values[:3]
        nodes = [n for n in cnumber if cnumber[n] in values]
        return nodes

    def coreMissing(self, nodes, core_ori):
        stop = 80
        step = 2
        iterer = 10
        cnumber = {n:[] for n in nodes}
        size = int(self.graph.number_of_edges()*step*0.01)
        noise = missing.MissingData()

        header = ['k_'+str(i*step) for i in xrange(0, int(stop/step)+1)]

        for _ in xrange(0, iterer):
            self.graph = nx.read_edgelist(self.fname)
            for i in xrange(0, int(stop/step)):
                self.graph = noise.removeRandomEdges(self.graph, size)
                cn = self.coreNumber()

                for n in cnumber:
                    if len(cnumber[n]) < i+1:
                        cnumber[n].append([])
                    if n in cn:
                        cnumber[n][i].append(cn[n])
                    else:
                        cnumber[n][i].append(0)
        data = {}
        for n in nodes:
            data[n] = [core_ori[n]]
            for d in cnumber[n]:
                data[n].append(np.mean(d))

        header += ['k_diff_'+str(i*step) for i in xrange(1, int(stop/step)+1)]
        for n in nodes:
            for d in cnumber[n]:
                data[n].append(core_ori[n] - np.mean(d))

        header += ['k_diff_ratio_'+str(i*step) for i in xrange(1, int(stop/step)+1)]
        for n in nodes:
            for d in cnumber[n]:
                data[n].append((core_ori[n] - np.mean(d))/core_ori[n])

        return data, header

    def cliqueData(self, cnumber, data, header, sg, k):
        for n in data:
            data[n]+=[0,0,0]
        com = list(nx.k_clique_communities(sg, k))
        header += [str(k)+'_clique_size', str(k)+'_clique_edges', str(k)+'_clique_density']
        for c in com:
            count = self.edgesCount(list(c))
            for n in c:
                if len(c) > data[n][-3]:
                    data[n][-3] = len(c)
                    data[n][-2] = count
                    data[n][-1] = count/(data[n][-3]*data[n][-3]-data[n][-3])
        header += [str(k)+'_min_edges', str(k)+'_min_edges_ratio']
        for n in data:
            if data[n][-1] > 0:
                data[n].append(np.ceil(data[n][-3]*cnumber[n]/2))
                data[n].append(data[n][-3]/data[n][-1])
            else:
                data[n] += [0,0]

        return data, header

    def saveData(self, data, header):
        sname = self.sname + '_core_number_min_edges.csv'
        with open(sname, 'w') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(header)
            for d in data:
                writer.writerow(d)

    def getTriangles(self, data, header):
        triangles = nx.triangles(self.graph, nodes=[n for n in data])
        header += ['triangles']
        for n in data:
            data[n].append(triangles[n])
        return data, header

    def runExperiment(self):
        cnumber = self.coreNumber()
        nodes = self.topNodes(cnumber)
        sg = self.getSubGraph(nodes)

        data = {n:[] for n in nodes}
        header = ['node']

        data, header = self.cliqueData(cnumber, data, header, sg, 3)
        data, header = self.cliqueData(cnumber, data, header, sg, 4)
        data, header = self.cliqueData(cnumber, data, header, sg, 5)

        data, header = self.getTriangles(data, header)

        cn, h = self.coreMissing(nodes, cnumber)

        header += h

        ldata = []
        for n in nodes:
            l = [n] + data[n] + cn[n]
            ldata.append(l)

        self.saveData(ldata, header)


    def run(self):
        self.runExperiment()


if __name__ == '__main__':
    print('Test')
