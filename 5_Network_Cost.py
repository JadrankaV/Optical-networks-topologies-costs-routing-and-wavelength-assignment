import networkx as nx
from array import array
import math
import re
from operator import itemgetter

init=0
CAPEX_models=[]
all_optical_nodes_cost_models=[]
all_links_cost_models=[]
models_names=['RGG','GG','RNG','KNNG','WG','SBAG'] 
models=['Model_RGG_edges.txt','Model_GG_edges.txt','Model_RNG_edges.txt','Model_KNNG_edges.txt','Model_WG_edges.txt','Model_SBAG_edges.txt'] 
for mod in models:
	
	#Graph
	G=nx.Graph()
		
	#Read network arcs from file
	with open(mod, "r") as ins:
		arcs = []
		for line in ins:
			numbers = line.split()
			if line != '\n':
				first = int(numbers[0])
				second= int(numbers[1])
				w=float(numbers[2])
				o=(first,second)		
				G.add_edge(first, second,weight=w) #Add to G
				arcs.append(o)
			
	
	#network nodes
	nodes_number=(max(arcs,key=itemgetter(0))[0])+1
	#print(nodes_number)

	i=0
	labels=[]
	nodes = []
	while i < nodes_number:
		nodes.append(int(i))
		G.add_node(int(i))
		i=i+1


	i=0
	for i in nodes:
		labels.append(i)
		i=i+1
		
	#Read network connection request from file
	with open("Connection_request.txt", "r") as ins:
		connection_request  = []
		for line in ins:
			numbers = line.split()
			if line != '\n':
				first = int(numbers[0])
				second= int(numbers[1])
				o=(first,second)
				connection_request.append(o)
			
	
	C_BASE=200
	C_Trunk=20
	C_Transponder=3

	optical_node_interfaces={}
	optical_transponders={}
	optical_node_cost={}
	all_optical_nodes_cost=0

	for i in G.nodes():
		optical_node_interfaces[i]=C_Trunk*G.degree(i)

	maxPath={}
	for i in G.nodes():
		maxPath[i]=0

	for i in G.nodes():
		for j in connection_request:
			if i==j[0] or i==j[1]:
				maxPath[i]=maxPath[i]+1

	for i in G.nodes():
		optical_transponders[i]=maxPath[i]*C_Transponder

	for i in G.nodes():
		optical_node_cost[i]=C_BASE+optical_node_interfaces[i]+optical_transponders[i]
		all_optical_nodes_cost=all_optical_nodes_cost+optical_node_cost[i]

		
	C_FOkm=1
	C_OA=8   
	SA=80

	optical_fiber_cost={}
	link_cost={}
	all_links_cost=0

	for i in G.edges():
		L=G[i[0]][i[1]]['weight']	
		optical_fiber_cost[i]=L*C_FOkm

	optical_amplifiers_cost={}
	for i in G.edges():
		L=G[i[0]][i[1]]['weight']	
		optical_amplifiers_cost[i]=math.floor(L/SA)*C_OA


	for i in G.edges():
		link_cost[i]=optical_fiber_cost[i]+optical_amplifiers_cost[i]
		all_links_cost=all_links_cost+link_cost[i]

	
	
	CAPEX=all_optical_nodes_cost+all_links_cost
	print(models_names[init],'\t',CAPEX ,'k')
	all_optical_nodes_cost_models.append(all_optical_nodes_cost)
	all_links_cost_models.append(all_links_cost)
	CAPEX_models.append(CAPEX)
	
	init=init+1

file1 = open('CAPEX.txt', 'a')
file2 = open('all_optical_nodes_cost.txt', 'a')
file3 = open('all_links_cost.txt','a')
j=0
for i in models_names:
	file1.write(str(CAPEX_models[j])+' ')
	file2.write(str(all_optical_nodes_cost_models[j])+' ')
	file3.write(str(all_links_cost_models[j])+' ')
	j=j+1
file1.write('\n')
file2.write('\n')
file3.write('\n')