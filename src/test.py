"""
Script for testing random stuff
"""

import csv
import sys
import networkx as nx

def readEdgelist(fname):
    g = nx.read_edgelist(fname)
    print(g.number_of_nodes(), g.number_of_edges())
    """
    with open(fname, 'r') as f:
        while f.readline().startswith('#'):
            continue
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            print(row)
    """

if __name__ == '__main__':
    fname = sys.argv[1]

    readEdgelist(fname)
