"""
Add edges between the high core number nodes to improve the robustness
"""

from __future__ import division, print_function
import networkx as nx
import numpy as np
import sys
import os
import cPickle as pickle
import time
import csv
from scipy.sparse import csr_matrix
from scipy import sparse
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

def computeMCD(graph, cnumber, nodes=None):
	mcd = {}
	if nodes is None:
		nodes = graph.nodes()
	for u in nodes:
		mcd[u] = 0
		n = graph.neighbors(u)
		for v in n:
			if cnumber[u] <= cnumber[v]:
				mcd[u] += 1

	return mcd

def updateMCD(graph, cnumber, mcd, e):
	"""
	Update the MCD of nodes after edge e has been added
	"""
	u = e[0]
	v = e[1]

	if cnumber[u] > cnumber[v]:
		mcd[v] += 1
	elif cnumber[v] > cnumber[u]:
		mcd[u] += 1
	elif cnumber[u] == cnumber[v]:
		mcd[u] += 1
		mcd[v] += 1
	return mcd

def updatePureCore(graph, cnumber, mcd, pc, e):
	"""
	Update the pure core of all affected nodes on adding edge e

	Returns new pc, and list of nodes whose pc have been changed
	"""
	e = list(e)
	u = e[0]
	v = e[1]

	if cnumber[u] != cnumber[v]:
		return pc

	changed = []
	if mcd[u] > cnumber[v]:
		t = findPureCore(graph, cnumber, mcd, v)
		if pc[v] != t:
			changed.append(v)
			pc[v] = t
	if mcd[v] > cnumber[u]:
		t = findPureCore(graph, cnumber, mcd, u)
		if pc[u] != t:
			changed.append(u)
			pc[u] = t

	for w in pc[u]:
		if mcd[v] > cnumber[w]:
			t = findPureCore(graph, cnumber, mcd, w)
			if pc[w] != t:
				changed.append(w)
				pc[w] = t

	for w in pc[v]:
		if mcd[u] > cnumber[w]:
			t = findPureCore(graph, cnumber, mcd, w)
			if pc[w] != t:
				changed.append(w)
				pc[w] = t

	return pc

def findPureCore(graph, cnumber, mcd, u):
	"""
	Find the pure core of node u 
	"""
	# Core number condition
	#if candidates is None:
	#	candidates = cnumber.keys()

	nodes = [v for v in cnumber if cnumber[v] == cnumber[u]]

	# MCD condition
	nodes = [v for v in nodes if mcd[v] > cnumber[u]]
	
	# Reachability condition
	nodes.append(u) 				# u inserted to check for reachabilty
	nodes = set(nodes)

	sg = graph.subgraph(nodes)
	cc = nx.connected_components(sg)

	for cm in cc:
		if u in cm:
			cm.remove(u)
			return cm
				
	return set([])
	

def generatePureCore(graph, cnumber, mcd, nodes=None):
	pc = {}
	
	if nodes is None:
		nodes = graph.nodes()

	for u in nodes:
		pc[u] = findPureCore(graph, cnumber, mcd, u)
	
	return pc


def updateCoreStrength(graph, cnumber, cs, edge):
	nodes  = [u for u in cs if e in edge]
	csn = getCoreStrength(graph, cnumber, nodes, normalize=False)

	for u in csn:
		cs[u] = csn[u]

	return cs

def getCoreStrength(graph, cnumber, nodes=None):
	data = {}

	if nodes is None:
		nodes = graph.nodes()

	for u in nodes:
		neighbors = graph.neighbors(u)
		cd = len([v for v in neighbors if cnumber[u] <= cnumber[v]])
		data[u] = cd - cnumber[u]

	smax = max(data.values())
	smin = min(data.values())

	for u in data:
		data[u] = (data[u] - smin)/(smax - smin)

	return data


def _getSupportNodes(graph, cnumber, u):
	"""
	Get the list of neighbors of u with greater core number than u
	whose removal will affect the core number of u
	"""
	n = [v for v in graph.neighbors(u) if cnumber[v] == cnumber[u]]
	m = [v for v in graph.neighbors(u) if cnumber[v] > cnumber[u]]

	# Node u relies on higher nodes for its core number
	return n, m

