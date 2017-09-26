from __future__ import division, print_function
import networkx as nx
import numpy as np
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

def kcoreMat(mat):
	s = np.matrix([1]*len(mat))
	s = np.transpose(s)
	k = 0

	cnumber = {}
	candidates = range(0, len(mat))
	plen = len(candidates)

	while len(candidates) > 0:
		r = np.matmul(mat, s)
		remove = []
		for u in candidates:
			if r[u,0] == k or (s[u,0] > 0 and r[u,0] < k):
				cnumber[u] = k
				candidates.remove(u)
				s[u, 0] = 0

		if len(candidates) == plen:
			k += 1
		plen = len(candidates)
			
	return cnumber

def kcore(graph):
	g = graph.copy()
	cnumber = {u:0 for u in g.nodes()}
	#candidates = list(graph.nodes())
	k = 0
	while g.number_of_nodes() > 0:
		changed = False
		degree = g.degree()
		for u in g.nodes():
			cnumber[u] = k
			if degree[u] <= k:
				g.remove_node(u)
				changed = True
		if not changed:
			k += 1

	return cnumber

def checkCoreChangeMat(mat1, mat2, u, v, cnumber):
	kmin = min(cnumber[u], cnumber[v])
	#print('K min: {}'.format(kmin))
	#m1 = np.copy(mat)
	#m2 = np.copy(mat)

	m1 = mat1
	m2 = mat2

	m2[u,v] = 1
	m2[v,u] = 1

	for i in xrange(len(mat)-1, 0):
		if cnumber(i) < kmin:
			np.delete(m1, i, 0)
			np.delete(m1, i, 1)
			np.delete(m2, i, 0)
			np.delete(m2, i, 1)

	s1 = np.matrix([1]*len(m1))
	s1 = np.transpose(s1)
	s2 = np.copy(s1)
	
	c1 = {}
	c2 = {}
	k1 = kmin
	k2 = kmin
	kmax = kmin + 1

	can1 = range(0, len(m1))
	can2 = list(can1)

	while k1 <= kmax or k2  <= kmax:
	#while len(can1) > 0 or len(can2) > 0 :
		#pass
		changed1 = False
		changed2 = False

		r1 = np.matmul(m1, s1)
		r2 = np.matmul(m2, s2)
		#r1 = m1 * s1
		#r2 = m2 * s2
		#print(np.transpose(r1))
		#print(np.transpose(r2))
		if (r1 == r2).all():
			#print(1, k1, k2)
			return True
		if k1 <= kmax:
			for w in can1:
				if r1[w,0] == k1 or (s1[w,0] > 0 and r1[w,0] < k1):
					c1[w] = k1
					if w in c2 and c2[w] != c1[w]:
						#print(3)
						return False
					s1[w, 0] = 0
					can1.remove(w)
					changed1 = True
		if k2 <= kmax:
			for w in can2:
				if r2[w,0] == k2 or (s2[w,0] > 0 and r2[w,0] < k2):
					c2[w] = k2
					if w in c1 and c2[w] != c1[w]:
						#print(3)
						return False
					s2[w, 0] = 0
					can2.remove(w)
					changed2 = True

		if not changed1:
			k1 += 1
		if not changed2:
			k2 += 1
		#print(len(can1), len(can2))

	#print(c1)
	#print(c2)
	#c1 = np.array([c1[w] for w in c1])
	#c2 = np.array([c2[w] for w in c2])
	#print(c1)
	#print(c2)
	if np.array_equal(np.array(c1.values()), np.array(c2.values())):
		#print(2)
		return True
	return False
		


def checkCoreChange(graph, u, v, cnumber):
	g = graph.copy()
	kmin = min(cnumber[u], cnumber[v])

	for w in g.nodes():
		if cnumber[w] < kmin:
			g.remove_node(w)

	c1 = kcore(g)
	g.add_edge(u,v)
	c2 = kcore(g)
	
	for w in c1:
		if c1[w] != c2[w]:
			#print(w)
			return False

	g.remove_edge(u,v)

	return True

def checkCoreChangeBaseline(graph, u, v):
	c1 = nx.core_number(graph)
	graph.add_edge(u,v)
	c2 = nx.core_number(graph)

	for w in c1:
		if c1[w] != c2[w]:
			return False

	return True


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

	tpr = tp / (tp + fn)
	tnr = tn / (tn + fp)
	fpr = fp / (fp + tn)
	fnr = fn / (fn + tp)

	print('TPR: {} \t FPR: {} \t FNR: {} \t TNR: {}'.format(tpr, fpr, fnr, tnr))

if __name__ == '__main__':
	fname = sys.argv[1]

	graph = readGraph(fname)
	#graph = nx.karate_club_graph()
	
	g = nx.Graph()
	g.add_edge('a', 'b')
	g.add_edge('b', 'c')
	g.add_edge('a', 'c')
	g.add_edge('b', 'd')
	g.add_edge('d', 'e')
	g.add_edge('d', 'f')
	g.add_edge('e', 'f')

	mat = nx.to_numpy_matrix(graph)
	#nodes = graph.nodes()
	#nodes = {i:nodes[i] for i in xrange(0, len(nodes))}
	#cnumber = {i:0 for i in nodes}

	t1 = time.time()
	cnumber = kcoreMat(mat)
	t2 = time.time()
	print('Time Mat: {}'.format(t2-t1))

	t1 = time.time()
	dnumber = kcore(nx.from_numpy_matrix(mat))
	t2 = time.time()
	print('Time Nx: {}'.format(t2-t1))

	core_ground = nx.core_number(nx.from_numpy_matrix(mat))
	
	#cnumber = {nodes[u]:cnumber[u] for u in cnumber}
	#print(cnumber)

	checkCorrectness(cnumber, core_ground)
	checkCorrectness(dnumber, core_ground)

	edges = [(u,v) for u in xrange(0, len(mat)) for v in xrange(0, len(mat)) if not graph.has_edge(u,v) and u != v]
	np.random.shuffle(edges)
	edges = edges[:5]

	t = []
	mresults = []
	for e in edges:
		m1 = np.copy(mat)
		m2 = np.copy(mat)
		t1 = time.time()
		r = checkCoreChangeMat(m1, m2, e[0], e[1], cnumber)
		t.append(time.time() - t1)
		mresults.append(r)

	print(np.mean(t), np.std(t))

	t = []
	kresults = []
	for e in edges:
		t1 = time.time()
		r = checkCoreChange(nx.from_numpy_matrix(mat), e[0], e[1], cnumber)
		t.append(time.time() - t1)
		kresults.append(r)

	print(np.mean(t), np.std(t))

	baseline = []
	for e in edges:
		t1 = time.time()
		r = checkCoreChangeBaseline(nx.from_numpy_matrix(mat), e[0], e[1])
		t.append(time.time() - t1)
		baseline.append(r)

	print(np.mean(t), np.std(t))
	#print(edges)
	#print(mresults)
	#print(kresults)
	#print(baseline)

	performance(mresults, baseline)