from __future__ import division, print_function
from decomposition import kcore
import networkx as nx
from pprint import pprint
import csv

class KCoreHistogram(object):
    """docstring for KCoreHistogram."""
    def __init__(self, fname, sname, adjacency=False, ftype='file'):
        super(KCoreHistogram, self).__init__()
        self.sname = sname                              # do not save if sname is none
        if ftype == 'file':
            if not adjacency:
                self.graph = nx.read_edgelist(fname)
            else:
                self.graph = nx.read_adjlist(fname)
        else:
            self.graph = fname.copy()      # fname is a networkx graph
        self.kcore = kcore.KCore(self.graph)
        print('Number of nodes: {}\t Number of edges: {}'.format(\
         self.graph.number_of_nodes(), self.graph.number_of_edges()))

    def coreData(self, cnumber):
        core_nodes = {i:[] for i in xrange(1, max([cnumber[n] for n in cnumber])+1)}
        for n in cnumber:
            core_nodes[cnumber[n]].append(n)

        core_data = []
        for i in core_nodes:
            if len(core_nodes[i]) > 0:
                sg = self.graph.subgraph(core_nodes[i])
                deg = sg.number_of_edges() * 2 / sg.number_of_nodes()
                cc = nx.average_clustering(sg)
                com = nx.number_connected_components(sg)
                count = sg.number_of_nodes()
                core_data.append([i, count, deg, cc, com])
            else:
                core_data.append([i, 0, 0, 0, 0])
        return core_data

    def saveData(self, data):
        with open(self.sname, 'w') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(('core', 'count', 'degree', 'clustering', 'components'))
            for d in data:
                writer.writerow(d)

    def runExperiment(self, save=True):
        cnumber = self.kcore.coreNumber()
        cdata = self.coreData(cnumber)
        if self.sname is not None:
            self.saveData(cdata)
        else:
            return cdata

if __name__ == '__main__':
    print('Go away')
