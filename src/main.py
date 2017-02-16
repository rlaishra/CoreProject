from experiments import kcore
import sys

if __name__ == '__main__':
    identifier = int(sys.argv[1])

    if identifier == 0 :
        fname = sys.argv[2]
        sname = sys.argv[3]
        kcore_exp = kcore.KCoreExperiment(fname, sname)
        kcore_exp.runExperimentNode(5,20)
