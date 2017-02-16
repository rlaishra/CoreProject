from __future__ import division, print_function
import sys
import graph_tool.all as gt
import csv
import random

def readData(fname, directed=False):
    g = gt.Graph(directed=directed)
    edges = []
    with open(fname, 'r') as f:
        reader = csv.reader(f, delimiter=' ', quotechar='"')
        for row in reader:
            if row[0] != row[1]:
                if directed:
                    edges.append((row[0],row[1]))
                if not directed:
                    edges.append((min(row[0],row[1]), max(row[0],row[1])))
    if not directed:
        edges = list(set(edges))
    g.add_edge_list(edges, hashed=True)
    return g

def draw(g,sname):
    pos = gt.sfdp_layout(g, max_iter=100, multilevel=True)
    #pos = gt.random_layout(g)
    gt.graph_draw(g, pos, output_size=(1000,1000),output=sname)

def randomWalk(g, directed=False, count = 1000):
    sample = gt.Graph(directed=directed)
    current = g.vertex(random.randint(0,g.num_vertices()))

    edges = []
    vertices = []
    i = 0

    for i in xrange(0,count):
        neighbors = []
        if not directed:
            for n in current.all_neighbours():
                edges.append((min(current,n), max(current,n)))
                neighbors.append(n)
        if directed:
            for n in current.out_neighbours():
                edges.append((current,n))
                neighbors.append(n)
        current = random.sample(neighbors,1)[0]
        vertices.append(n)
        if random.random() < 0.1:
            vertices = list(set(vertices))
            current = random.sample(vertices,1)[0]

    if not directed:
        edges = list(set(edges))
    sample.add_edge_list(edges, hashed=True)

    return sample, edges

def saveSample(sample, sname, count):
    fname = sname + '_count.edgelist'
    with open(fname, 'w') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"')
        for e in sample:
            writer.writerow(e)

if __name__ == '__main__':
    fname = sys.argv[1]
    sname = sys.argv[2]
    directed = int(sys.argv[3]) > 0

    g = readData(fname, directed)

    #nodeStatistics(g)

    s, edges = randomWalk(g,directed,50000)

    draw(s,sname)
    #draw(g, sname)
