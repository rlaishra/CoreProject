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
	nodes = [v for v in cnumber if cnumber[v] == cnumber[u]]

	# MCD condition
	nodes = [v for v in cnumber if mcd[v] > cnumber[u]]
	
	# Reachability condition
	nodes.append(u) 				# u inserted to check for reachabilty
	sg = graph.subgraph(nodes)
	cc = nx.connected_components(sg)
	for c in cc:
		if u in c:
			if mcd[u] <= cnumber[u]:
				c.remove(u)
			return c
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
		data[u] = cd/cnumber[u]

	return data

def edgePriority(nedges, rcd):
	priority = {}

	for e in nedges:
		priority[e] = rcd[e[0]] * rcd[e[1]]

	edges = sorted(priority, key=priority.get, reverse=False)
	#print(np.mean([priority[e] for e in edges[:10]]), np.mean([priority[e] for e in edges[-
	#	10:]]))
	return edges

def updatePureCore(graph, cnumber, mcd, pc, e):
	"""
	Update the pure core of all affected nodes on adding edge e

	Returns new pc, and list of nodes whose pc have been changed
	"""
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

	Returns true if chang, false otherwise
	"""
	graph.add_edge(u, v)
	tcore = nx.core_number(graph)
	tcore = np.array(tcore.values())
	graph.remove_edge(u, v)

	if np.array_equiv(tcore, carray):
		return True
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

	if carray is None:
		carray = np.array(cnumber.values())

	if kcore is None:
		kcore = nx.k_core(graph, cutoff)
	
		
	print('Changed count: {}'.format(len(changed)))

	# Remove edges that will change core number from nedges
	remove = []
	for e in nedges:
		u = e[0]
		v = e[1]
		if (u in changed or v in changed) and\
		  _checkIfCoreNumberChange(kcore, carray, u, v):
			remove.append((u,v))
			if len(remove)%100 == 0:
				print('Remove: {} of {}'.format(len(remove), len(nedges)))
	
	remove = set(remove)
	nedges = [e for e in nedges if e not in remove]

	print('0 \t Edges size \tO: {} N: {}'.format(len(oedges), len(nedges)))

	# If size of remove is less than size, add more
	while len(nedges) < size and len(oedges) > 0:
		e = oedges.pop(0)

		u = e[0]
		v = e[1]

		"""
		if (u in changed or v in changed) and cnumber[u] != cnumber[v]\
		 and _checkIfCoreNumberChange(graph, carray, u, v):
			n.append((u,v))
			print(len(pruned_list), len(edges))

		"""
		if ((cnumber[u] <= cnumber[v] and u in changed)\
		 or (cnumber[v] <= cnumber[u] and v in changed))\
		 and _checkIfCoreNumberChange(kcore, carray, u, v):
			if len(oedges)%500 == 0:
				print('1 \t Edges size \tO: {} N: {}'.format(len(oedges), len(nedges)))
			continue

		nedges.append((u,v))
		if len(nedges)%1000 == 0:
			print('2 \t Edges size \tO: {} N: {}'.format(len(oedges), len(nedges)))
		

	return oedges, nedges


def generateCandidateEdges(graph, cnumber, pc, cutoff, size, kcore, carray, rcd):
	"""
	Generate list of edges which can be added without change in core number
	"""
	nodes = set([n for n in cnumber if cnumber[n] > cutoff])
	
	vedges = {}
	oedges = []
	while len(nodes) >= 2:
		u = nodes.pop()
		n = nodes.difference(graph.neighbors(u))
		for v in n:
			#if cnumber[v] != cnumber[u]: 				# (Temp) This will filter out edges that will not change core number
			vedges[(u,v)] = cnumber[u]*cnumber[v]
			oedges.append((u, v))

	#oedges = sorted(vedges, key=vedges.get, reverse=True)
	oedges = edgePriority(oedges, rcd)
	print('Unpruned candidates: {}'.format(len(oedges)))
	
	#oedges = edgePriority(oedges, rcd)
	nedges = []
	oedges, nedges = pruneCandidateEdges(graph, oedges, nedges, cnumber, pc, changed=None, size=size, carray=carray, kcore=kcore)
	print('Pruned candidates: {}'.format(len(nedges)))

	return oedges, nedges, vedges


def main(fname, sname, k, m=10):

	t0 = time.time()
	t = []

	graph = readGraph(fname)
	cnumber = nx.core_number(graph)

	cvals = cnumber.values()
	cutoff = sorted(cvals, reverse=True)[int(len(cnumber)*k/100)]
	step = int(graph.number_of_edges()/100)

	nodes = [u for u in cnumber if cnumber[u] > cutoff]

	mcd = computeMCD(graph, cnumber, nodes)
	pc = generatePureCore(graph, cnumber, mcd, nodes)
	rcd = getRCD(graph, cnumber, nodes)
	
	#pc_size = [len(pc[u]) for u in pc]
	
	print(nx.info(graph))
	print('Max core: {} \t Cut off: {}'.format(max(cvals), cutoff))
	#print('Pure Core Size \t Max: {} \t Mean: {}'.format(max(pc_size), np.mean(pc_size)))

	# Global values for comparison
	# The kcore subgraph greater then thershold for camparisons
	kcore = nx.k_core(graph, cutoff)
	carray = np.array(nx.core_number(kcore).values())

	oedges, nedges, vedges = generateCandidateEdges(graph, cnumber, pc, cutoff, step, kcore, carray, rcd)
	print('Number of candidate: {} {}'.format(len(nedges),len(oedges)))

	#nedges = edgePriority(nedges, rcd)

	i = 0

	# Original graph
	tsname = sname + '0.csv'
	nx.write_edgelist(graph, tsname)

	while len(nedges) > 0 and i < m*step:
		e = nedges.pop(0)
		graph.add_edge(e[0],e[1])
		i += 1

		mcd = updateMCD(graph, cnumber, mcd, e)
		pc, changed = updatePureCore(graph, cnumber, mcd, pc, e)
		oedges, nedges = pruneCandidateEdges(graph, oedges, nedges, cnumber, pc, changed, step, carray=carray, kcore=kcore)

		if i%100 == 0:
			nedges = edgePriority(nedges, rcd) 

		if i%step == 0:
			tsname = sname + str(int(i/step)) + '.csv'
			print('Number of candidate: {} {}'.format(len(nedges), len(oedges)))
			print('Saving: {}'.format(tsname))
			print(nx.info(graph))
			nx.write_edgelist(graph, tsname)

			t1 = time.time()
			t.append(t1-t0)
			print('Time: {}'.format(t[-1]))
	print('time', open(sname+'_time','w'))


if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]
	k = int(sys.argv[3])

	main(fname, sname, k)

