import csv
import sys

def filesNames(path, count):
    fnames = []
    for x in xrange(0, count):
        fn = path + str(x) + '.txt'
        fnames.append(fn)
    return fnames

def extractEdgelist(fname):
    edges = []
    with open(fname, 'r') as f:
        reader = csv.reader(f, delimiter=' ')
        for row in reader:
            edges.append((row[2], row[4]))
    edges = list(map(list, set(map(frozenset, edges))))
    return edges

def saveEdgelist(spath, edges, index):
    fname = spath + str(index) + '.csv'
    with open(fname, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        for e in edges:
            writer.writerow(e)


if __name__ == '__main__':
    path = sys.argv[1]
    spath = sys.argv[2]
    count = int(sys.argv[3])

    fnames = filesNames(path, count)

    for i, f in enumerate(fnames):
        edges = extractEdgelist(f)
        print(len(edges))
        saveEdgelist(spath, edges, i)
