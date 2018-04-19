"""
The natural connectivity of graphs as defined in
Jun, W. U., et al. "Natural connectivity of complex networks." Chinese physics letters 27.7 (2010): 078902.
"""

from __future__ import division, print_function

import sys
import csv
import random
import scipy.stats as stats
import numpy as np 
import networkx as nx
import scipy as sp


def readGraph(fname, k=None):
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
	if k is not None:
		graph = getSubgraph(graph, k)
	return graph


def getSubgraph(graph, n=0.5):
	core = nx.core_number(graph)
	core = sorted(core.values(), reverse=True)
	k = core[int(len(core) * n)]
	return nx.k_core(graph, k)


def compareRanking(x1, x2):
	common = set(x1.keys()).intersection(x2.keys())
	y1 = []
	y2 = []
	for u in common:
		y1.append(x1[u])
		y2.append(x2[u])

	cor, _ = stats.kendalltau(y1, y2, nan_policy='omit')

	return cor


def computeResilience(fname):
	step = 10
	p = range(0, 51, step)

	adata = []

	for _ in xrange(0, 10):
		graph = readGraph(fname)
		num = int(graph.number_of_nodes()*step/100)
	 	ocn = nx.core_number(graph)
	 	
	 	tdata = []
	 	for y in p:
	 		nodes = graph.nodes()
	 		random.shuffle(nodes)
	 		nodes = nodes[:num]
		 	redges = []
			for u in nodes:
				redges += list([(u,v) for v in graph.neighbors(u)])
			graph.remove_edges_from(redges)

	 		ncn = nx.core_number(graph)
	 		cor = compareRanking(ocn, ncn)
	 		tdata.append(cor)

	 	adata.append(np.mean(tdata))

	return np.mean(adata)


def getRobustnenssScore(fname, t):
	"""
	Natural Connectivity
	"""
	graph = readGraph(fname, t)
	mat = nx.to_numpy_matrix(graph)
	w = sp.linalg.eigvalsh(mat)
	s = [np.exp(x) for x in w]
	return np.log(np.mean(s))


def saveData(sname, connectivity, resilience, dname, tname):
	with open(sname, 'a') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow([connectivity, resilience, dname, tname])
		f.close()

if __name__ == '__main__':
	sname = sys.argv[1]

	fname = [
	 'data/as-733/as19971108.txt',
	 'data/as-733/as19990309.txt',
	 'data/oregon1_010331.txt',
	 'data/oregon1_010428.txt',
	 'data/bio-dmela/bio-dmela.mtx',
	 'data/bio-yeast-protein-inter/bio-yeast-protein-inter.edges',
	 'data/grqc.csv',
	 'data/ca-HepTh.csv',
	 'data/ca-Erdos992/ca-Erdos992.mtx',
	 'data/inf-openflights/inf-openflights.edges',
	 'data/inf-power/inf-power.mtx',
	 'data/inf-USAir97/inf-USAir97.csv',
	 'data/p2p-Gnutella08.csv',
	 'data/p2p-Gnutella09.csv',
	 'data/soc-hamsterster/soc-hamsterster.edges',
	 'data/soc-advogato/soc-advogato.csv',
	 'data/soc-wiki-Vote/soc-wiki-Vote.mtx',
	 'data/tech-pgp/tech-pgp.edges',
	 'data/tech-routers-rf/tech-routers-rf.mtx',
	 'data/tech-WHOIS/tech-WHOIS.mtx',
	 'data/web-spam/web-spam.mtx'
	]

	tname = [
	 'AS', 'AS', 'AS', 'AS', 'BIO', 'BIO', 'CA', 'CA', 'CA', 'INF', 'INF', 'INF', 'P2P', 'P2P', 'SOC', 'SOC', 'SOC', 'TECH', 'TECH', 'TECH', 'WEB'
	]

	for i in xrange(0, len(fname)):
		connectivity = getRobustnenssScore(fname[i], 0.10)
		resilience = computeResilience(fname[i])
		saveData(sname, connectivity, resilience, fname[i], tname[i])
		print(fname[i], connectivity, resilience)

