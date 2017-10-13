import sys
import os

fnames = [
'data/as-733/as19971108.txt',
'data/as-733/as19971122.txt',
'data/as-733/as19980201.txt',
'data/as-733/as19980711.txt',
'data/as-733/as19990217.txt',
'data/as-733/as19990309.txt',
'data/Oregon1_010331.txt',
'data/Oregon1_010428.txt',
'data/inf-openflights/inf-openflights.edges',
'data/inf-power/inf-power.mtx',
'data/inf-USAir97/inf-USAir97.csv',
'data/tech-pgp/tech-pgp.edges',
'data/tech-routers-rf/tech-routers-rf.mtx',
'data/tech-WHOIS/tech-WHOIS.mtx',
'data/p2p-Gnutella08.csv',
'data/p2p-Gnutella09.csv',
'data/p2p-Gnutella24.txt',
'data/p2p-Gnutella25.txt',
]

snames = [
'outputs/oct_13/as19971108',
'outputs/oct_13/as19971122',
'outputs/oct_13/as19980201',
'outputs/oct_13/as19980711',
'outputs/oct_13/as19990217',
'outputs/oct_13/as19990309',
'outputs/oct_13/Oregon1_010331',
'outputs/oct_13/Oregon1_010428',
'outputs/oct_13/inf-openflights',
'outputs/oct_13/inf-power',
'outputs/oct_13/inf-USAir97',
'outputs/oct_13/tech-pgp',
'outputs/oct_13/tech-routers-rf',
'outputs/oct_13/tech-WHOIS',
'outputs/oct_13/p2p-Gnutella08',
'outputs/oct_13/p2p-Gnutella09',
'outputs/oct_13/p2p-Gnutella24',
'outputs/oct_13/p2p-Gnutella25',
]

if __name__ == '__main__':
	for i in xrange(0, len(fnames)):
		command = 'python src/improve_robustness.py {} {} 25 alg'.format(fnames[i], snames[i])
		os.system(command)