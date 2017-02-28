import community
import networkx as nx

class FindCommunities(object):
    def __init__(self, fname, adj):
        super(FindCommunities, self).__init__()
        self.fname = fname
        self.adj = adj

    def readData(self):
        if not self.adj:
            self.graph = nx.read_edgelist(self.fname)
        else:
            self.graph = nx.read_adjlist(self.fname)

    def find(self):
        partition = community.best_partition(self.graph)
        print(partition)

if __name__ == '__main__':
    print('No')
