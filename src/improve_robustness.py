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


def getRCD(graph, cnumber, nodes=None):
	data = {}

	if nodes is None:
		nodes = graph.nodes()

	for u in nodes:
		if cnumber[u] == 0:
			data[u] = np.inf
			continue
		neighbors = graph.neighbors(u)
		cd = len([v for v in neighbors if cnumber[u] == cnumber[v]])
		data[u] = cd/cnumber[u] + 1
		#data[u] = cd + 1

	# Normalize betweenn 0-1
	#rmin = min(data.values())
	#rmax = max(data.values())

	#for u in data:
	#	data[u] = (data[u] - rmin) / (rmax - rmin)

	return data


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



def getCoreInfluence(cnumber, kcore, nodes=None, changed=None):
	"""
	Compute the influence score for each nodes
	"""
	if nodes is None:
		nodes = cnumber.keys()

	if changed is None:
		changed = nodes

	knumber = [cnumber[u] for u in nodes if u in changed]
	kmin = min(knumber)
	kmax = min(knumber)

	iScore = {u:1 for u in nodes}

	empty = []
	for k in xrange(kmin, kmax + 1):
		# Nodes in the kcore
		knodes = kcore[k].nodes()

		for u in set(knodes).intersection(nodes):
			supNodes = _getSupportNodes(kcore[k], cnumber, u)
			if len(supNodes) < 1:
				empty.append(u)
				continue

			share = iScore[u]/len(supNodes)
			for v in supNodes:
				iScore[v] += share

	# Normalize between 0-1
	#imin = min(iScore.values())
	#imax = max(iScore.values())

	#if imin == imax:
	#	return iScore

	#for u in iScore:
	#	iScore[u] = (iScore[u]-imin)/(imax - imin)
	
	#print('Core Influence: {}'.format(len(empty)))
	return iScore



def edgePriority(nedges, rcd, cnumber, iscore, shell):
	priority = {}
	#epsilon = 0.001
	for e in nedges:
		e = list(e)
		u = e[0]
		v = e[1]
		if u in rcd and v in rcd:
			p1 =  iscore[u] * iscore[v]
			p2 =  rcd[u] * rcd[v]

			#p1 = min(iscore[u], iscore[v])
			#p2 = max(rcd[u], rcd[v])
			
			p3 = max(len(shell[u]), len(shell[v])) / len(shell[u].union(shell[v]))
			#p3 = 1
			priority[(u,v)] = p1 * p3 / p2

	edges = sorted(priority, key=priority.get, reverse=True)
	edges = [set(e) for e in edges]

	#print('iScore', max(iscore.values()), min(iscore.values()))
	#print('RCD', max(rcd.values()), min(rcd.values()))

	#e = edges[0]
	#print('Max', e, priority[e], iscore[e[0]], iscore[e[1]], rcd[e[0]], rcd[e[1]], cnumber[e[0]], cnumber[e[1]])
	#e = edges[-1]
	#print('Min', e, priority[e], iscore[e[0]], iscore[e[1]], rcd[e[0]], rcd[e[1]], cnumber[e[0]], cnumber[e[1]])
	return edges


def updatePureCore(graph, cnumber, mcd, pc, e, candidates):
	"""
	Update the pure core of all affected nodes on adding edge e

	Returns new pc, and list of nodes whose pc have been changed
	"""
	e = list(e)
	u = e[0]
	v = e[1]

	if cnumber[u] != cnumber[v]:
		return pc, []

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

	return pc, set(changed)


def _checkIfCoreNumberChange(graph, carray, u, v):
	"""
	Add edge and check if core number change

	Returns true if change, false otherwise
	"""
	if graph.has_edge(u,v):
		print('Exist', u,v)
		return True

	graph.add_edge(u, v)
	tcore = nx.core_number(graph)
	#tcore = np.array(tcore.values())
	#graph.remove_edge(u, v)

	for x in carray:
		if carray[x] != tcore[x]:
			#print('Core Chaged\t{} \t Prev: \t{}\tNew: \t{}'.format(x, carray[x], tcore[x]))
			return True

	#print([(carray[u], tcore[u]) for u in carray])
	return False


def pruneCandidateEdges(graph, oedges, nedges, cnumber, pc, changed=None, size=None, carray=None, kcore=None, cutoff=0):
	"""
	Remove the edges which will change core number
	"""
	if changed is None:
		changed = set(pc.keys())

	if size is None:
		size = len(oedges)

	if len(changed) == 0 and len(nedges) > 0.5 * size:
		return oedges, nedges
	#print('edges', len(oedges), len(nedges))

	if kcore is None:
		kcore = generateCoreSubgraph(graph, cnumber)

	if carray is None:
		carray = generateCoreNumber(kcore)
	
	print('Changed count: {}'.format(len(changed)))

	# Remove edges that will change core number from nedges
	remove = []
	for e in nedges:
		e = list(e)
		u = e[0]
		v = e[1]
		sg = kcore[min(cnumber[u], cnumber[v])]
		cv = carray[min(cnumber[u], cnumber[v])]

		if _checkIfCoreNumberChange(sg, cv, u, v):
			remove.append(set([u,v]))
			if len(remove)%100 == 0:
				print('Remove: {} of {}'.format(len(remove), len(nedges)))
	
	print('Edges before pruning: {}'.format(len(nedges)))
	#remove = set(remove)
	nedges = [e for e in nedges if e not in remove]
	print('Edges after pruning: {}'.format(len(nedges)))

	print('Edges size \tO: {} N: {}'.format(len(oedges), len(nedges)))

	# If size of remove is less than size, add more
	while len(nedges) < size and len(oedges) > 0:
		e = list(oedges.pop(0))

		u = e[0]
		v = e[1]

		sg = kcore[min(cnumber[u], cnumber[v])]
		cv = carray[min(cnumber[u], cnumber[v])]

		if not _checkIfCoreNumberChange(sg, cv, u, v):
			nedges.append(set([u,v]))
	
		if len(nedges)%1000 == 0 or len(oedges)%1000 == 0:
			print('Edges size \tO: {} N: {}'.format(len(oedges), len(nedges)))
		
	return oedges, nedges


