from __future__ import division, print_function
import networkx as nx
import numpy as np
import sys
import os
import cPickle as pickle
import time
import csv


def readData(fname, k1, k2):
	data1 = {}
	data2 = {}
	with open(fname, 'r') as f:
		reader = csv.reader(f)
		reader.next()
		for r in reader:
			if k1 == int(r[4]):
				data1[(int(r[0]), int(r[1]))] = float(r[2])
			elif k2 == int(r[4]):
				data2[(int(r[0]), int(r[1]))] = float(r[2])
	return data1, data2

def difference(dat1, dat2, name):
	data = []
	for d in dat1:
		if d in dat2:
			data.append([d[0], d[1], round((dat2[d] - dat1[d])/min(dat2[d], dat1[d]),1), name])
	return data

def saveData(sname, data):
	with open(sname, 'w') as f:
		writer = csv.writer(f, delimiter=',')
		writer.writerow(['p', 'k', 'diff', 'name'])
		for d in data:
			writer.writerow(d)

if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]
	k1 = int(sys.argv[3])
	k2 = int(sys.argv[4])

	data1, data2 = readData(fname, k1, k2)
	diff = difference(data1, data2, str(k1) + '_' + str(k2))
	saveData(sname, diff)