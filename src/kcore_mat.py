from __future__ import division, print_function
import networkx as nx
import numpy as np
from scipy.sparse import csr_matrix
from scipy import sparse
import sys
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

def kcoreMat(mat, l):
	s = np.matrix([1]*l)
	s = np.transpose(s)
	k = 0

	cnumber = {}
	candidates = set(range(0, l))

	while len(candidates) > 0:
		r = mat.dot(s)

		can = np.where(s <= 0)[0]
		r[can, 0] = k + 1
		can = np.where(r <= k)[0]
		
		if len(can) == 0:
			k += 1
			continue
		
		for u in can:
			cnumber[u] = k
	
		s[can, 0] = 0
		candidates.difference_update(can)
		
	return cnumber

def kcore(graph):
	cnumber = {u:0 for u in graph.nodes()}
	k = 0
	while g.number_of_nodes() > 0:
		remove = []
		changed = False
		degree = nx.degree(graph)
		for u in graph.nodes():
			cnumber[u] = k
			if degree[u] <= k:
				remove.append(u)
				changed = True
		graph.remove_nodes_from(remove)
		if not changed:
			k += 1

	return cnumber

def checkCoreChangeMat(mat, edges, cnumber):
	nodes = []
	for e in edges:
		nodes.append(e[0])
		nodes.append(e[1])
	nodes = set(nodes)
	cn = [cnumber[u] for u in nodes]
	kmin = min(cn)
	kmax = max(cn)

	for e in edges:
		mat[e[0],e[1]] = 1
		mat[e[1],e[0]] = 1

	rem = [i for i in cnumber if cnumber[i] < kmin]
	mat = np.delete(mat, rem, 0)
	mat = np.delete(mat, rem, 1)
	
	s = np.matrix([1]*len(mat))
	s = np.transpose(s)
	
	k = kmin
	
	mat = sparse.csr_matrix(mat)
	changed = []

	while k  < kmax:
		r = mat.dot(s)
		can = np.where(s <= 0)[0]
		r[can, 0] = k + 1
		can = np.where(r <= k)[0]

		if len(can) == 0:
			k += 1
			continue
		
		for u in can:
			if k != cnumber[u]:
				changed.append(u)
		
		s[can, 0] = 0

	whitelist = [] 		# Edges that does not change core number
	blacklist = []		# Edges that changes core number

	for e in edges:
		if e[0] not in changed and e[1] not in changed:
			whitelist.append(e)
		elif e[0] in changed and cnumber[e[0]] > cnumber[e[1]]:
			whitelist.append(e)
		elif e[1] in changed and cnumber[e[1]] > cnumber[e[0]]:
			whitelist.append(e)
	blacklist = [e for e in edges if e not in whitelist]
	#print(len(whitelist), len(blacklist), len(edges))

	return whitelist, blacklist
		

def checkCoreChange(graph, u, v, cnumber):
	kmin = min(cnumber[u], cnumber[v])

	remove = []
	for w in g.nodes():
		if cnumber[w] < kmin:
			remove.append(g)
	graph.remove_nodes_from(remove)

	c1 =np.array([cnumber[w] for w in graph.nodes()])

	g.add_edge(u,v)
	c2 = kcore(g)
	c2 = np.array(c2.values())

	if np.array_equal(c1, c2):
		return True

	return False

def checkCoreChangeBaseline(graph, u, v):
	kmin = min(cnumber[u], cnumber[v])

	remove = []
	for w in g.nodes():
		if cnumber[w] < kmin:
			remove.append(g)
	graph.remove_nodes_from(remove)

	c1 =np.array([cnumber[w] for w in graph.nodes()])
	
	graph.add_edge(u,v)
	c2 = nx.core_number(graph)
	c2 = np.array(c2.values())

	if np.array_equal(c1, c2):
		return True

	return False


def checkCorrectness(c1, c2):
	ic = 0
	for u in c1:
		if c1[u] != c2[u]:
			ic += 1
	print('Incorrect: {}/{}'.format(ic, len(c1)))
	return True

def performance(pred, ground):
	tp = 0
	tn = 0
	fp = 0
	fn = 0

	for i in xrange(0, len(pred)):
		if pred[i] and ground[i]:
			tp += 1
		elif pred[i] and not ground[i]:
			fp += 1
		elif not pred[i] and ground[i]:
			fn += 1
		elif not pred[i] and not ground[i]:
			tn += 1

	print('TP: {} \t FP: {} \t FN: {} \t TN: {}'.format(tp, fp, fn, tn))

