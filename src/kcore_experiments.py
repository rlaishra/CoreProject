from experiments import kcore
import sys
import os

identifiers = ['p2p_09_10', 'hamster_10', 'grqc_10', 'p2p_09_25', 'hamster_25', 'grqc_25']
#identifiers = ['hamster_10', 'hamster_25']
identifiers = ['p2p_09_10', 'hamster_10', 'grqc_10']
vals = range(0, 10)

fpath = sys.argv[1]
spath = sys.argv[2]

if os.path.exists(fpath) and os.path.exists(spath):
	for i in identifiers:
		for v in vals:
			fname = os.path.join(fpath, i + '_' + str(v) + '.csv')
			sname = os.path.join(spath, i + '_' + str(v))

			print('Processing: {}'.format(fname))

			kcore_exp = kcore.KCoreExperiment(fname, sname, False, '010')
			kcore_exp.runExperiment(10, 1, 51)