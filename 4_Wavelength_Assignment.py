import networkx as nx
#import matplotlib.pyplot as plt
#import pylab


init=0
WA_models=[]
models_names=['RGG','GG','RNG','KNNG','WG','SBAG'] 
models_arcs=['WA_RGG_arcs.txt','WA_GG_arcs.txt','WA_RNG_arcs.txt','WA_KNNG_arcs.txt','WA_WG_arcs.txt','WA_SBAG_arcs.txt'] 
models_nodes=['WA_RGG_nodes.txt','WA_GG_nodes.txt','WA_RNG_nodes.txt','WA_KNNG_nodes.txt','WA_WG_nodes.txt','WA_SBAG_nodes.txt'] 
models_path=['WA_RGG_path.txt','WA_GG_path.txt','WA_RNG_path.txt','WA_KNNG_path.txt','WA_WG_path.txt','WA_SBAG_path.txt'] 

for mod in models_names:
	with open(models_nodes[init], "r") as ins:
		nodes = []
		for line in ins:
			if line != '\n':
				nodes.append(int(line))

	with open(models_arcs[init], "r") as ins:
		arcs = []
		for line in ins:
			numbers = line.split()
			if line != '\n':
				first = numbers[0]
				second= numbers[1]
				o=(int(first),int(second))
				arcs.append(o)
			

	G=nx.Graph()

	i=1
	colors=[]
	while i<len(nodes):
		colors.append(i)
		i=i+1
		

	G.add_nodes_from(nodes)
	G.add_edges_from(arcs)
	colors_of_nodes={}


	def coloring(node, color):
		for neighbor in G.neighbors(node):
			color_of_neighbor = colors_of_nodes.get(neighbor, None)
			if color_of_neighbor == color:
				return False

		return True

	def get_color_for_node(node):
		for color in colors:
			if coloring(node, color):
				return color

	def main():
		max_color=0
		for node in G.nodes():
			colors_of_nodes[node] = get_color_for_node(node)
			if max_color<colors_of_nodes[node]:
				max_color=colors_of_nodes[node]
		
		WA_models.append(max_color)
		
		

		

		
	#Print colors of nodes
	main()
	init=init+1

	
file = open('WA.txt', 'a')
j=0
for i in models_names:
	file.write(str(WA_models[j])+' ')
	j=j+1
file.write('\n')
