from experiments import kcore
import sys
import os

identifiers = ['p2p09', 'hamster']
vals = range(0, 11)

fpath = sys.argv[1]
spath = sys.argv[2]

if os.path.exists(fpath) and os.path.exists(spath):
	for i in identifiers:
		for v in vals:
			fname = os.path.join(fpath, i + '_' + str(v) + '.csv')
			sname = os.path.join(spath, i + '_' + str(v))

			print('Processing: {}'.format(fname))

			top = range(100, 0, 10)

			kcore_exp = kcore.KCoreExperiment(fname, sname, False, '010', top=top)
			kcore_exp.runExperiment(50, 1, 51)