from __future__ import division, print_function
import networkx as nx 
import numpy as np 
import sys
from pprint import pprint
import csv


def readGraph(fname):
	if fname.endswith('mtx'):
		edges = []
		with open(fname, 'r') as f:
			reader = csv.reader(f, delimiter=' ')
			for row in reader:
				if len(row) == 2:
					edges.append(row)
		graph = nx.Graph()
		graph.add_edges_from(edges)
	else:
		graph = nx.read_edgelist(fname)
	graph.remove_edges_from(graph.selfloop_edges())
	print(nx.info(graph))
	return graph


def getCoreDistrubution(graph):
	cn = nx.core_number(graph)
	c_max = max(cn.values())

	total = len(cn)
	dist = {c:0 for c in xrange(0, c_max+1)}

	for c in cn:
		dist[cn[c]] += 1/total

	return dist

def saveCoreDistribution(sname, dist):
	with open(sname, 'w') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow(['core', 'frequency'])
		for d in dist:
			writer.writerow([d, dist[d]])

if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]

	graph = readGraph(fname)
	dist = getCoreDistrubution(graph)
	saveCoreDistribution(sname, dist)