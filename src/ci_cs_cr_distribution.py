from __future__ import division, print_function
import networkx as nx
import numpy as np
import sys
import os
import cPickle as pickle
import time
import csv
import scipy.stats as stats

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


def _getSupportNodes(graph, cnumber, u):
	"""
	Get the list of neighbors of u with greater core number than u
	whose removal will affect the core number of u
	"""
	n = [v for v in graph.neighbors(u) if cnumber[v] == cnumber[u]]

	# Check if u relies on nodes with higher core number for its core number
	if len(n) >= cnumber[u]:
		return []

	# Node u relies on higher nodes for its core number
	return [v for v in graph.neighbors(u) if cnumber[v] > cnumber[u]]



def getCoreInfluence(cnumber, kcore):
	"""
	Compute the influence score for each nodes
	"""
	knumber = [cnumber[u] for u in cnumber]
	kmin = min(knumber)
	kmax = min(knumber)

	iScore = {u:1 for u in cnumber}
	empty = []
	for k in xrange(kmin, kmax + 1):
		# Nodes in the kcore
		knodes = kcore[k].nodes()

		for u in knodes:
			supNodes = _getSupportNodes(kcore[k], cnumber, u)
			if len(supNodes) < 1:
				empty.append(u)
				continue

			share = iScore[u]/len(supNodes)
			for v in supNodes:
				iScore[v] += share
	

	# Normalize between 0 and std
	#imin = min(iScore.values())
	#imax = max(iScore.values())

	#for u in iScore:
	#	iScore[u] = (iScore[u]-imin)/(imax - imin)

	return iScore


def getCoreStrength(graph, cnumber):
	data = {}
	m = graph.number_of_edges()

	for u in cnumber:
		neighbors = graph.neighbors(u)
		cd = len([v for v in neighbors if cnumber[u] <= cnumber[v]])
		data[u] = cd - cnumber[u]
		
	return data

def generateCoreSubgraph(graph, cnumber):
	cn = set(cnumber.values())
	core_subgraph = {}

	for c in cn:
		core_subgraph[c] = nx.k_core(graph, k = c, core_number=cnumber)

	return core_subgraph


def saveData(sname, data, name, n):
	if n:
		f = open(sname, 'w')
	else:
		f = open(sname, 'a')
	
	writer = csv.writer(f, delimiter=',')
	if n:
		writer.writerow(['ci', 'cs', 'cr', 'name'])
	
	for d in data:
		writer.writerow(d + [name])


if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]
	name = float(sys.argv[3])
	n = int(sys.argv[4]) == 1

	# Generate nodes list
	graph = readGraph(fname)
	cnumber = nx.core_number(graph)
	nodes = graph.nodes()
	#cutoff = 0
	#nodes = [u for u in graph.nodes() if cnumber[u] >= cutoff]

	# Get data
	#graph = readGraph(fname2)
	#cnumber = nx.core_number(graph)
	kcore = generateCoreSubgraph(graph, cnumber)

	#graph = graph.subgraph(nodes)
	ci = getCoreInfluence(cnumber, kcore)
	cs = getCoreStrength(graph, cnumber)

	#iScore = {u:iScore[u] for u in nodes}
	#rcd = {u:rcd[u] for u in nodes}

	data = []

	for u in nodes:
		data.append([ci[u], cs[u], cnumber[u]])

	saveData(sname, data, name, n)