def updateCoreInfluence(graph, cnumber, kcore, ci, cd, edge):
	kmin = min(cnumber[e[0]], cnumber[e[1]])
	kmax = max(cnumber.values())

	nodes = [u for u in ci if u in edge and cnumber[u] == kmin]

	for k in xrange(kmin + 1, kmax + 1):
		cand = []
		for u in nodes:
			cand += [v for v in graph.neighbors(u) if cnumber[v] > cnumber[u]]

		nodes = []
		cand = set(cand)
		for u in cand:
			supNodes = _getSupportNodes(kcore[k], cnumber, u)
			cd[u] = 1 if len(supNodes) > 0 else 0
			if len(supNodes) < 1:
				empty.append(u)
				continue

			share = ci[u]/len(supNodes)
			for v in supNodes:
				ci[v] += share
				nodes.append(v)

		nodes = list(set(nodes))

	return ci

def _ciPriority(ci, cnumber, kcore, cd, u, v, n, m):
	"""
	Returns the combined decrease in ci of higher core number nodes
	if u and v are connected
	"""

	if cnumber[u] == cnumber[v]:
		s1 = [ci[x] for x in n[u] ] + [ci[x] for x in m[u]]
		s2 = [ci[x] for x in n[v] ] + [ci[x] for x in m[v]]

		return np.mean(s1) + np.mean(s2)

		delta = []
		if cnumber[u] > len(n[u]):
			s1 += cd[u] - ci[u]
			s1 -= cd[u] - cd[u] * (len(n[u]) + 1) / cnumber[u]
			delta += [x for x in m[u]]
			#s1 = s1 / len(m[u])
			#print(s1)
			#s1 = s1 * np.mean([ci[x] for x in m[u]])
		if cnumber[v] > len(n[v]):
			s2 += cd[v] - ci[v]
			s2 -= cd[v] - cd[v] * (len(n[v]) + 1) / cnumber[v]
			delta += [x for x in m[v]]
			#s2 = s2 / len(m[v])
			#print(s2)
			#s2 = s2 * np.mean([ci[x] for x in m[v]])
		#print(s1 + s2)
		#if u == 651 and v == 2044:
		#	print('same', u, v, cnumber[u], n[u], n[v], m[u], m[v], ci[u], ci[v], cd[u], cd[v], s1, s2)
		s = s1 + s2

		if len(delta) > 0:
			s = s * np.mean([cd[x] for x in set(delta)])
		return s

	if cnumber[u] < cnumber[v]:
		s = [ci[x] for x in n[u] ] + [ci[x] for x in m[u]]
		return np.mean(s)

	if cnumber[u] > cnumber[v]:
		s = [ci[x] for x in n[v] ] + [ci[x] for x in m[v]]
		return np.mean(s)

	return 0

	if cnumber[u] < cnumber[v] and cnumber[u] > len(n[u]) and len(m[u]) > 0:
		s = 0
		s += (cd[u] - ci[u])/len(m[u])
		s -= (cd[u] - ci[u])/(len(m[u]) + 1)
		#s = s * np.mean([ci[x] for x in m[u]])

		mvals = []
		for x in m[u]:
			mvals.append((cd[x] - s)*len(n[x])/cnumber[x])

		vval = (cd[v] + s) * len(n[v])/cnumber[v]

		if max(mvals) > vval:
			return s * np.mean([cd[x] for x in m[u]])
		else:
			return 0

	if cnumber[u] > cnumber[v] and cnumber[v] > len(n[v]) and len(m[v]) > 0:
		s = 0
		s += (cd[v] - ci[v])/len(m[v])
		s -= (cd[v] - ci[v])/(len(m[v]) + 1)
		#s = s * np.mean([ci[x] for x in m[v]])
		
		mvals = []
		for x in m[v]:
			mvals.append((cd[x] - s)*len(n[x])/cnumber[x])

		vval = (cd[u] + s) * len(n[u])/cnumber[u]

		if max(mvals) > vval:
			return s * np.mean([cd[x] for x in m[v]])
		else:
			return 0
	
	return 0


