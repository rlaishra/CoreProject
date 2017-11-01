from __future__ import division, print_function
import networkx as nx 
import numpy as np 
import sys
from scipy.stats import rankdata
import random
import csv
import scipy.stats as stats
from scipy.stats import iqr
import community


class Anomaly(object):
	"""Anomaly detection with Core-A"""
	def __init__(self, fname, sname, name, tname):
		super(Anomaly, self).__init__()
		self.fname = fname
		self.sname = sname
		self.name = name
		self.tname = tname


	def readGraph(self):
		fname = self.fname
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
		isolates = nx.isolates(graph)
		graph.remove_nodes_from(isolates)
		#print(nx.info(graph))
		return graph

	def fractionalRank(self, data):
		keys = data.keys()
		values = data.values()

		values = [-1*v for v in values] # since we want ranking in reverse
		values = rankdata(values, method='average')
		
		for i in xrange(0, len(keys)):
			data[keys[i]] = values[i]

		return data

	def compareRanking(self, x1, x2):
		common = set(x1.keys()).intersection(x2.keys())
		y1 = []
		y2 = []
		for u in common:
			y1.append(x1[u])
			y2.append(x2[u])

		cor, _ = stats.kendalltau(y1, y2, nan_policy='omit')

		return cor

	def computeAgreement(self, x1, x2):
		#y1 = {u:x1[u] for u in x2}
		#y2 = {u:x2[u] for u in x2}

		v1 = x1.values()
		v2 = x2.values()

		h1 = 1.5*iqr(v1) + np.percentile(v1,75)
		h2 = 1.5*iqr(v2) + np.percentile(v2,75)

		print(h1,h2)

		# Anomaliess
		y1 = set([u for u in x1 if x1[u] > h1 and u in x2])
		y2 = set([u for u in x2 if x2[u] > h2])

		print(np.percentile(v1,75), np.percentile(v1,25), iqr(v1))
		print('Anomalies: {} {} of {}'.format(len(y1), len(y2), len(x2)))

		if len(y1) > 0 and len(y2) > 0:
			return len(y1.intersection(y2))/len(y1.union(y2))
		return None



		v1 = sorted(y1.values(), reverse=True)
		v1 = v1[int(len(v1)*0.01)]
		y1 = set([u for u in y1 if y1[u] >=v1])

		v2 = sorted(y2.values(), reverse=True)
		v2 = v2[int(len(v2)*0.01)]
		y2 = set([u for u in y2 if y2[u] >=v2])

		#print(len(y1), len(y2), len(y1.intersection(y2)), len(y1.union(y2)))
		if len(y1) > 10 and len(y2) > 10:
			return len(y1.intersection(y2))/len(y1.union(y2))
		return None

	def sample(self, graph, steps=0.5):
		sample = nx.Graph()
		current = random.choice(graph.nodes())
		size = int(graph.number_of_nodes() * steps)
		#queue = [current]

		for _ in xrange(0, size):
			#current = queue.pop(0)
			neighbors = graph.neighbors(current)
			edges = [(current, u) for u in neighbors]
			sample.add_edges_from(edges)
			#cand = [u for u in neighbors if u not in queue]
			#queue += cand

			if len(neighbors) > 0:
				current = random.choice(neighbors)
			else:
				current = random.choice(sample.nodes())

		return sample

	def computeResilience(self, pu = 100):
		step = 5
		p = range(0, 51,step)

		adata = []

		for _ in xrange(0, 10):
			graph = self.readGraph()
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
		 		cor = self.compareRanking(ocn, ncn)
		 		tdata.append(cor)

		 	adata.append(np.mean(tdata))

		return np.mean(adata)

	def computeDMP(self, degree, core):
		dmp = {}
		for u in degree:
			dmp[u] = np.abs(np.log(degree[u]) - np.log(core[u]))
			#print(degree[u], core[u], dmp[u])
			#if dmp[u] > 0:
			#	print(u, dmp[u])
		return dmp

	def run(self):
		graph = self.readGraph()
		cnumber = self.fractionalRank(nx.core_number(graph))
		degree = self.fractionalRank(graph.degree())
		odmp = self.computeDMP(degree, cnumber)

		sizes = [0.25, 0.50, 0.75]
		data = []

		resilience = self.computeResilience(50)

		for s in sizes:
			agreement = []

			for _ in xrange(0,10):
				sample = self.sample(graph, s)
				cnumber = self.fractionalRank(nx.core_number(sample))
				degree = self.fractionalRank(sample.degree())
				ndmp = self.computeDMP(degree, cnumber)

				#agreement.append(self.compareRanking(odmp, ndmp))
				a = self.computeAgreement(odmp, ndmp)
				if a is not None:
					agreement.append(a)
		
			data.append([s, resilience, np.mean(agreement), np.std(agreement)])

		# Save
		with open(self.sname, 'a') as f:
			writer = csv.writer(f, delimiter=',')
			for d in data:
				writer.writerow([self.tname, self.name] + d)
				print(d)

