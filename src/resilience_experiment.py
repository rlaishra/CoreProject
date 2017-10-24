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
'outputs/oct_23/resilience/as19971108',
'outputs/oct_23/resilience/as19971122',
'outputs/oct_23/resilience/as19980201',
'outputs/oct_23/resilience/as19980711',
'outputs/oct_23/resilience/as19990217',
'outputs/oct_23/resilience/as19990309',
'outputs/oct_23/resilience/Oregon1_010331',
'outputs/oct_23/resilience/Oregon1_010428',
'outputs/oct_23/resilience/inf-openflights',
'outputs/oct_23/resilience/inf-power',
'outputs/oct_23/resilience/inf-USAir97',
'outputs/oct_23/resilience/tech-pgp',
'outputs/oct_23/resilience/tech-routers-rf',
'outputs/oct_23/resilience/tech-WHOIS',
'outputs/oct_23/resilience/p2p-Gnutella08',
'outputs/oct_23/resilience/p2p-Gnutella09',
'outputs/oct_23/resilience/p2p-Gnutella24',
'outputs/oct_23/resilience/p2p-Gnutella25',
]

k = 25
mode = 'alg_node'

if __name__ == '__main__':
	for i in xrange(0, len(fnames)):
		command = 'python src/improve_resilience.py {} {} {} {}'.format(fnames[i], snames[i], k, mode)
		print(command)
		os.system(command)