def getCoreInfluence(cnumber, kcore, nodes=None):
	"""
	Compute the influence score and core influence delta for each nodes
	"""
	if nodes is None:
		nodes = cnumber.keys()

	#if changed is None:
	#	changed = nodes

	knumber = [cnumber[u] for u in nodes]
	kmin = min(knumber)
	kmax = max(knumber)

	ci = {u:1.0 for u in nodes}
	cd = {u:0.0 for u in nodes}

	empty = []
	for k in xrange(kmin, kmax + 1):
		# Nodes in the kcore
		knodes = kcore[k].nodes()
		knodes = [u for u in knodes if cnumber[u] == k]

		#print(len(knodes), k)

		for u in set(knodes).intersection(nodes):
			snodes, hnodes = _getSupportNodes(kcore[k], cnumber, u)
			cd[u] = float(ci[u])
			#if u == 651:
			#	print(cd[u], ci[u])
			#cd[u] = 1 if len(snodes) >= cnumber[u] else 0

			#if u == 651 or u == 2044:
			#	print(u, cnumber[u], len(snodes), len(hnodes), cd[u])
		
			if len(snodes) >= cnumber[u]:
				empty.append(u)
				continue
			if len(hnodes) > 0:	
				dif = ci[u]*(cnumber[u] - len(snodes))/cnumber[u]
				#print(dif)
				#ci[u] = ci[u] - dif
				share = dif / len(hnodes)

				#if u == 651:
				#	print(cd[u], ci[u], dif)
				#print(cnumber[u], len(snodes), len(hnodes), ci[u], dif, cd[u], share)
				for v in hnodes:
					ci[v] += share
					#if v == 651:
					#	print('added',cd[651], ci[651], cnumber[651], cnumber[u], k)

			#if u == 651 or u == 2044:
			#	print(u, cnumber[u], len(snodes), len(hnodes), cd[u], ci[u], dif)
			#print(cd[u], ci[u])

	# Normalized sum to 1
	#total = sum(ci.values())
	#for u in ci:
	#	ci[u] = ci[u]/total

	# Normalize between 0-1
	#imin = min(ci.values())
	#imax = max(ci.values())

	#if imin == imax:
	#	return iScore

	#for u in ci:
	#	ci[u] = (ci[u]-imin)/(imax - imin)
	
	#print('Core Influence: {}'.format(len(empty)))
	#print('last', cd[651], ci[651])
	return ci, cd


def baselinePriority(nedges, cnumber, degree, mode='random'):
	nedges = list(nedges)
	if mode == 'random':
		np.random.shuffle(nedges)
		return nedges
	if mode == 'degree':
		priority = {}
		for e in nedges:
			u = e[0]
			v = e[1]
			priority[e] = 0.5 * (degree[u] + degree[v])
		edges = sorted(priority, key=priority.get, reverse=True)
		return edges
	if mode == 'core':
		priority = {}
		for e in nedges:
			u = e[0]
			v = e[1]
			priority[e] = 0.5 * (cnumber[u] + cnumber[v])
		edges = sorted(priority, key=priority.get, reverse=True)
		return edges


