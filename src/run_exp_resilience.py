import os
import sys

fname = sys.argv[1]
sname = sys.argv[2]
alg = sys.argv[3]
name = sys.argv[4]

x = 0.25
for i in xrange(0,21):
	f = fname + str(x*i) + '.csv'
	print(f)
	if name == 'CICS':
		print('Mode: {}'.format(name))
		l = str(1) if i == 0 else str(0)
		os.system('python src/csci.py ' + f + ' ' + sname + ' ' + str(x*i) + ' ' + l +' ' + name + ' ' + alg + ' ' + str(x*i))
	else:
		print('Baseline Mode: {}'.format(name))
		#os.system('python src/csci.py ' + f + ' ' + sname + ' ' + str(x*i) + ' ' + str(0) +' ' + name + ' ' + alg + ' ' + str(x*i))
		os.system('python src/csci.py ' + f + ' ' + sname + ' ' + str(x*i) + ' ' + str(0) +' ' + name + ' ' + alg + ' ' + str(0))