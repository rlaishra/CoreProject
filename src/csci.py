from __future__ import division, print_function
import networkx as nx
import numpy as np
import sys
import os
import cPickle as pickle
import time
import csv
import scipy.stats as stats
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
		graph = nx.read_edgelist(fname, delimiter=',')
		
		if graph.number_of_edges() == 0:
			graph = nx.read_edgelist(fname, delimiter='\t')
		if graph.number_of_edges() == 0:
			graph = nx.read_edgelist(fname, delimiter=' ')

	graph.remove_edges_from(graph.selfloop_edges())
	#print(nx.info(graph))
	return graph


def _getSupportNodes(graph, cnumber, u):
	"""
	Get the list of neighbors of u with greater core number than u
	whose removal will affect the core number of u
	"""
	n = [v for v in graph.neighbors(u) if cnumber[v] == cnumber[u]]
	m = [v for v in graph.neighbors(u) if cnumber[v] > cnumber[u]]
		
	# Node u relies on higher nodes for its core number
	return n, m



def getCoreInfluence(cnumber, kcore):
	"""
	Compute the influence score for each nodes
	"""
	knumber = [cnumber[u] for u in cnumber]
	kmin = min(knumber)
	kmax = max(knumber)

	ci = {u:1.0 for u in nodes}
	cd = {u:0 for u in nodes}

	empty = []
	for k in xrange(kmin, kmax + 1):
		# Nodes in the kcore
		if k not in kcore:
			continue

		knodes = kcore[k].nodes()
		knodes = [u for u in knodes if cnumber[u] == k]

		for u in set(knodes).intersection(nodes):
			snodes, hnodes = _getSupportNodes(kcore[k], cnumber, u)

			cd[u] = 1 if len(snodes) >= cnumber[u] else 0
			
			if len(snodes) >= cnumber[u]:
				empty.append(u)
				continue

			dif = ci[u]*(cnumber[u] - len(snodes))/cnumber[u]
			#ci[u] = ci[u] - dif
			#dif = ci[u]
			share = dif / len(hnodes)
			for v in hnodes:
				ci[v] += share

	# Normalize so that sum is 1
	#total = sum(iScore.values())
	#imin = min(iScore.values())
	#imax = max(iScore.values())

	#for u in iScore:
	#	iScore[u] = iScore[u]/total
	#print(min(iScore.values()), max(iScore.values()))
	return ci


def getCoreStrength(graph, cnumber):
	data = {}
	m = graph.number_of_edges()

	for u in cnumber:
		neighbors = graph.neighbors(u)
		cd = len([v for v in neighbors if cnumber[u] <= cnumber[v]])
		data[u] = cd - cnumber[u]
		#data[u] = data[u]/m
		
	return data

def generateCoreSubgraph(graph, cnumber):
	cn = set(cnumber.values())
	core_subgraph = {}

	for c in cn:
		core_subgraph[c] = nx.k_core(graph, k = c, core_number=cnumber)

	return core_subgraph


def saveData(sname, data, n):
	if n:
		f = open(sname, 'w')
	else:
		f = open(sname, 'a')
	
	writer = csv.writer(f, delimiter=',')
	if n:
		writer.writerow(['type','name','ci_mean', 'cs_mean', 'ci_perc','cs_perc', 'cst_mean', 'cit_mean', 'k_shell', 'cr', 'cr_s', 'n'])
	
	for d in data:
		writer.writerow(d)


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
	#sl = sorted(x1, key=x1.get, reverse=True)
	#print(len(sl), k,  len(sl) * k / 100)
	th = 1
	if k < 100:
		th = sl[int(len(sl) * k / 100)]

	# Filter out nodes not in x2 from x1
	#print(len(x1))
	x1 = {u:x1[u] for u in x1 if u in x2}
	ind = [u for u in x1 if x1[u] > th]

	#print(len(x1))

	d1 = [x1[i] for i in ind] + [0]
	d2 = [x2[i] for i in ind] + [0]
	#print(d1)
	#print(d1)
	#print(d2)
	cor, _ = stats.kendalltau(d1, d2, nan_policy='omit')

	if np.isnan(cor):
		cor = 1
	return cor

