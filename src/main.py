from experiments import kcore
from experiments import ktruss
from experiments import nucleus
from experiments import degree_dist
from experiments import community_exp
from experiments import kcore_temporal
from experiments import ktruss_temporal
from experiments import core_triangles
from experiments import core_min_edges
from experiments import histogram
from data import yahoo_im_clean as yahoo
from data import kcore_graph
import sys

if __name__ == '__main__':
    identifier = int(sys.argv[1])

    if identifier == 0 :
        # k-core experimnet with missing nodes and edges
        fname = sys.argv[2]                 # Input data file
        sname = sys.argv[3]                 # Output file
        adj = int(sys.argv[4]) > 0          # 1 if input file is adjacency list, 0 otherwise
        mode = sys.argv[5]
        kcore_exp = kcore.KCoreExperiment(fname, sname, adj, mode)
        cnumber = kcore_exp.runExperiment(50, 1, 51)

    if identifier == 1 :
        # k-truss experimnet with missing nodes and edges
        fname = sys.argv[2]                 # Input data file
        sname = sys.argv[3]                 # Output file
        adj = int(sys.argv[4]) > 0          # 1 if input file is adjacency list, 0 otherwise
        mode = sys.argv[5]
        ktruss_exp = ktruss.KTrussExperiment(fname, sname, adj, mode)
        tnumber = ktruss_exp.runExperiment(10, 2, 50)

    if identifier == 2 :
        # degree distribution after removing random edges and nodes
        fname = sys.argv[2]                 # Input data file
        sname = sys.argv[3]                 # Output file
        pc = int(sys.argv[4])               # Percentage of missing data

        deg = degree_dist.main(fname, sname, pc)

    if identifier == 3:
        # detect communities
        fname = sys.argv[2]
        adj = int(sys.argv[3]) > 0
        com = community_exp.FindCommunities(fname, adj)
        com.readData()
        com.find()

    if identifier == 4:
        # Clean the yahoo im dateset
        fpath = sys.argv[2]
        spath = sys.argv[3]
        count = int(sys.argv[4])

        fnames = yahoo.filesNames(fpath, count)
        for i, f in enumerate(fnames):
            edges = yahoo.extractEdgelist(f)
            yahoo.saveEdgelist(spath, edges, i)

    if identifier == 5 :
        # k-core experimnet with missing nodes and edges
        fname = sys.argv[2]                 # Input data file
        sname = sys.argv[3]                 # Output file
        adj = int(sys.argv[4]) > 0          # 1 if input file is adjacency list, 0 otherwise
        mode = sys.argv[5]
        nucleus_exp = nucleus.NucleusExperiment(fname, sname, adj, mode)
        cnumber = nucleus_exp.runExperiment(5, 5, 50)

    if identifier == 6:
        fname = sys.argv[2]
        sname = sys.argv[3]

        kcore = kcore_temporal.KCoreExperiment(fname, sname)
        kcore.runExperiment()

    if identifier == 7:
        fname = sys.argv[2]
        sname = sys.argv[3]

        kcore = ktruss_temporal.KTrussExperiment(fname, sname)
        kcore.runExperiment()

    if identifier == 8:
        fname = sys.argv[2]
        sname = sys.argv[3]
        k = int(sys.argv[4])

        ktr = core_triangles.KCoreTriangles(fname, sname)
        ktr.run(k)

    if identifier == 9:
        fname = sys.argv[2]
        sname = sys.argv[3]

        exp = core_min_edges.CoreMinEdgesExperiments(fname, sname)
        exp.run()

    if identifier == 10:
        fname = sys.argv[2]
        sname = sys.argv[3]
        adj = int(sys.argv[4]) > 0

        exp = histogram.KCoreHistogram(fname, sname, adj)
        exp.runExperiment()

    if identifier == 11:
        fname = sys.argv[2]
        sname = sys.argv[3]
        adj = int(sys.argv[4]) > 0
        k = int(sys.argv[5])

        exp = kcore_graph.KCoreGraph(fname, sname, adj)
        exp.runExpRemoveNodes(k)
