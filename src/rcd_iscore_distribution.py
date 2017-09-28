from __future__ import division, print_function
import networkx as nx
import numpy as np
import sys
import os
import cPickle as pickle
import time
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
	print(len(empty))

	# Normalize between 0 and std
	#imin = min(iScore.values())
	#imax = max(iScore.values())

	#for u in iScore:
	#	iScore[u] = (iScore[u]-imin)/(imax - imin)

	return iScore


def getRCD(graph, cnumber):
	data = {}

	for u in cnumber:
		neighbors = graph.neighbors(u)
		cd = len([v for v in neighbors if cnumber[u] == cnumber[v]]) + 1
		#data[u] = cd/cnumber[u] + 1
		data[u] = cd + 1

	# Rescale by dividing by
	#rmin = min(data.values())
	#rmax = max(data.values())

	#for u in data:
	#	data[u] = (data[u] - rmin) / (rmax - rmin)

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
		writer.writerow(['iscore', 'rcd', 'core', 'name'])
	
	for d in data:
		writer.writerow(d + [name])


if __name__ == '__main__':
	fname1 = sys.argv[1]
	fname2 = sys.argv[2]
	sname = sys.argv[3]
	#k = int(sys.argv[4])
	name = float(sys.argv[4])
	n = int(sys.argv[5]) == 1

	# Generate nodes list
	graph = readGraph(fname1)
	cnumber = nx.core_number(graph)
	#cutoff = sorted(cnumber.values(), reverse=True)[int(len(cnumber)*k/100)]
	cutoff = 0
	nodes = [u for u in graph.nodes() if cnumber[u] >= cutoff]

	# Get data
	graph = readGraph(fname2)
	cnumber = nx.core_number(graph)
	kcore = generateCoreSubgraph(graph, cnumber)

	#graph = graph.subgraph(nodes)
	iScore = getCoreInfluence(cnumber, kcore)
	rcd = getRCD(graph, cnumber)

	data = []

	for u in nodes:
		data.append([iScore[u], rcd[u], cnumber[u]])

	print('CIN \t 75: {} \t 90: {} \t 95: {} \t Mean: {}'.format(np.percentile(iScore.values(), 75),np.percentile(iScore.values(), 90),np.percentile(iScore.values(), 95), np.mean(iScore.values())))
	print('RCD \t 5: {} \t 10: {} \t 25: {} \t Mean: {}'.format(np.percentile(rcd.values(), 5),np.percentile(rcd.values(), 10),np.percentile(rcd.values(), 25), np.mean(rcd.values())))

	saveData(sname, data, name, n)