def edgeGroups(edges, cnumber):
	# Set of edges where the endpoints have same core number
	sim = [e for e in edges if cnumber[e[0]] == cnumber[e[1]]]
	# Set of edges where the endpoints do not have same core number
	dis = [e for e in edges if e not in sim]

	# Set of edges involving a node
	node_edges = {}
	for e in sim:
		if e[0] not in node_edges:
			node_edges[e[0]] = []
		if e[1] not in node_edges:
			node_edges[e[1]] = []

		node_edges[e[0]].append(e)
		node_edges[e[1]].append(e)

	dis_el = []
	sim_el = []
	
	while len(sim) > 0:
		nodes = set([])
		sl = []
		for e in sim:
			if e[0] not in nodes and e[1] not in nodes:
				sl.append(e)
				nodes.update([e[0], e[1]])
		sim_el.append(sl)
		sim = [e for e in sim if e not in sl]

	while len(dis) > 0:
		nodes = set([])
		kmin = np.inf
		kmax = 0
		sl = []
		for e in dis:
			if e[0] not in nodes and e[1] not in nodes:
				sl.append(e)
				nodes.update([e[0], e[1]])
			elif e[0] in nodes:
				if cnumber[e[1]] < min([min(cnumber[f[0]], cnumber[f[1]]) for f in sl]):
					sl.append(e)
					nodes.update([e[0], e[1]])
				if cnumber[e[1]] > max([max(cnumber[f[0]], cnumber[f[1]]) for f in sl]):
					sl.append(e)
					nodes.update([e[0], e[1]])
			elif e[1] in nodes:
				if cnumber[e[0]] < min([min(cnumber[f[0]], cnumber[f[1]]) for f in sl]):
					sl.append(e)
					nodes.update([e[0], e[1]])
				if cnumber[e[0]] > max([max(cnumber[f[0]], cnumber[f[1]]) for f in sl]):
					sl.append(e)
					nodes.update([e[0], e[1]])
		dis_el.append(sl)
		dis = [e for e in dis if e not in sl]

	el = sim_el + dis_el

	return el

if __name__ == '__main__':
	n1 = 100
	n2 = 1000

	fname = sys.argv[1]
	sname = sys.argv[2]
	name = sys.argv[3]
	header = int(sys.argv[4]) == 1

	graph = readGraph(fname)
	
	sdata = []
	sdata.append(name)
	sdata.append(graph.number_of_nodes())
	sdata.append(graph.number_of_edges())
	sdata.append(2*graph.number_of_edges()/graph.number_of_nodes())
	sdata.append(1 - 2*graph.number_of_nodes()/graph.number_of_nodes()**2)

	print('Sparsity: {}'.format(1 - 2*graph.number_of_nodes()/graph.number_of_nodes()**2))

	mat = nx.to_numpy_matrix(graph)
	t = []
	for _ in xrange(0, n1):
		m = sparse.csr_matrix(mat)
		t1 = time.time()
		cnumber = kcoreMat(m, len(mat))
		t.append(time.time() - t1)
	print('Time Mat: {} {}'.format(np.mean(t), np.std(t)))
	sdata.append(np.mean(t))

	t = []
	for _ in xrange(0, n1):
		g = nx.from_numpy_matrix(mat)
		t1 = time.time()
		dnumber = kcore(g)
		t.append(time.time() - t1)
	print('Time Nor: {} {}'.format(np.mean(t), np.std(t)))
	sdata.append(np.mean(t))


	t = []
	for _ in xrange(0, n1):
		g = nx.from_numpy_matrix(mat)
		t1 = time.time()
		core_ground = nx.core_number(g)
		t.append(time.time() - t1)
	print('Time Ground: {} {}'.format(np.mean(t), np.std(t)))
	sdata.append(np.mean(t))
	
	#cnumber = {nodes[u]:cnumber[u] for u in cnumber}
	#print(cnumber)

	checkCorrectness(cnumber, core_ground)
	checkCorrectness(dnumber, core_ground)

	#n1 = np.random.randint(0, len(mat), size=min(len(mat), n2))
	#n2 = np.random.randint(0, len(mat), size=min(len(mat), n2))
	edges = [(u,v) for u in xrange(0, len(mat)) for v in xrange(0, len(mat)) if not graph.has_edge(u,v) and u != v]
	np.random.shuffle(edges)
	edges = edges[:n2]
	print('Edges selected')

	t = []
	mresults = [False]*len(edges)
	t1 = time.time()
	el = edgeGroups(edges, cnumber)
	t.append(time.time() - t1)
	for e in el:
		m = np.copy(mat)
		t1 = time.time()
		whitelist, blacklist = checkCoreChangeMat(m, e, cnumber)
		t.append(time.time() - t1)
		for u in whitelist:
			i = edges.index(u)
			mresults[i] = True
	#print(mresults)
	print('Time mat: {}'.format(np.sum(t)/len(edges)))
	sdata.append(np.sum(t)/len(edges))

	t = []
	kresults = []
	for e in edges:
		g = nx.from_numpy_matrix(mat)
		t1 = time.time()
		r = checkCoreChange(g, e[0], e[1], cnumber)
		t.append(time.time() - t1)
		kresults.append(r)

	print('Time normal: {}'.format(np.mean(t)))
	sdata.append(np.sum(t)/len(edges))
	
	t = []
	baseline = []
	for e in edges:
		g = nx.from_numpy_matrix(mat)
		t1 = time.time()
		r = checkCoreChangeBaseline(g, e[0], e[1])
		baseline.append(r)
		t.append(time.time() - t1)
		kresults.append(r)
	#print(baseline)
	print('Time baseline: {}'.format(np.mean(t)))
	sdata.append(np.sum(t)/len(edges))

	#print(edges)
	#print(mresults)
	#print(kresults)
	#print(baseline)

	#performance(mresults, baseline)

	# Save results
	with open(sname, 'a') as f:
		writer = csv.writer(f, delimiter=',')
		if header:
			writer.writerow(['name','nodes','edges','degree','sparsity','mat_dec','nor_dec','nx_dec','mat_cha','nor_cha','nx_cha'])
		writer.writerow(sdata)

