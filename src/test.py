"""
Script for testing random stuff
"""

import csv
import sys
import networkx as nx
from utils import statistics
from pprint import pprint
import numpy as np

def readData(fname):
    data = {}
    with open(fname, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        headers = next(reader)
        for h in headers:
            data[h] = []
        for row in reader:
            for i,_ in enumerate(row):
                data[headers[i]].append(float(row[i]))
    return data

def caluclateMonotonic(data):
    stats = statistics.Statistics()

    for d in data:
        u = np.polyfit(data['change'], data[d] ,deg=1, full=True)
        v = stats.monotonic(data[d])
        w = np.polyfit(data['change'], data[d] ,deg=2, full=True)
        x = stats.increasing(data[d])
        pprint((d, v, x, u[1][0], w[1][0]))

if __name__ == '__main__':
    fname = sys.argv[1]

    data = readData(fname)
    caluclateMonotonic(data)
