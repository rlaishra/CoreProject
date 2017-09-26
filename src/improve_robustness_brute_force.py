"""
Add edges between the high core number nodes to improve the robustness
"""

from __future__ import division, print_function
import networkx as nx
import numpy as np
import sys
import random
import time

def readGraph(fname):
	graph = nx.read_edgelist(fname)
	graph.remove_edges_from(graph.selfloop_edges())
	return graph

def addEdges(graph, ne, edges, id=None):
	cn =nx.core_number(graph)
	core = np.array(cn.values())

	i = 0

	while len(edges) > 0:
		e = edges.pop(0)

		graph.add_edge(e[0],e[1])
		tcore = nx.core_number(graph)
		tcore = np.array(tcore.values())

		diff = np.linalg.norm(core - tcore)

		if diff != 0:
			graph.remove_edge(e[0], e[1])
		else:
			i += 1

		if i >= ne:
			break

		if len(edges)%1000 == 0:
			print('Edges : {}'.format(len(edges)))
	return graph, edges


def possibleEdges(graph, k):
	core = nx.core_number(graph)
	th = sorted(core.values())[int(len(core) * k / 100)]
	nodes = graph.nodes()
	nodes = set([u for u in nodes if core[u] >= th])

	edges = []
	while len(nodes) > 2:
		u = nodes.pop()
		n = nodes.difference(graph.neighbors(u))
		for v in n:
			edges.append([u, v])
	random.shuffle(edges)

	return edges

if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]

	t0 = time.time()
	t = []

	nedges = xrange(1,11)

	graph = readGraph(fname)
	edges = possibleEdges(graph, 25)
	count = graph.number_of_edges()/100

	tsname = sname + '0.csv'
	nx.write_edgelist(graph, tsname)

	print('Number of possible edges: {}'.format(len(edges)))

	ne = int(count)

	for e in nedges:
		tsname = sname + str(e) + '.csv'
		#graph = readGraph(fname)
		print(nx.info(graph))
		graph, edges = addEdges(graph, ne, edges, e)
		print(nx.info(graph))
		nx.write_edgelist(graph, tsname)
		
		t1 = time.time()
		t.append(t1-t0)
		print('Time: {}'.format(t[-1]))
	print('time',t)
