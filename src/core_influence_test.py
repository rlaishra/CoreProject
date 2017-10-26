import sys
import os


fnames = [
'data/as-733/as19971108.txt',
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
'data/p2p-Gnutella25.txt',
'data/web-spam/web-spam.mtx',
'data/web-webbase-2001/web-webbase-2001.mtx',
'data/grqc.csv',
'data/ca-HepTh.csv',
'data/ca-Erdos992/ca-Erdos992.mtx',
'data/soc-hamsterster/soc-hamsterster.edges',
'data/soc-advogato/soc-advogato.csv',
'data/soc-wiki-Vote/soc-wiki-Vote.mtx',
'data/bio-dmela/bio-dmela.mtx',
'data/bio-yeast-protein-inter/bio-yeast-protein-inter.edges',
]

names = [
'AS_733_19971108',
'AS_733_19990309',
'AS_Oregon_010331',
'AS_Oregon_010428',
'INF_OpenFlights',
'INF_PowerGrid',
'INF_USAir',
'TECH_PGP',
'TECH_Router',
'TECH_WHOIS',
'P2P_Gnutella08',
'P2P_Gnutella09',
'P2P_Gnutella25',
'WEB_Spam',
'WEB_Webbase',
'CA_GrQc',
'CA_HepTH',
'CA_Erdos',
'SOC_Hamsterster',
'SOC_Advogato',
'SOC_WikiVote',
'BIO_Dmela',
'BIO_Yeast'
]

ntype = [
'AS',
'AS',
'AS',
'AS',
'INF',
'INF',
'INF',
'TECH',
'TECH',
'TECH',
'P2P',
'P2P',
'P2P',
'WEB',
'WEB',
'CA',
'CA',
'CA',
'SOC',
'SOC',
'SOC',
'BIO',
'BIO'
]

sname = 'outputs/oct_24/resilience/original_edges.csv'

mode = 'edges'

if __name__ == '__main__':
	for i in xrange(0, len(fnames)):
		n = 1 if i == 0 else 0
		command = 'python src/csci.py {} {} {} {} {} {} {}'.format(fnames[i], sname, names[i], n, ntype[i], mode, 0 )
		print(command)
		os.system(command)
