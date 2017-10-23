"""
Compute the k,p-robustness of a network
"""

from __future__ import division, print_function
import networkx as nx
import numpy as np
import sys
import os
import cPickle as pickle
from scipy import stats
import time
import csv
import random

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
	#print(nx.info(graph))
	return graph

def nodesOrder(graph):
	nodes = list(graph.nodes())
	return tuple(nodes)

def coreNumber(graph, nodes):
	cn = nx.core_number(graph)
	cn = {u:cn[u] for u in nodes if u in cn}
	return cn

def removeEdges(graph, num):
	edges = list(graph.edges())
	random.shuffle(edges)
	remove = edges[:num]
	graph.remove_edges_from(remove)
	return graph

def removeNodes(graph, num):
	nodes = list(graph.nodes())
	random.shuffle(nodes)
	remove = nodes[:num]
	graph.remove_nodes_from(remove)
	return graph

def compare(x1, x2, k):
	sl = sorted([x1[u] for u in x1], reverse=True)
	#print(len(sl), k,  len(sl) * k / 100)
	th = sl[int(len(sl) * k / 100)]

	# Filter out nodes not in x2 from x1
	#print('threshold',th)
	#print(len(x1), len(x2))
	#print(max([x1[u] for u in x1]))
	x1 = {u:x1[u] for u in x1 if u in x2}
	#print(max([x1[u] for u in x1]))
	ind = [u for u in x1 if x1[u] >= th]
	#print(len(x1), len(x2))
	#print(ind)

	d1 = [x1[i] for i in ind] + [0]
	d2 = [x2[i] for i in ind] + [0]
	#print(d1)
	#print(d2)
	cor, _ = stats.kendalltau(d1, d2, nan_policy='omit')

	if np.isnan(cor):
		cor = 1
	return cor


def saveRawData(sname, data, name, n, noise):
	if n:
		f = open(sname + '_' + noise + '_' + '_raw.csv', 'w')
	else:
		f = open(sname + '_' + noise + '_' + '_raw.csv', 'a')

	writer = csv.writer(f, delimiter=',')
	if n:
		writer.writerow(['exp', 'p', 'k', 'cor', 'added'])
	for d in data:
		writer.writerow(d + [name])

def saveCompiledData(sname, data, name, n, noise):
	if n:
		f = open(sname + '_' + noise + '_' + '_compiled.csv', 'w')
	else:
		f = open(sname + '_' + noise + '_' + '_compiled.csv', 'a')

	writer = csv.writer(f, delimiter=',')
	if n:
		writer.writerow(['p', 'k', 'cor_mean', 'cor_std', 'name'])
	for d in data:
		writer.writerow(d + [name])

def main(fname, sname, exp, name, n, noise='edges'):
 	k = range(20,100,20)
 	p = range(1,25,1)
 	#k = [1]

 	results = {}
 	data = []
 	cdata = {}

	for z in k:
		x = 0

	 	adata = []

	 	while x < exp:
	 		tdata = []
	 		for y in p:
		 		graph = readGraph(fname)
	 			nodes = nodesOrder(graph)

	 			# The baseline core numbers
	 			ocn = coreNumber(graph, nodes)

	 			if noise == 'edges':
	 				num = int(graph.number_of_edges()*y/100)
	 				graph = removeEdges(graph, num)
	 			elif noise == 'nodes':
	 				num = int(graph.number_of_nodes()*y/100)
	 				graph = removeNodes(graph, num)

	 			ncn = coreNumber(graph, nodes)

	 			cor = compare(ocn, ncn, z)
	 			tdata.append(cor)
	 			#print(y, tdata)
	 			data.append([x, y, z, cor])

	 			if (y,z) not in cdata:
		 			cdata[(y,z)] = []
	 			cdata[(y,z)].append(np.mean(cor))

	 		adata.append(np.mean(tdata))

	 		#print(tdata)
	 		x += 1
	 	results[z] = (np.mean(adata), np.std(adata))
 		x += 1

 	#print('Mean Core Resilience: {} {}'.format(np.mean(adata), np.std(adata)))
 	#print('')

 	saveRawData(sname, data, name, n, noise)

 	# Generate mean and std
 	tdata = []
 	for t in cdata:
 		tdata.append([t[0], t[1], np.mean(cdata[t]), np.std(cdata[t])])
 	saveCompiledData(sname, tdata, name, n, noise)

if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]
	exp = int(sys.argv[3])
	name = float(sys.argv[4])
	n = int(sys.argv[5]) == 1
	noise = sys.argv[6] # Edge or Node or both


	main(fname, sname, exp, name, n, noise)

