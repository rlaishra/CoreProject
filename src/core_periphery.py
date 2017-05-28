from __future__ import division, print_function

import coreness as cr
import networkx as nx
import sys
import os
from pprint import pprint

class CorePeriphery(object):
    """docstring for CorePeriphery."""
    def __init__(self, dirname, sname):
        super(CorePeriphery, self).__init__()
        self._dir = dirname
        self._allowed_extensions = ['.csv', '.edgelist', '.mtx']
        self._fpaths = self._getFiles()
        self._max_nodes = 20000
        self._sname = sname

    def _readMtx(self, fpath):
        edges = []
        with open(fpath, 'r') as f:
            reader = csv.reader(f, delimiter=' ')
            for row in reader:
                if len(row) == 2:
                    edges.append(row)
        return edges

    def _getFiles(self):
        # Get all the files under the given dir
        fpaths = {}
        for (dirpath, dirnames, filenames) in os.walk(self._dir):
            for f in filenames:
                fname, ext = os.path.splitext(f)
                if ext in self._allowed_extensions:
                    fpaths[fname] = {'path': os.path.join(dirpath, f), 'ext': ext}
        return(fpaths)

    def _readFile(self, fdata):
        if fdata['ext'] == '.mtx':
            edges = self._readMtx(fdata['path'])
            graph = nx.Graph()
            graph.add_edges_from(edges)
        else:
            graph = nx.read_edgelist(fdata['path'], comments=comment)

        if graph.number_of_nodes() <= self._max_nodes:
            print(nx.info(graph))
            return graph
        else:
            return None

    def main(self):
        sfile = open(self._sname, 'w')
        print('fname, exp_number, correlation', file=sfile)
        print(self._fpaths)
        for fname in self._fpaths:
            graph = self._readFile(self._fpaths[fname])
            if graph is None:
                continue
            for x in xrange(0, 5):
                c = cr.coreness(s, return_correlation=True)
                print('{} \t Network: {} \t Correlation: {}'.format(x, fname, c[1]))
                print('{},{},{}'.format(x, fname, c), file=sfile)

if __name__ == '__main__':
    fname = sys.argv[1]
    sname = sys.argv[2]

    cp = CorePeriphery(fname, sname)
    cp.main()
