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

def readGraph(fname):
	graph = nx.read_edgelist(fname)
	graph.remove_edges_from(graph.selfloop_edges())
	return graph

def computeMCD(graph, cnumber):
	mcd = {}
	for u in graph.nodes():
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
	nodes = [v for v in nodes if mcd[v] > cnumber[u]]
	
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


def generatePureCore(graph, cnumber, mcd):
	pc = {}

	for u in graph.nodes():
		pc[u] = findPureCore(graph, cnumber, mcd, u)
	
	return pc

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


def pruneCandidateEdges(graph, edges, cnumber, pc, changed=None):
	"""
	Remove the edges which will change core number
	"""
	if changed is None:
		changed = pc.keys()

	if len(changed) == 0:
		return edges

	carray = np.array(cnumber.values())
	pruned_list = []
	
	for e in edges:
		u = e[0]
		v = e[1]
		if (cnumber[u] <= cnumber[v] and u in changed\
		 and _checkIfCoreNumberChange(graph, carray, u, v))\
		 or (cnumber[v] <= cnumber[u] and v in changed\
		 and _checkIfCoreNumberChange(graph, carray, u, v)):
			continue
		pruned_list.append((u,v))

	return pruned_list


def generateCandidateEdges(graph, cnumber, pc, cutoff):
	"""
	Generate list of edges which can be added without change in core number
	"""
	core = cnumber
	nodes = set(n for n in core if core[n] > cutoff)
	
	vedges = {}
	while len(nodes) > 2:
		u = nodes.pop()
		n = nodes.difference(graph.neighbors(u))
		for v in n:
			vedges[(u,v)] = core[u]*core[v]

	edges = sorted(vedges, key=vedges.get, reverse=True)
	print('Unpruned candidates: {}'.format(len(edges)))
	
	edges = pruneCandidateEdges(graph, edges, cnumber, pc, changed=nodes)
	print('Pruned candidates: {}'.format(len(edges)))

	return edges, vedges


def main(fname, sname, k, m=10):
	t0 = time.time()
	t = []

	graph = readGraph(fname)
	cnumber = nx.core_number(graph)
	mcd = computeMCD(graph, cnumber)
	pc = generatePureCore(graph, cnumber, mcd)
	
	#pc_size = [len(pc[u]) for u in pc]

	cutoff = sorted(cnumber.values(), reverse=True)[int(len(cnumber)*k/100)]
	
	print(nx.info(graph))
	#print('Max core: {} \t Cut off: {}'.format(max(cnumber.values()), cutoff))
	#print('Pure Core Size \t Max: {} \t Mean: {}'.format(max(pc_size), np.mean(pc_size)))

	edges, vedges = generateCandidateEdges(graph, cnumber, pc, cutoff)
	print('Number of candidate: {}'.format(len(edges)))

	count = int(graph.number_of_edges()/100)
	i = 0

	# Original graph
	tsname = sname + '0.csv'
	nx.write_edgelist(graph, tsname)

	while len(edges) > 0 and i < m*count:
		e = edges.pop(0)
		graph.add_edge(e[0],e[1])
		i += 1

		mcd = updateMCD(graph, cnumber, mcd, e)
		pc, changed = updatePureCore(graph, cnumber, mcd, pc, e)
		edges = pruneCandidateEdges(graph, edges, cnumber, pc, changed)

		if i%count == 0:
			tsname = sname + str(int(i/count)) + '.csv'
			print('Number of candidate: {}'.format(len(edges)))
			print('Saving: {}'.format(tsname))
			print(nx.info(graph))
			nx.write_edgelist(graph, tsname)

			t1 = time.time()
			t.append(t1-t0)
			print('Time: {}'.format(t[-1]))
	  print('time',t)


if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]
	k = int(sys.argv[3])

	main(fname, sname, k)

