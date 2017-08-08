from __future__ import division, print_function

from utils import statistics as st
import sys
import csv
import numpy as np
import os

def readData(fname, i):
	data = {}
	with open(fname, 'r') as f:
		reader = csv.reader(f, delimiter=',')
		header = next(reader)
		print('Reading: {}'.format(header[i]))

		for row in reader:
			if row[0] not in data:
				data[row[0]] = []
			data[row[0]].append(float(row[i]))
	return data

def main(fname, i):
	data = readData(fname, i)
	stats = st.Statistics()

	dist = []

	for i in data:
		d = data[i]
		dist.append(stats.distanceFromDecreasing(d))
		#dist.append(stats.monotonic(d))
	
	m = np.mean(dist)
	s = np.std(dist)

	print('Distance Mean: {} \t Std: {}'.format(m,s))

	return m, s

if __name__ == '__main__':
	identifiers = ['p2p09_10', 'hamster_10']
	vals = range(0, 11)
	#identifiers = ['hamster_10']
	#vals = range(0,4)

	fpath = sys.argv[1]
	spath = sys.argv[2]

	if os.path.exists(fpath) and os.path.exists(spath):
		for i in identifiers:
			sname = os.path.join(spath, i + '_error.csv')
			header = ['edges']
			for x in xrange(5, 100, 5):
			#for x in xrange(5, 10, 5):
				header += ['mean_' + str(x), 'std_' + str(x)]

			data = [header]
			for v in vals:
				fname = os.path.join(fpath, i + '_' + str(v) + '_core_edges_delete_random.results')
				print('Processing: {}'.format(fname))
				tdata = [v]
				for j in xrange(5,100,5):
				#for j in xrange(5, 10, 5):
					k = int((100 - j)/5) + 2

					m, s = main(fname, k)
					tdata += [m,s]
				data.append(tdata)
		
			with open(sname, 'w') as f:
				writer = csv.writer(f, delimiter=',')
				for d in data:
					writer.writerow(d)