class KCommunity(object):
	"""docstring for Community"""
	def __init__(self, fname, sname, name, tname):
		super(KCommunity, self).__init__()
		self.fname = fname
		self.sname = sname
		self.name = name
		self.tname = tname


	def readGraph(self):
		fname = self.fname
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
		isolates = nx.isolates(graph)
		graph.remove_nodes_from(isolates)
		#print(nx.info(graph))
		return graph

	def bestPartition(self, graph):
		part = community.best_partition(graph)
		return part

	def assignPartition(self, graph, part):
		unassigned = [u for u in graph.nodes() if u not in part]

		while len(unassigned) > 0:
			print('Unassigned: {}'.format(len(unassigned)))
			remove = []
			for u in unassigned:
				can = []
				for v in graph.neighbors(u):
					if v in part:
						can.append(part[v])
				if len(can) > 0:
					part[u] = max(set(can), key=can.count)
					remove.append(u)
			unassigned = [u for u in unassigned if u not in remove]
			if len(remove) == 0:
				return part
		return part

	def subGraph(self, graph):
		cnumber = nx.core_number(graph)
		threshold = np.percentile(cnumber.values(),50)
		sgraph = nx.k_core(graph, threshold)
		return sgraph


	def sample(self, graph, steps=0.5):
		sample = nx.Graph()
		current = random.choice(graph.nodes())
		size = int(graph.number_of_nodes() * steps)

		for _ in xrange(0, size):
			neighbors = graph.neighbors(current)
			edges = [(current, u) for u in neighbors]
			sample.add_edges_from(edges)
			#cand = [u for u in neighbors if u not in queue]
			#queue += cand
			
			if len(neighbors) > 0:
				current = random.choice(neighbors)
			else:
				current = random.choice(sample.nodes())

		return sample

	def getPartition(self, graph):
		sg = self.subGraph(graph)
		part = self.bestPartition(sg)
		part = self.assignPartition(graph, part)
		return part

	def computeSimilarity(self, part1, part2):
		com1 = {i:set([]) for i in set(part1.values())}
		com2 = {i:set([]) for i in set(part2.values())}

		for u in part1:
			if u in part2:
				com1[part1[u]].update([u])

		for u in part2:
			com2[part2[u]].update([u])

		#print(len(com1), len(com2))

		sim = []
		for i in com2:
			msim = 0
			match = None
			c = com2[i]
			for j in com1:
				d = com1[j]
				s = len(c.intersection(d))/len(c.union(d))
				if s > msim:
					#print(c)
					#print(d)
					msim = s
					match = match
			if match is not None:
				del com1[match]

			sim.append(msim)
		#print(sim)

		return np.mean(sim)


	def compareRanking(self, x1, x2):
		common = set(x1.keys()).intersection(x2.keys())
		y1 = []
		y2 = []
		for u in common:
			y1.append(x1[u])
			y2.append(x2[u])

		cor, _ = stats.kendalltau(y1, y2, nan_policy='omit')

		return cor

	def computeResilience(self, pu = 100):
		step = 5
		p = range(0, 51,step)

		adata = []

		for _ in xrange(0, 10):
			graph = self.readGraph()
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
		 		cor = self.compareRanking(ocn, ncn)
		 		tdata.append(cor)

		 	adata.append(np.mean(tdata))

		return np.mean(adata)

	def run(self):
		graph = self.readGraph()
		opart = self.getPartition(graph)

		sizes = [0.25, 0.50, 0.75]
		data = []
		resilience = self.computeResilience(50)

		for s in sizes:
			similarity = []

			for _ in xrange(0,10):
				sample = self.sample(graph, s)
				npart = self.getPartition(sample)

				similarity.append(self.computeSimilarity(opart, npart))
		
			data.append([s, resilience, np.mean(similarity), np.std(similarity)])

		# Save
		with open(self.sname, 'a') as f:
			writer = csv.writer(f, delimiter=',')
			for d in data:
				writer.writerow([self.tname, self.name] + d)
				print(d)




		

if __name__ == '__main__':
	mode = int(sys.argv[1])
	fname = sys.argv[2]
	sname = sys.argv[3]
	name = sys.argv[4]
	tname = sys.argv[5]

	if mode == 0:
		anomaly = Anomaly(fname, sname, name, tname)
		anomaly.run()
	elif mode == 1:
		com = KCommunity(fname, sname, name, tname)
		com.run()



		