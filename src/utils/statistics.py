from __future__ import division, print_function
import numpy as np
import networkx as nx
import sys
import csv
from pprint import pprint
import scipy.stats

class Statistics(object):
	"""docstring for Statistics."""
	def __init__(self):
		super(Statistics, self).__init__()

	def degreeDistribution(self, graph):
		degree = nx.degree(graph)
		dist = {}
		for n in degree:
			if degree[n] not in dist:
				dist[degree[n]] = 0
			dist[degree[n]] += 1
		total = graph.number_of_nodes()
		dist = {n: dist[n]/total for n in dist}
		return dist

	def kendalltau(self, l1, l2):
		# Variation of kendall tau that do not discard ties
		if not(len(l1) == len(l2)):
			return False
		n = len(l1)
		s = 0

		v = zip(l1, l2)
		v.sort()
		
		l1, l2 = zip(*v)

		for i in xrange(0, n):
			u1 = l1[i]
			u2 = l2[i]
			for j in xrange(i+1, n):
				v1 = l1[j]
				v2 = l2[j]
				# Concordant
				if (u1 == v1 and u2 == v2) or (u1 < v1 and u2 < v2) or (u1 > v1 and u2 > v2):
					s += 1
				else:
					s -= 1
		cor = s/(n*(n-1)*0.5)
		return cor

	def _isDecreasing(self, x):
		for i in xrange(1, len(x)):
			if x[i-1] < x[i]:
				return False
		return True

	def longest_decreasing_subsequence(self, d):
		'Return one of the L.I.S. of list d'
		l = []
		for i in range(len(d)):
			l.append(max([l[j] for j in range(i) if l[j][-1] > d[i]] or [[]], key=len) 
					  + [d[i]])
		return max(l, key=len)

	def distanceFromDecreasing(self, x, n=None):
		"""
		Returns the total value to be subtracted to make the sequence decreasing
		"""
		#print(x)
		
		x = [i if not np.isnan(i) else 1 for i in x]
		#y = [round(i,2) for i in x]
		#print(y)
		if n is None:
			n = len(x)

		#x = [0.5 * (i + 1) for i in x]
		#print(x)

		error = []
		ss = self.longest_decreasing_subsequence(x)
		y = [round(i,2) for i in ss]
		#print(y)
		#print(len(ss))
		if len(ss) < 2:
			return 0
		sel = [None for _ in xrange(0, len(x))]

		j = 0
		for i in xrange(0, len(x)):
			if x[i] == ss[j]:
				sel[i] = ss[j]
				j += 1
				if j >= len(ss):
					break

		u = ss[0]
		v = ss[1]
		for i in xrange(0, len(x)):
			if sel[i] is None:
				if x[i] != 0 :
					#print(np.abs(x[i]-u))
					#print(np.abs(x[i]-v))
					e = max(np.abs(x[i]-u), np.abs(x[i]-v))
					#print(e)
					#e = np.abs(e/x[i])
					error.append(e*e)
					#error.append(e)
			else:
				u = sel[i]
				if i < len(ss)-1:
					v = ss[i+1]
				else:
					v = u

		#print(np.mean(error), np.std(error))
		#print(error)
		if len(error) == 0:
			return 0
		#return np.sum(error)/n
		#print(max(error))
		return np.sqrt(np.sum(error)/n)
		#return np.sqrt(np.sum(error)/len(error))


	def monotonic(self, y):
		x = range(0, len(y))

		r, p = scipy.stats.spearmanr(x, y)

		return r

		#slope = -1 if np.polyfit(range(0, len(x)), x, 1)[0] < 0 else 1
		#print(slope)
		change = []

		#slope = -1
		# Normalize
		if min(x) == max(x):
			return -1
		#x_min = min(x)
		#x_max = max(x) - x_min
		#x = [(v - x_min)/x_max for v in x]

		for i in xrange(1, len(x)):
			u = x[i-1]
			v = x[i]

			"""
			if slope*(v-u) < 0 and u != 0:
				c = np.abs((u-v)/u)
				#c = (u-v)/u
				change += c*c
			"""

			#c = (v - u) + 1
			c = (v - u)

			if v > u:
				#change.append(c/u)
				#print(c,u,c/u)
				change.append(c * c)
				#change += (v-u)
			else:
				change.append(0)
			#else:
			#    change += c
		#return change
		#print(change)
		if len(change) == 0:
		   return 0
		#print(np.std(change), len(change))
		#print(sum([n*n for n in change])/(len(change)-1))
		#return sum(change)/len(x)
		return np.mean(change)

	def increasing(self, x):
		change = 0
		count = 0
		# Normalize
		#x_min = min(x)
		#x_max = max(x) - x_min
		#x = [(v - x_min)/x_max for v in x]

		for i in xrange(1, len(x)):
			u = x[i-1]
			v = x[i]
			if u < v:
				change += (v - u)
				count += 1
		return change

	def linearRegression(self, y):
		x = range(0, len(y))
		slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
		return slope, r_value

if __name__ == '__main__':
	stats = Statistics()

	"""
	l1 = [i for i in xrange(0,100)] + [20000]*100
	l2 = [i for i in xrange(0,10)] + [3,5,9,0,10]
	l3 = range(1000,100,-1)
	l4 = range(10, 100)
	l5 = range(0,10) + [50] + range(11,20)

	change = stats.monotonic(l3)
	print(change)

	change = stats.monotonic(l4)
	print(change)

	change = stats.monotonic(l2)
	print(change)

	change = stats.monotonic(l1)
	print(change)

	change = stats.monotonic(l5)
	print(change)
	"""

	fname = sys.argv[1]
	sname = sys.argv[2]
	ident = sys.argv[3]
	#index = int(sys.argv[2])

	data = []

	for index in xrange(-1,-21,-1):
		print(index)

		cdata = {}
		rd = [0,0]
		with open(fname, 'r') as f:
			reader = csv.reader(f, delimiter=',')
			header = next(reader)
			print('Data: {}'.format(header[index]))

			for r in reader:
				if r[0] not in cdata:
					cdata[r[0]] = []
				cdata[r[0]].append(float(r[index]))
				rd[0] = min(rd[0], float(r[1]))
				rd[1] = max(rd[0], float(r[1]))

		
		e = []
		for i in cdata:
			d = stats.distanceFromDecreasing(cdata[i], (rd[1] - rd[0]))
			e.append(d)

		data.append([-5*index, np.mean(e), np.std(e), ident])

	with open(sname, 'a') as f:
		writer = csv.writer(f, delimiter=',')
		for d in data:
			writer.writerow(d)

	#change1 = stats.monotonic(data[0])
	#change2 = stats.monotonic(data[1])
	#change3 = stats.monotonic(data[2])
	#change4 = stats.monotonic(data[3])
	#change5 = stats.monotonic(data[4])

	#print(stats.distanceFromDecreasing(data[3]))

	#print(change1, change2, change3, change4)