def edgePriority(nedges, cnumber, cs, ci, cd, kcore, mode='alg_edge'):
	priority = {}
	epsilon = 0.001
	
	if mode == 'alg_edge':
		for e in nedges:
			e = list(e)
			u = e[0]
			v = e[1]
			if u in cs and v in cs:
				if cnumber[u] < cnumber[v]:
					priority[(u,v)] = ci[u]/(cs[u] + epsilon)
				elif cnumber[u] > cnumber[v]:
					priority[(u,v)] = ci[v]/(cs[v] + epsilon)
				else:
					priority[(u,v)] = ci[u]/(cs[u] + epsilon) + ci[v]/(cs[v] + epsilon)
	elif mode == 'alg_node':

		n = {}
		m = {}

		for u in cnumber:
			n[u], m[u] = _getSupportNodes(kcore[cnumber[u]], cnumber, u)

			#if u == 651 or u == 2044:
			#	print(u, cnumber[u], n[u], m[u])

		for e in nedges:
			e = list(e)
			u = e[0]
			v = e[1]

			#if u == 651 or u == 2044:
			#	print(u, cnumber[u], n[u], m[u], ci[u], cd[u], cs[u])

			priority[(u,v)] = _ciPriority(ci, cnumber, kcore, cd, u, v, n, m)

			#if pr > 0:
			#	priority[(u,v)] = pr

			"""
			if cnumber[u] < cnumber[v]:
				if cd[u] > 0:
					priority[(u,v)] = cd[u]
			elif cnumber[v] < cnumber[u]:
				if cd[v] > 0:
					priority[(u,v)] = cd[v]
			elif cnumber[u] == cnumber[v]:
				if cd[u] > 0 and cd[v] > 0:
					priority[(u,v)] = cd[v] + cd[u]
			"""
			
			
			#print(ci[v], ci[u], cd[v], cd[u])

	edges = sorted(priority, key=priority.get, reverse=True)
	
	print('Prioritiy', priority[edges[0]], edges[0], cnumber[edges[0][0]], cnumber[edges[0][1]])
	return edges


def checkCoreChangeMat(mat, edges, cnumber):
	nodes = []
	for e in edges:
		nodes.append(e[0])
		nodes.append(e[1])
	cn = {nodes[i]:cnumber[nodes[i]] for i in xrange(0, len(nodes))}
	nodes = set(nodes)
	kmin = min(cn.values())
	kmax = max(cn.values())

	for e in edges:
		mat[e[0],e[1]] = 1
		mat[e[1],e[0]] = 1

	rem = [i for i in cnumber if cnumber[i] < kmin]
	mat = np.delete(mat, rem, 0)
	mat = np.delete(mat, rem, 1)

	s = np.matrix([1]*len(mat))
	s = np.transpose(s)
	
	k = kmin
	m = sparse.csr_matrix(mat)
	changed = set([])

	while k  < kmax:
		r = m.dot(s)
		can = np.where(s <= 0)[0]
		r[can, 0] = k + 1
		can = np.where(r <= k)[0]

		if len(can) == 0:
			k += 1
			continue
		
		s[can, 0] = 0
		can = nodes.intersection(can)
		
		for u in can:
			if k != cn[u]:
				changed.update([u])

	whitelist = [] 		# Edges that does not change core number
	#blacklist = []		# Edges that changes core number

	for e in edges:
		if e[0] not in changed and e[1] not in changed:
			whitelist.append(e)
		elif e[0] in changed and e[1] not in changed and cnumber[e[0]] > cnumber[e[1]]:
			whitelist.append(e)
		elif e[1] in changed and e[0] not in changed and cnumber[e[1]] > cnumber[e[0]]:
			whitelist.append(e)
	#blacklist = [e for e in edges if e not in whitelist]
	#print(len(whitelist), len(blacklist), len(edges))

	return whitelist

