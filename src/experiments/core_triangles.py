from __future__ import division, print_function
from decomposition import kcore
from noise import missing
import networkx as nx
import operator
import csv

class KCoreTriangles(object):
    """docstring for KCoreTriangles."""
    def __init__(self, fname, sname):
        super(KCoreTriangles, self).__init__()
        self.graph = nx.read_edgelist(fname)
        self.kcore = kcore.KCore(self.graph)
        self.top = int(self.graph.number_of_nodes()*0.1)
        self.sname = sname

    def topCoreNodes(self):
        cnumber = self.kcore.coreNumber(self.graph)
        data = [(k,cnumber[k]) for k in cnumber]
        data = sorted(data, key=operator.itemgetter(1), reverse=True)[:self.top]
        return data

    def triangleCounts(self, cdata):
        tdata = []
        traingles = nx.triangles(self.graph,[d[0] for d in cdata])
        for d in cdata:
            tdata.append((d[1], traingles[d[0]]))
        return tdata

    def cliqueCounts(self, cdata, k):
        tdata = []
        cliques = nx.cliques_containing_node(self.graph,[d[0] for d in cdata])
        for d in cdata:
            cl = len([c for c in cliques[d[0]] if len(c) >= k])
            tdata.append((d[1], cl))
        return tdata

    def cliqueNumber(self, cdata):
        tdata = []
        cliques = nx.node_clique_number(self.graph,[d[0] for d in cdata])
        for d in cdata:
            tdata.append((d[1], cliques[d[0]]))
        return tdata

    def saveData(self, tdata):
        with open(self.sname, 'w') as f:
            writer = csv.writer(f, delimiter=' ')
            writer.writerow(['core', 'triangles'])
            for d in tdata:
                writer.writerow(d)

    def run(self, k=3):
        cdata = self.topCoreNodes()
        #tdata = self.triangleCounts(cdata)
        #cldata = self.cliqueCounts(cdata, k)
        cldata = self.cliqueNumber(cdata)
        self.saveData(cldata)
        print(cldata)
