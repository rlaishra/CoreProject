"""
Reformats the outputs of kcore experiment
"""

import csv
import sys

def readFile(fname):
	cdata = {}
	
	for x in xrange(0,10):
		data = []
		tname = fname + str(x) + '_core_mean_edges_delete_random.csv'
		
		with open(tname, 'r') as f:
			reader = csv.reader(f, delimiter=',')
			reader.next()
			
			for row in reader:
				data.append(row)
	
		cdata[x] = data
	return cdata

def reformatData(data):
	ndata = []
	header = ['added', 'change', 'mean', 'std', 'nodes']
	ndata.append(header)

	for x in data:
		for row in data[x]:
			for i in xrange(0, 20):
				j = 2*i - 1
				k = 2*i
				n = 100 - 5*i
				ndata.append(map(float,[x, row[0], row[j], row[k], n]))
	return ndata

def saveData(sname, data):
	with open(sname, 'w') as f:
		writer = csv.writer(f, delimiter=',')
		for row in data:
			writer.writerow(row)

if __name__ == '__main__':
	fname = sys.argv[1]
	sname = sys.argv[2]

	data = readFile(fname)
	data = reformatData(data)
	saveData(sname, data)

	