def edgeGroups(edges, cnumber, graph, pc):	
	# Set of edges where the endpoints have same core number
	sim = set([e for e in edges if cnumber[e[0]] == cnumber[e[1]]])
	# Set of edges where the endpoints do not have same core number
	dis = set([e for e in edges if e not in sim])

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
		spc = set([])
		scn = set([])
		for e in sim:
			if (cnumber[e[0]] not in scn and cnumber[e[1]] not in scn)\
			 or (e[0] not in spc and e[1] not in spc):
				sl.append(e)
				nodes.update([e[0], e[1]])
				scn.update([cnumber[e[0]], cnumber[e[1]]])
				spc.update(pc[e[0]])
				spc.update(pc[e[1]])
		sim_el.append(sl)
		#sim = [e for e in sim if e not in sl]
		sim.difference_update(sl)

	while len(dis) > 0:
		nodes = set([])
		sl = []
		spc = set([])
		scn = {}
		for e in dis:
			if (cnumber[e[0]] not in scn and cnumber[e[1]] not in scn)\
			 or (e[0] not in spc and e[1] not in spc):
				sl.append(e)
				nodes.update([e[0], e[1]])
				scn[e[0]] = [cnumber[e[1]]]
				scn[e[1]] = [cnumber[e[0]]]
				spc.update(pc[e[0]])
				spc.update(pc[e[1]])
			elif e[0] in nodes and len(scn[e[0]]) < 2:
				if cnumber[e[0]] < cnumber[e[1]] and cnumber[e[0]] > max(scn[e[0]]):
					sl.append(e)
					nodes.update([e[0], e[1]])
					scn[e[0]].append(cnumber[e[1]])
					scn[e[1]] = [cnumber[e[0]]]
					spc.update(pc[e[0]])
					spc.update(pc[e[1]])
				elif cnumber[e[0]] > cnumber[e[1]] and cnumber[e[0]] < min(scn[e[0]]):
				#elif cnumber[e[1]] > max(scn):
					sl.append(e)
					nodes.update([e[0], e[1]])
					scn[e[0]].append(cnumber[e[1]])
					scn[e[1]] = [cnumber[e[0]]]
					spc.update(pc[e[0]])
					spc.update(pc[e[1]])
			elif e[1] in nodes and len(scn[e[1]]) < 2:
				if cnumber[e[1]] < cnumber[e[0]] and cnumber[e[1]] > max(scn[e[1]]):
				#if cnumber[e[0]] < min(scn):
					sl.append(e)
					nodes.update([e[0], e[1]])
					scn[e[1]].append(cnumber[e[0]])
					scn[e[0]] = [cnumber[e[1]]]
					spc.update(pc[e[0]])
					spc.update(pc[e[1]])
				#if cnumber[e[0]] > max(scn):
				elif cnumber[e[1]] > cnumber[e[0]] and cnumber[e[1]] < min(scn[e[1]]):
					sl.append(e)
					nodes.update([e[0], e[1]])
					scn[e[1]].append(cnumber[e[0]])
					scn[e[0]] = [cnumber[e[1]]]
					spc.update(pc[e[0]])
					spc.update(pc[e[1]])
		dis_el.append(sl)
		#dis = [e for e in dis if e not in sl]
		dis.difference_update(sl)

	el = sim_el + dis_el

	print('Edge Groups', len(el), len(sim_el), len(dis_el))

	return el


def _checkIfCoreNumberChange(graph, cnumber, e):
	"""
	Add edge and check if core number change

	Returns true if change, false otherwise
	"""
	u = e[0]
	v = e[1]

	if graph.has_edge(u,v):
		print('Exist', u,v)
		return True

	graph.add_edge(u, v)
	tcore = nx.core_number(graph)
	graph.remove_edge(u, v)

	if tcore[u] == cnumber[u] and tcore[v] == cnumber[v]:
		return False

	#print([(carray[u], tcore[u]) for u in carray])
	return True


def updateCandidateEdges(graph, nedges, cnumber, pc, edge):
	"""
	Remove edges from nedges that will change core number.
	nedges is are the edges before adding new edge 'edge'
	"""
	# The edges to keep
	# If an edge do not have any endpoints in new added edge, keep it
	edgesk = set([e for e in nedges if e[0] not in edge and e[1] not in edge])

	print('Unchanged edges: {} of {}'.format(len(edgesk), len(nedges)))

	# Edges to check
	edgesc = set(nedges).difference(edgesk)
	edgesc = pruneCandidateEdges(graph, edgesc, cnumber, pc)

	# Combine sets
	edges = edgesk.union(edgesc)
	print('Before pruning: {}\t After pruning: {}'.format(len(nedges), len(edges)))

	return edges