def computeResilience(graph, exp, a = 0, mode='edges'):
	k = [25, 50, 100]
	p = range(0,26,5)

	results = {}

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

	 			if mode == 'edges':
		 			num = int(graph.number_of_edges()*y/(100 * (1 + a/100)))
		 			graph = removeEdges(graph, num)
		 		elif mode == 'nodes':
		 			num = int(graph.number_of_nodes()*y/(100 * (1 + a/100)))
		 			graph = removeNodes(graph, num)
		 		else:
		 			print('Incorrect Mode')
		 			return False

	 			ncn = coreNumber(graph, nodes)

	 			cor = compare(ocn, ncn, z)
	 			tdata.append(cor)
	 			#print(y, tdata)

	 		adata.append(np.mean(tdata))
	 		#print(tdata)
	 		x += 1
	 	results[z] = (np.mean(adata), np.std(adata))

	return results


if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]
	name = sys.argv[3]
	n = int(sys.argv[4]) == 1
	t = sys.argv[5] 			# Type of network
	mode = sys.argv[6]
	x = float(sys.argv[7])

	#k = 50

	# Generate nodes list
	graph = readGraph(fname)
	node_count = graph.number_of_nodes()
	print(nx.info(graph))
	cnumber = nx.core_number(graph)
	#cutoff = sorted(cnumber.values(), reverse=True)[int(len(cnumber)*k/100)]
	#print('Cutoff', cutoff)
	cutoff = 0
	nodes = [u for u in graph.nodes() if cnumber[u] > cutoff]

	cnumber = nx.core_number(graph)
	kcore = generateCoreSubgraph(graph, cnumber)

	#graph = graph.subgraph(nodes)
	ci = getCoreInfluence(cnumber, kcore)
	cs = getCoreStrength(graph, cnumber)
	results = computeResilience(graph, 10, x, mode)

	# Means
	ci_mean = np.mean(ci.values())
	cs_mean = np.mean(cs.values())

	# Medians
	ci_mean = len([u for u in ci if ci[u] > ci_mean])/node_count
	#cs_mean = np.var(ci.values())

	ci_perc = np.percentile(ci.values(),95)
	cs_perc = np.percentile(cs.values(),95)

	data = [t, name, ci_mean, cs_mean, ci_perc, cs_perc]

	print('CS: {} {}'.format(cs_mean, cs_perc))
	print('CI: {} {}'.format(ci_mean, ci_perc))
	print('Resilience', results)

	#print('CI \t 75: {} \t 90: {} \t 95: {} \t Mean: {}'.format(np.percentile(iScore.values(), 75),np.percentile(iScore.values(), 90),np.percentile(iScore.values(), 95), np.mean(iScore.values())))
	#print('CS \t 75: {} \t 90: {} \t 95: {} \t Mean: {}'.format(np.percentile(rcd.values(), 75),np.percentile(rcd.values(), 90),np.percentile(rcd.values(), 95), np.mean(rcd.values())))

	# Mean CS of top 95 percentile CI
	ci_th = np.percentile(ci.values(), 95)
	#nod = [ci[u] for u in ci if ci[u] > ci_th]
	nod = [u for u in ci if ci[u] > ci_th]
	cs_t = [cs[u] for u in nod]
	cs_m = np.mean(cs_t)
	print('Top 5% CI CS: {} {}'.format(np.mean(cs_t), np.std(cs_t)))

	#cs_th = np.percentile(cs.values(), 95)
	#nod = [u for u in cs if cs[u] > cs_th]
	ci_t = [ci[u] for u in ci if ci[u] > ci_th]
	ci_m = np.mean(ci_t)/np.mean(ci.values())
	ci_s = np.std(ci_t)
	print('Top 5% CS CI: {} {}'.format(np.mean(ci_t), np.std(ci_t)))
	
	data += [cs_m, ci_m]

	# Number of k-shells
	data += [len(set(cnumber.values()))]

	d = []
	for k in results:
		d.append(data + [results[k][0], results[k][1],k])
	
	saveData(sname, d, n)


