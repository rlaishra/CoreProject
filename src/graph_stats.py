import networkx as nx
import csv, sys

def readGraph(fname):
	if fname.endswith('mtx'):
		edges = []
		with open(fname, 'r') as f:
			reader = csv.reader(f, delimiter=' ')
			for row in reader:
				if len(row) == 2:
					edges.append(row)
		graph = nx.Graph()
		graph.add_edges_from(edges)
	else:
		graph = nx.read_edgelist(fname, delimiter=',')
		
		if graph.number_of_edges() == 0:
			graph = nx.read_edgelist(fname, delimiter='\t')
		if graph.number_of_edges() == 0:
			graph = nx.read_edgelist(fname, delimiter=' ')

	graph.remove_edges_from(graph.selfloop_edges())
	isolates = nx.isolates(graph)
	graph.remove_nodes_from(isolates)
	#print(nx.info(graph))
	return graph


if __name__ == '__main__':
	fname = sys.argv[1]
	graph = readGraph(fname)
	cnumber = nx.core_number(graph)
	deg = max(cnumber.values())

	print('Nodes:\t{}'.format(graph.number_of_nodes()))
	print('Edges:\t{}'.format(graph.number_of_edges()))
	print('Degen:\t{}'.format(deg))