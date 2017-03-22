from __future__ import division, print_function
import networkx as nx
import sys
import pickle

class NucleusDecomposition(object):
    """docstring for NucleusDecomposition."""
    def __init__(self):
        super(NucleusDecomposition, self).__init__()

    def findKClique(self, graph, k, cliques=None):
        pass


    def checkInList(self, candidates, nodes):
        # Check if all the nodes in candidates are in set nodes
        for n in candidates:
            if n not in nodes:
                return False
        return True

    def checkSConnected(self, clique1, clique2, s_set):
        # clique1 is list of cliques
        # clique2 is a clique

        # If already in list no need to say s connected
        if clique2 in clique1:
            return False
        s = len(s_set[0])
        clique_list = list(clique1)
        for c in clique_list:
            un = c.union(clique2)
            if len(un) == s:
                if un in s_set:
                    return True
        return False

    def decomposition(self, graph):
        r = 3
        cliques = {}
        cliques[2] = set([frozenset(e) for e in graph.edges()])
        stop = False
        r = 3
        while not stop:
            temp = set()
            itemp = set(cliques[r-1])
            for x in cliques[r-1]:
                itemp.remove(x)
                for y in itemp:
                    xuy = set(x).union(y)
                    xiy = set(x).intersection(y)

                    if len(xiy) == r-2 and frozenset(xuy) not in temp:
                        z = list(xuy.difference(xiy))
                        if len(z) == 2 and frozenset([z[0],z[1]]) in cliques[2]:
                            temp.add(frozenset(xuy))
                            print(r, len(temp), frozenset(xuy))
            stop = not(len(temp) > 0)
            if not stop:
                cliques[r] = set(temp)
                print(r, len(cliques[r]))
                r += 1

        print([(k, len(cliques[k])) for k in cliques.keys()])

        # Remove 2 cliques
        print(cliques.keys())
        cliques.pop(2,None)
        print(cliques.keys())

        nucleii_membership = {}
        nucleii_sets = {}

        r = min(cliques.keys())
        while r <= max(cliques.keys()) - 1:
            s = r + 1
            while s <= max(cliques.keys()):
                print(r,s)
                r_clique = list(cliques[r])
                s_clique = list(cliques[s])

                # Pruning
                # Only nodes in s cliques are candidates for merging
                s_clique_nodes = set([n for clique in s_clique for n in clique])
                # Candate nodes in r cliques have to be part of some s clique
                r_clique = [c for c in r_clique if self.checkInList(c, s_clique_nodes)]
                print('r_clique after pruning',len(r_clique))

                nucleii = [[clique] for clique in r_clique]
                updated = True
                while updated:
                    updated = False
                    for c1 in nucleii:
                        for c2 in r_clique:
                            if self.checkSConnected(c1, c2, s_clique):
                                c1.append(c2)
                                updated = True
                    nucleii = map(list,list(set(map(frozenset,nucleii))))
                    # Prune nucleus of size smaller than s
                    nucleii = [n for n in nucleii if len(n) >= s]
                    print('Candidate Nucleii: {}'.format(len(nucleii)))

                    temp = []
                    members = []
                    for nucleus in nucleii:
                        temp.append(frozenset(set().union(*nucleus)))
                        members = set(members).union(*nucleus)
                    nucleii_sets[(r,s)] = temp

                    for m in members:
                        if m not in nucleii_membership:
                            nucleii_membership[m] = []
                        if (r,s) not in nucleii_membership[m]:
                            nucleii_membership[m].append((r,s))
                    print(nucleii_membership)

                s += 1
            r += 1

        return nucleii_sets, nucleii_membership

    def saveResults(self, nucleii_sets, nucleii_membership, sname):
        f1 = open(sname+'_sets.pickle', 'w')
        f2 = open(sname+'_membership.pickle', 'w')

        pickle.dump(nucleii_sets, f1)
        pickle.dump(nucleii_membership, f2)

if __name__ == '__main__':
    fname = sys.argv[1]
    sname = sys.argv[2]

    graph = nx.read_edgelist(fname)
    #graph = nx.complete_graph(10)
    #graph.add_edges_from([(12,13),(12,14),(12,15),(13,14),(13,15),(14,15)])

    nc = NucleusDecomposition()
    nucleii, members = nc.decomposition(graph)
    nc.saveResults(nucleii, members, sname)
