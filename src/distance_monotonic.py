from __future__ import division, print_function

from utils import statistics as st
import sys
import csv
import numpy as np

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

if __name__ == '__main__':
	fname = sys.argv[1]
	i = int(sys.argv[2]) 			# The top i nodes
	k = int(sys.argv[3]) + 1		# The cost upto which error is calculated

	i = int((100 - i)/10) + 2

	print('Max Removed: {}'.format(k-1))

	data = readData(fname, i)
	stats = st.Statistics()

	dist = []

	for i in data:
		d = data[i][:k]
		dist.append(stats.distanceFromDecreasing(d))
	
	m = np.mean(dist)
	s = np.std(dist)

	print('Distance Mean: {} \t Std: {}'.format(m,s))