def pruneCandidateEdges(graph, nedges, cnumber, pc):
	"""
	Remove the edges which will change core number
	"""

	mat = nx.to_numpy_matrix(graph)
	#mat = sparse.csr_matrix(mat)

	print('Edges before pruning: {}'.format(len(nedges)))
	
	# Edge grouping to speed up
	edge_group = edgeGroups(nedges, cnumber, graph, pc)

	# Check edges
	edges = set([])
	for i in xrange(0, len(edge_group)):
		e = edge_group[i]
		whitelist = checkCoreChangeMat(mat, e, cnumber)
		edges.update(whitelist)

		if i % 500 == 0:
			print('Index: {} \t Total: {}'.format(i, len(edges)))
		
	print('Edges after pruning: {}'.format(len(edges)))
	return edges


def generateCandidateEdges(graph, cnumber, cutoff, pc, nodes):
	"""
	Generate list of edges which can be added without change in core number
	"""
	#nodes = set([n for n in cnumber if cnumber[n] >= cutoff])
	#print('Number of nodes: {}'.format(len(nodes)))
	
	edges = []
	while len(nodes) >= 2:
		u = nodes.pop()

		if u not in graph.nodes():
			continue

		cand = nodes.difference(graph.neighbors(u))

		for v in cand:
			edges.append((u, v))

	edges = pruneCandidateEdges(graph, edges, cnumber, pc)

	return edges


def updateCoreSubgraph(kcore, cnumber, u, v):
	kmax = max(cnumber[u], cnumber[v])
	kmin = min(kcore.keys())

	for k in xrange(kmin, kmax + 1):
		kcore[k].add_edge(u,v)

	return kcore


def generateCoreSubgraph(graph, cnumber):
	cn = set(cnumber.values())
	core_subgraph = {}

	for c in cn:
		core_subgraph[c] = nx.k_core(graph, k = c, core_number=cnumber)

	return core_subgraph


def generateCoreNumber(kcore):
	carray = {}

	for c in kcore:
		carray[c] = nx.core_number(kcore[c])

	return carray


def generateCoreSubgraphNodes(kcore):
	"""
	The grouphs of nodes that are connected in the kcore
	"""
	nodes = {}
	for c in kcore:
		if nx.is_connected(kcore[c]):
			nodes[c] = [set(kcore[c].nodes())]
		else:
			nodes[c] = [cn for cn in nx.connected_components(kcore[c])]
	return nodes


def getShellConnectedComponents(graph, cnumber, candidates=None):
	nodes = {}
	if candidates is None:
		cvals = list(set(cnumber.values()))
	else:
		cvals = list(set(cnumber[u] for u in candidates))

	for c in cvals:
		sg = nx.k_shell(graph, c, cnumber)
		cc = nx.connected_components(sg)
		for c in cc:
			for u in c:
				nodes[u] = c

	return nodes

