import networkx as nx
import sys
import random
from pprint import pprint

def randomRegularGraph(n, d, sname=None):
    g = nx.random_regular_graph(d,n)
    if sname is not None:
        nx.write_edgelist(g, sname)

def corePeriphery(n1, n2, sname=None):
    pp = 0.20
    pc = 0.80
    mat = [[0 for _ in xrange(0, n1 + n2)] for _ in xrange(0, n1 + n2)]
    for i in xrange(0, n1 + n2):
        for j in xrange(i, n1 + n2):
            if i < n1 and j < n1:
                v = 1 if random.random() < pc else 0
            elif (i < n1 and j >= n1) or (i >= n1 and j < n1) :
                v = 1 if random.random() < pp else 0
            else:
                v = 0
            mat[i][j] = v
            mat[j][i] = v

    # Create the graph
    g = nx.Graph()
    for i in xrange(0, len(mat)):
        for j in xrange(i, len(mat[i])):
            if mat[i][j] == 1:
                g.add_edge(i,j)
    print(nx.info(g))

    if sname is not None:
        nx.write_edgelist(g, sname)

def corePeriphery2(n1, n2, n3, sname=None):
    pp = 0.9
    pc = 0.1
    mat = [[0 for _ in xrange(0, n1 + n2 + n3)] for _ in xrange(0, n1 + n2 + n3)]
    for i in xrange(0, n1):
        for j in xrange(i, n1):
            v = 1 if random.random() < pp else 0
            mat[i][j] = v
            mat[j][i] = v

    core = range(0, n1)
    step = int(n2/5)
    p = pc
    nodes = [range(n1 + i, n1 + i + step) for i in xrange(0, n2, step)]
    count = int(pp * n1) - 5
    for n in nodes:
        p = p - 0.1
        #count = int(n1 * p)
        count -= 1
        for i in n:
            n = random.sample(core, count)
            for j in n:
                mat[i][j] = 1
                mat[j][i] = 1

    nodes = range(n1 + n2, n1 + n2 + n3)
    for n in nodes:
        v = random.choice(core)
        mat[n][v] = 1
        mat[v][n] = 1

    # Create the graph
    g = nx.Graph()
    for i in xrange(0, len(mat)):
        for j in xrange(i, len(mat[i])):
            if mat[i][j] == 1:
                g.add_edge(i,j)
    print(nx.info(g))

    if sname is not None:
        nx.write_edgelist(g, sname)

if __name__ == '__main__':
    """
    sname = sys.argv[1]
    d = int(sys.argv[2])
    n = int(sys.argv[3])

    randomRegularGraph(n, d, sname)
    """
    sname = sys.argv[1]
    n1 = int(sys.argv[2])
    n2 = int(sys.argv[3])
    n3 = int(sys.argv[4])
    corePeriphery2(n1, n2, n3, sname)
