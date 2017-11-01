import sys
import os

fnames = [
'data/as-733/as19971108.txt',
'data/as-733/as19990309.txt',
#'data/Oregon1_010331.txt',
#'data/Oregon1_010428.txt',
'data/inf-openflights/inf-openflights.edges',
'data/inf-power/inf-power.mtx',
'data/inf-USAir97/inf-USAir97.csv',
#'data/tech-pgp/tech-pgp.edges',
'data/tech-routers-rf/tech-routers-rf.mtx',
'data/tech-WHOIS/tech-WHOIS.mtx',
'data/p2p-Gnutella08.csv',
'data/p2p-Gnutella09.csv',
#'data/p2p-Gnutella25.txt',
'data/web-spam/web-spam.mtx',
'data/web-webbase-2001/web-webbase-2001.mtx',
'data/grqc.csv',
#'data/ca-HepTh.csv',
'data/ca-Erdos992/ca-Erdos992.mtx',
'data/soc-hamsterster/soc-hamsterster.edges',
#'data/soc-advogato/soc-advogato.csv',
'data/soc-wiki-Vote/soc-wiki-Vote.mtx',
'data/bio-dmela/bio-dmela.mtx',
'data/bio-yeast-protein-inter/bio-yeast-protein-inter.edges',
]

snames = [
'outputs/oct_29/data/as19971108',
'outputs/oct_29/data/as19990309',
#'outputs/oct_29/data/Oregon1_010331',
#'outputs/oct_29/data/Oregon1_010428',
'outputs/oct_29/data/inf-openflights',
'outputs/oct_29/data/inf-power',
'outputs/oct_29/data/inf-USAir97',
#'outputs/oct_29/data/tech-pgp',
'outputs/oct_29/data/tech-routers-rf',
'outputs/oct_29/data/tech-WHOIS',
'outputs/oct_29/data/p2p-Gnutella08',
'outputs/oct_29/data/p2p-Gnutella09',
#'outputs/oct_29/data/p2p-Gnutella25',
'outputs/oct_29/data/web-spam',
'outputs/oct_29/data/web-webbase-2001',
'outputs/oct_29/data/ca-grqc',
#'outputs/oct_29/data/ca-HepTh',
'outputs/oct_29/data/ca-Erdos992',
'outputs/oct_29/data/soc-hamsterster',
#'outputs/oct_29/data/soc-advogato',
'outputs/oct_29/data/soc-wiki-Vote',
'outputs/oct_29/data/bio-dmela',
'outputs/oct_29/data/bio-yeast-protein-inter'
]

k = 25

if __name__ == '__main__':
	mode = sys.argv[1]
	for i in xrange(0, len(fnames)):
		command = 'python src/improve_resilience.py {} {} {} {}'.format(fnames[i], snames[i], k, mode)
		print(command)
		os.system(command)