def main(fname, sname, k=None, m=10, mode='alg_edge'):
	"""
	fname 	: The original data file
	sname 	: The save location and fname
	k 		: Top k% nodes to preserve
	"""

	t0 = time.time()
	t = []

	graph = readGraph(fname)

	if graph.number_of_nodes() > 20000:
		print('Graph too large')
		return False

	print(nx.info(graph))

	graph_matrix = nx.to_numpy_matrix(graph)
	graph = nx.from_numpy_matrix(graph_matrix)
	#graph_matrix = sparse.csr_matrix(graph_matrix)

	cnumber = nx.core_number(graph)
	degree = graph.degree()

	kcore = generateCoreSubgraph(graph, cnumber)
	#carray = generateCoreNumber(kcore)
	#knodes = generateCoreSubgraphNodes(kcore)

	cvals = cnumber.values()
	
	if k == 100 or k is None:
		cutoff = min(cvals)
		k = 100
	else:
		cutoff = sorted(cvals, reverse=True)[int(len(cnumber)*k/100)]
		
	step = int(graph.number_of_edges()/400)

	if mode == 'alg_edge' or mode == 'alg_node' or mode == 'alg_both':
		nodes = set([u for u in cnumber if cnumber[u] > cutoff])
	elif mode == 'core':
		nodes = set(sorted(cnumber, key=cnumber.get, reverse=True)[0:int(len(cnumber)*0.1)])
	elif mode == 'degree':
		nodes = set(sorted(degree, key=degree.get, reverse=True)[0:int(len(degree)*0.1)])
	elif mode == 'random':
		nodes = set(random.sample(cnumber.keys(), int(len(degree)*0.1)))
	elif mode == 'oracle':
		nodes = set([u for u in cnumber if cnumber[u] > cutoff])

	mcd = computeMCD(graph, cnumber)
	pc = generatePureCore(graph, cnumber, mcd)
	
	cs = getCoreStrength(graph, cnumber)
	ci, cd = getCoreInfluence(cnumber, kcore)
	shell = getShellConnectedComponents(graph, cnumber)
	
	
	print('\nMax core: {} \t Cut off: {}'.format(max(cvals), cutoff))
	
	nedges = generateCandidateEdges(graph, cnumber, cutoff, pc, nodes)
	print('Number of candidate: {}'.format(len(nedges)))

	if mode == 'alg_edge' or mode == 'alg_node' or mode == 'alg_both':
		nedges = edgePriority(nedges, cnumber, cs, ci, cd, kcore, mode)
	elif mode == 'random' or mode == 'core' or mode == 'random':
		nedges = baselinePriority(nedges, cnumber, degree, mode)
	elif mode == 'oracle':
		nedges = list(nedges)

	i = 0

	# Original graph
	if mode != 'oracle':
		tsname = sname + '_' + mode + '_' + '_k_' + str(k) + '_0.0.csv'
		nx.write_edgelist(graph, tsname, data=False)

	while len(nedges) > 0 and i <= m*step:
		#if i <= m*step and mode != 'oracle':
		#	break
		e = nedges.pop(0)

		#if _checkIfCoreNumberChange(graph, cnumber, e):
		#	continue

		#print(cnumber[e[0]], cnumber[e[1]])

		graph.add_edge(e[0],e[1])
		graph_matrix[e[0],e[1]] = 1
		graph_matrix[e[1],e[0]] = 1
		
		if mode != 'oracle':
			i += 1

		mcd = updateMCD(graph, cnumber, mcd, e)
		pc = updatePureCore(graph, cnumber, mcd, pc, e)
		nedges = updateCandidateEdges(graph, nedges, cnumber, pc, e)
		#nedges = pruneCandidateEdges(graph, nedges, cnumber, pc)

		if mode == 'alg_edge' or mode == 'alg_node' or mode == 'alg_both':
			#kcore = generateCoreSubgraph(graph, cnumber)
			kcore = updateCoreSubgraph(kcore, cnumber, e[0], e[1])
			cs = getCoreStrength(graph, cnumber)
			ci, cd = getCoreInfluence(cnumber, kcore)
			nedges = edgePriority(nedges, cnumber, cs, ci, cd, kcore, mode)
		elif mode == 'oracle':
			nedges = list(nedges)
		else:
			nedges = baselinePriority(nedges, cnumber, graph.degree(), mode=mode)

		if i%step == 0 and mode != 'oracle':
			tsname = sname + '_' + mode + '_'  + '_k_' + str(k) + '_' + str(float(i/(step*4))) + '.csv'
			#print('Number of candidate: {} {}'.format(len(nedges), len(oedges)))
			print('Saving: {}'.format(tsname))
			print(nx.info(graph))
			nx.write_edgelist(graph, tsname, data=False)

			t1 = time.time()
			t.append(t1-t0)
			print('Time: {}'.format(t[-1]))

		if i%1000 and mode == 'oracle':
			print('Edges left: {]'.format(len(nedges)))
			print(nx.info(graph))

	if mode == 'oracle':
		tsname = sname + '_oracle.csv'
		#print('Number of candidate: {} {}'.format(len(nedges), len(oedges)))
		print('Saving: {}'.format(tsname))
		print(nx.info(graph))
		nx.write_edgelist(graph, tsname, data=False)

	print(t, file=open(sname+'_time','w'))


if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]
	k = int(sys.argv[3])
	mode = sys.argv[4]

	main(fname, sname, k, 20, mode)

