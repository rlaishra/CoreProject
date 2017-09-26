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
	print(nx.info(graph))
	return graph

def nodesOrder(graph):
	nodes = list(graph.nodes())
	return tuple(nodes)

def coreNumber(graph, nodes):
	cn = nx.core_number(graph)
	cn = [cn[u] for u in nodes]
	return cn

def removeEdges(graph, num):
	edges = list(graph.edges())
	random.shuffle(edges)
	remove = edges[:num]
	graph.remove_edges_from(remove)
	return graph

def compare(x1, x2, k):
	sl = sorted(x1, reverse=True)
	th = sl[int(len(sl) * k / 100)]

	ind = [j for j in xrange(0, len(x1)) if x1[j] >= th]

	d1 = [x1[i] for i in ind] + [0]
	d2 = [x2[i] for i in ind] + [0]
	#print(d1)
	#print(d2)
	cor, _ = stats.kendalltau(d1, d2, nan_policy='omit')

	if np.isnan(cor):
		cor = 1
	return cor


def saveRawData(sname, data, name, n):
	if n:
		f = open(sname + '_raw.csv', 'w')
	else:
		f = open(sname + '_raw.csv', 'a')

	writer = csv.writer(f, delimiter=',')
	if n:
		writer.writerow(['exp', 'p', 'k', 'cor', 'added'])
	for d in data:
		writer.writerow(d + [name])

def saveCompiledData(sname, data, name, n):
	if n:
		f = open(sname + '_compiled.csv', 'w')
	else:
		f = open(sname + '_compiled.csv', 'a')

	writer = csv.writer(f, delimiter=',')
	if n:
		writer.writerow(['p', 'k', 'cor_mean', 'cor_std', 'name'])
	for d in data:
		writer.writerow(d + [name])

def main(fname, sname, exp, name, n):
 	k = range(10,100,10)
 	p = range(10,100,10)

 	x = 0

 	data = []
 	cdata = {}

 	while x < exp:
 		for y in p:
	 		graph = readGraph(fname)
 			nodes = nodesOrder(graph)

 			# The baseline core numbers
 			ocn = coreNumber(graph, nodes)

 			num = int(graph.number_of_edges()*y/100)
 			graph = removeEdges(graph, num)

 			ncn = coreNumber(graph, nodes)

 			for z in k:
 				cor = compare(ocn, ncn, z)
 				data.append([x, y, z, cor])

 				if (y,z) not in cdata:
 					cdata[(y,z)] = []
 				cdata[(y,z)].append(cor)

 				print(data[-1])
 		x += 1

 	saveRawData(sname, data, name, n)

 	# Generate mean and std
 	tdata = []
 	for t in cdata:
 		tdata.append([t[0], t[1], np.mean(cdata[t]), np.std(cdata[t])])
 	saveCompiledData(sname, tdata, name, n)

if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]
	exp = int(sys.argv[3])
	name = int(sys.argv[4])
	n = int(sys.argv[5]) == 1


	main(fname, sname, exp, name, n)