def generateCandidateEdges(graph, cnumber, pc, cutoff, size, kcore, carray, rcd, knodes, iscore, shell):
	"""
	Generate list of edges which can be added without change in core number
	"""
	nodes = set([n for n in cnumber if cnumber[n] >= cutoff])
	print('Number of nodes: {}'.format(len(nodes)))
	
	vedges = {}
	oedges = []
	while len(nodes) >= 2:
		u = nodes.pop()

		if u not in graph.nodes():
			continue

		cand = [sn for sn in knodes[cnumber[u]] if u in sn][0]
		cand = set(cand).difference(graph.neighbors(u))
		cand = cand.intersection(nodes)
		#cand = [v for v in cand if cnumber[v] == cnumber[u]]

		for v in cand:
			#if cnumber[v] == cnumber[u]: 				# (Temp) This will filter out edges that will not change core number
			#vedges[(u,v)] = cnumber[u]*cnumber[v]
			oedges.append(set([u, v]))

	#oedges = sorted(vedges, key=vedges.get, reverse=True)
	oedges = edgePriority(oedges, rcd, cnumber, iscore, shell)
	print('Unpruned candidates: {}'.format(len(oedges)))
	
	#oedges = edgePriority(oedges, rcd)
	nedges = []
	oedges, nedges = pruneCandidateEdges(graph, oedges, nedges, cnumber, pc, changed=None, size=size, carray=carray, kcore=kcore)
	print('Pruned candidates: {}'.format(len(nedges)))

	return oedges, nedges, vedges


def generateCoreSubgraph(graph, cnumber):
	cn = set(cnumber.values())
	core_subgraph = {}

	for c in cn:
		core_subgraph[c] = nx.k_core(graph, k = c, core_number=cnumber)

	return core_subgraph


def generateCoreNumber(kcore):
	carray = {}

	for c in kcore:
		#cn = 
		#carray[c] = np.array([cn[u] for u in sorted(cn.keys())])
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


def main(fname, sname, k=None, m=10):
	"""
	fname 	: The original data file
	sname 	: The save location and fname
	k 		: Top k% nodes to preserve
	"""

	t0 = time.time()
	t = []

	graph = readGraph(fname)

	if graph.number_of_nodes() > 25000:
		print('Graph too large')
		return False

	print(nx.info(graph))

	cnumber = nx.core_number(graph)

	kcore = generateCoreSubgraph(graph, cnumber)
	carray = generateCoreNumber(kcore)
	knodes = generateCoreSubgraphNodes(kcore)

	cvals = cnumber.values()
	
	if k is not None:
		cutoff = sorted(cvals, reverse=True)[int(len(cnumber)*k/100)]
	else:
		cutoff = min(cvals)
		k = 100

	step = int(graph.number_of_edges()/100)

	nodes = [u for u in cnumber if cnumber[u] >= cutoff]

	mcd = computeMCD(graph, cnumber, nodes)
	pc = generatePureCore(graph, cnumber, mcd, nodes)
	rcd = getRCD(graph, cnumber)
	iscore = getCoreInfluence(cnumber, kcore)
	shell = getShellConnectedComponents(graph, cnumber)
	
	#pc_size = [len(pc[u]) for u in pc]
	
	print(nx.info(graph))
	print('\nMax core: {} \t Cut off: {}'.format(max(cvals), cutoff))
	#print('Pure Core Size \t Max: {} \t Mean: {}'.format(max(pc_size), np.mean(pc_size)))

	oedges, nedges, vedges = generateCandidateEdges(graph, cnumber, pc, cutoff, step, kcore, carray, rcd, knodes, iscore, shell)
	print('Number of candidate: {} {}'.format(len(nedges),len(oedges)))

	#nedges = edgePriority(nedges, rcd)

	i = 0

	# Original graph
	tsname = sname + '_k_' + str(k) + '_0.csv'
	nx.write_edgelist(graph, tsname)

	updatedNodes = []

	while len(nedges) > 0 and i <= m*step:
		e = list(nedges.pop(0))
		graph.add_edge(e[0],e[1])
		i += 1

		mcd = updateMCD(graph, cnumber, mcd, e)
		pc, changed = updatePureCore(graph, cnumber, mcd, pc, e, nodes)
		oedges, nedges = pruneCandidateEdges(graph, oedges, nedges, cnumber, pc, changed, step, carray=carray, kcore=kcore)

		updatedNodes += changed

		if i%10 == 0:
			#print('Recomputing edge priority')
			rcd = getRCD(graph, cnumber, nodes)
			iscore = getCoreInfluence(cnumber, kcore)
			shell = getShellConnectedComponents(graph, cnumber)
			nedges = edgePriority(nedges, rcd, cnumber, iscore, shell) 

		if i%step == 0:
			tsname = sname + '_k_' + str(k) + '_' + str(int(i/step)) + '.csv'
			print('Number of candidate: {} {}'.format(len(nedges), len(oedges)))
			print('Saving: {}'.format(tsname))
			print(nx.info(graph))
			nx.write_edgelist(graph, tsname)

			t1 = time.time()
			t.append(t1-t0)
			print('Time: {}'.format(t[-1]))
	print(t, file=open(sname+'_time','w'))


if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]
	#k = int(sys.argv[3])

	main(fname, sname)

