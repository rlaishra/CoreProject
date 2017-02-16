from __future__ import division, print_function
from decomposition import kcore
from noise import missing
import networkx as nx
import sys
import random
import csv

class KCoreExperiment(object):
    """docstring for KCoreExperiment."""
    def __init__(self, fname, sname):
        super(KCoreExperiment, self).__init__()
        self.graph = nx.read_edgelist(fname)
        self.kcore = kcore.KCore(self.graph)

    def coreNumber(self):
        return self.kcore.coreNumber()

    def runExperimentNode(self, step = 5, end = 50):
        cnumber = {0:self.coreNumber()}

        noise = missing.MissingData()
        size = int(self.graph.number_of_nodes()*step*0.01)

        for i in xrange(1, int(end/step)):
            self.graph = noise.removeRandomNodes(self.graph, size)
            cnumber[i*step] = self.coreNumber()

        print(cnumber)




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
