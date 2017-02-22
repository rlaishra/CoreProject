from __future__ import division, print_function
from utils import statistics
import networkx as nx
from noise import missing
import csv

def readData(fname):
    return nx.read_edgelist(fname)

def removeEdges(graph, pc):
    noise = missing.MissingData()
    size = int(graph.number_of_edges()*pc*0.01)
    return noise.removeRandomEdges(graph, size)

def degreeDistribution(graph):
    stats = statistics.Statistics()
    return stats.degreeDistribution(graph)

def formatData(data):
    fdata = {d:[] for d in xrange(0, max([max(data[k].keys()) for k in data])+1)}
    header = ['degree'] + ['removed_'+str(d) for d in data]

    for r in data:
        for d in fdata:
            if d in data[r]:
                fdata[d].append(data[r][d])
            else:
                fdata[d].append(0)

    return header, fdata

def saveOutputs(data, sname):
    header, data = formatData(data)

    with open(sname, 'w') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(header)
        for d in data:
            writer.writerow([d]+data[d])


def main(fname, sname, pc):
    graph1 = readData(fname)
    dist = {}
    dist[0] = degreeDistribution(graph1)

    for r in xrange(pc-10, pc+10, 2):
        graph2 = removeEdges(graph1.copy(), r)
        dist[r] = degreeDistribution(graph2)

    saveOutputs(dist, sname)

if __name__ == '__main__':
    print('Nope')
