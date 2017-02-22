from experiments import kcore
from experiments import ktruss
from experiments import degree_dist
import sys

if __name__ == '__main__':
    identifier = int(sys.argv[1])

    if identifier == 0 :
        fname = sys.argv[2]                 # Input data file
        sname = sys.argv[3]                 # Output file
        adj = int(sys.argv[4]) > 0          # 1 if input file is adjacency list, 0 otherwise
        kcore_exp = kcore.KCoreExperiment(fname, sname, adj)
        cnumber = kcore_exp.runExperiment(10, 2, 50)
        #print(cnumber)

    if identifier == 1 :
        fname = sys.argv[2]                 # Input data file
        sname = sys.argv[3]                 # Output file
        adj = int(sys.argv[4]) > 0          # 1 if input file is adjacency list, 0 otherwise
        ktruss_exp = ktruss.KTrussExperiment(fname, sname, adj)
        tnumber = ktruss_exp.runExperiment(10, 2, 50)

    if identifier == 2 :
        fname = sys.argv[2]                 # Input data file
        sname = sys.argv[3]                 # Output file
        pc = int(sys.argv[4])               # Percentage of missing data

        deg = degree_dist.main(fname, sname, pc)
