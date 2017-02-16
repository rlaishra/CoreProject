from __future__ import division, print_function

from decomposition import kcore
import networkx as nx
import sys
import random
import csv

def ktruss(graph, k = 2):
    cgraph = graph.copy()
    complete = False
    while not complete:
        complete = True
        for n in cgraph.nodes():
            if nx.triangles(cgraph,n) < k:
                cgraph.remove_node(n)
                complete = False
    return cgraph

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
