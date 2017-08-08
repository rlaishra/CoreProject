"""
Find the core number and the number of neighbors with same core number or higher
"""

from __future__ import division, print_function

import networkx as nx
import numpy as np
import sys
import csv

def getGraph(fname, connected=True):
	"""
	Returns the graph
	If conncted is TRUE, returs the largest conncted component
	"""
	graph = nx.read_edgelist(fname, delimiter=',')
	if graph.number_of_nodes() == 0:
		graph = nx.read_edgelist(fname, delimiter='\t')
	if graph.number_of_nodes() == 0:
		graph = nx.read_edgelist(fname, delimiter=' ')
	if graph.number_of_nodes() == 0:
		return False
	graph = max(nx.connected_component_subgraphs(graph), key=len)
	graph.remove_edges_from(graph.selfloop_edges())
	return graph


def coreNumber(graph):
	cnumber = nx.core_number(graph)
	return cnumber


def coreDegree(graph, cnumber):
	"""
	The number of neighbors wih core number same or greater core number
	"""
	data = {}

	for u in graph.nodes():
		neighbors = graph.neighbors(u)
		mcd = len([v for v in neighbors if cnumber[u] <= cnumber[v]])
		cd = len([v for v in neighbors if cnumber[u] == cnumber[v]])
		data[u] = [mcd, cd, mcd/cnumber[u], cd/cnumber[u]]

	return data


def removeEdges(graph, p):
	"""
	Remove p fraction of edges and return a copy of the graph
	"""
	cgraph = graph.copy()
	edges = list(graph.edges())
	np.random.shuffle(edges)
	edges = edges[:int(p*len(edges)*0.01)]
	cgraph.remove_edges_from(edges)
	#print(p,len(edges),cgraph.number_of_edges(), graph.number_of_edges())
	return cgraph

def compileDate(cnumber, cdata, rdata):
	data = []
	for u in cnumber:
		for p in rdata[u]:
			#dat.append((cnumber[u]-r)/cnumber[u])
			data.append([u, cnumber[u]] + cdata[u] + [(cnumber[u] - rdata[u][p])/cnumber[u], p])
	return data


def saveData(sname, data):
	with open(sname, 'w') as f:
		writer = csv.writer(f, delimiter=',')
		header = ['name', 'core', 'mcd', 'cd', 'rmcd', 'rcd', 'delta_core', 'removed']
		writer.writerow(header)
		for d in data:
			writer.writerow(d)

if __name__ == '__main__':
	p_max = 25
	i_max = 100

	fname = sys.argv[1]
	sname = sys.argv[2]
	#p = int(sys.argv[3])

	graph = getGraph(fname)
	cnumber = coreNumber(graph)
	cdata = coreDegree(graph, cnumber)

	rdata = {u:{} for u in graph.nodes()}

	for p in xrange(1, p_max + 1):
		tdata = {u:[] for u in graph.nodes()}
		for x in xrange(0, i_max):
			print('Remove: {}\tIteration: {}'.format(p, x))
			cgraph = removeEdges(graph, p)
			tcnumber = coreNumber(cgraph)
			for u in tcnumber:
				tdata[u].append(tcnumber[u])
		
		for u in tdata:
			rdata[u][p] = np.mean(tdata[u])

	data = compileDate(cnumber, cdata, rdata)

	saveData(sname, data)