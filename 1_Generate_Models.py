import networkx as nx
import matplotlib.pyplot as plt
import random
import math
import numpy as np
import sys

nodes_number=int(sys.argv[1])

labels={}
coordinates={}

RGG=nx.Graph() 
GG=nx.Graph() 
RNG=nx.Graph() 
KNNG=nx.Graph()
WG=nx.Graph()
SBAG = nx.Graph();

nodes=RGG.nodes()

xmin=0
xmax=3000
ymin=0
ymax=3000

def Coordinates():
	
	#Generate_coordinates
	'''
	i=0
	file = open('coordinates.txt', 'w')
	while i<nodes_number:
		coordinates[i]=(xmin + ((xmax-xmin)*random.random()),ymin + ((ymax-ymin)*random.random()))
		file.write(str(coordinates[i][0])+' '+str(coordinates[i][1])+'\n')
		i=i+1
	'''
		
	i=0
	with open("coordinates.txt", "r") as ins:
		for line in ins:
			if line != '\n':
				line_el=line.split()
				coordinates[i]=(float(line_el[0]),float(line_el[1]))
				i=i+1
		
	i=0	
	while i<nodes_number:
		RGG.add_node(i,pos=coordinates[i]) 
		GG.add_node(i,pos=coordinates[i]) 
		RNG.add_node(i,pos=coordinates[i]) 
		KNNG.add_node(i,pos=coordinates[i])
		SBAG.add_node(i,pos=coordinates[i])
		i=i+1

def Normalize(lista):
	sum=0
	for i in lista:
		sum=sum+i
	new_lista=[]
	for i in lista:
		new_lista.append(i/sum)
	return new_lista

def RandomGeometricGraph():
	RemoveEdge(RGG)
	r=450
	for i in nodes:
		for j in nodes:
			if i!=j and distances[i][j]<=r:
				RGG.add_edge(i,j,weight=distances[i][j])		

def GabrielGraph():
	RemoveEdge(GG)
	for i in nodes:
		for j in nodes:
			if i!=j:
				a=distances[i][j]*distances[i][j]
				tmp=0
				for k in nodes:
					if k!=i and k!=j:
						b=distances[i][k]*distances[i][k]
						c=distances[j][k]*distances[j][k]
						if a<=b+c:
							tmp=tmp+1
				#if tmp==(nodes_number-2):
				if tmp>=(nodes_number-2):
					GG.add_edge(i,j)

def RelativeNeighborhoodGraph():
	RemoveEdge(RNG)
	for i in nodes:
		for j in nodes:
			if i!=j:
				a=distances[i][j]*distances[i][j]
				tmp=0
				for k in nodes:
					if k!=i and k!=j: 
						b=distances[i][k]*distances[i][k]
						c=distances[j][k]*distances[j][k]
						if a<=max(b,c):
							tmp=tmp+1
				if tmp>=(nodes_number-2):
					RNG.add_edge(i,j)
					
def KNearestNeighborGraph():
	RemoveEdge(KNNG)
	dis_sort=np.array(distances)
	dis_sort.sort(axis=1)
	k=5
	for i in nodes:
		for j in nodes:
			if i!=j and distances[i][j]<=dis_sort[i][k]:			
				KNNG.add_edge(i,j)
	

def WaxmanGraph():
	n=nodes_number
	alpha=0.7
	beta=0.11
	L=None
	domain=(0, 0, 4000, 4000)
	
	# build graph of n nodes with random positions in the unit square
	RemoveEdge(WG)
	WG.add_nodes_from(range(n))
	(xmin,ymin,xmax,ymax)=domain
	for n in WG:
		WG.node[n]['pos']=coordinates[n]
		
	if L is None:
		# find maximum distance L between two nodes
		l = 0
		pos = list(nx.get_node_attributes(WG,'pos').values())
		while pos:
			x1,y1 = pos.pop()
			for x2,y2 in pos:
				r2 = (x1-x2)**2 + (y1-y2)**2
				if r2 > l:
					l = r2
		l=math.sqrt(l)
	else:
		# user specified maximum distance
		l = L

	nodes=WG.nodes()
	if L is None:
		# Waxman-1 model
		# try all pairs, connect randomly based on euclidean distance
		while nodes:
			u = nodes.pop()
			x1,y1 = WG.node[u]['pos']
			for v in nodes:
				x2,y2 = WG.node[v]['pos']
				r = math.sqrt((x1-x2)**2 + (y1-y2)**2)
				if random.random() < alpha*math.exp(-r/(beta*l)):
					WG.add_edge(u,v)
	else:
		# Waxman-2 model
		# try all pairs, connect randomly based on randomly chosen l
		while nodes:
			u = nodes.pop()
			for v in nodes:
				r = random.random()*l
				if random.random() < alpha*math.exp(-r/(beta*l)):
					WG.add_edge(u,v)
	
def SpatialBarabasiAlbertGraph():
	n=nodes_number
	mlinks=3
	alpha=4
	RemoveEdge(SBAG)
	seed={(0,1),(0,2),(0,3),(1,3),(2,3)}
	for i in seed:
		SBAG.add_edge(i[0],i[1]) #init graph

	
	sumlinks=len(SBAG.edges())
	probability=[[0 for i in nodes] for i in nodes]	
	degree={}
	for i in nodes:
		for j in nodes:
			if i!=j:
				probability[i][j]=1.0/pow(distances[i][j],alpha)
			

	pos=4

	while pos  < nodes_number:
		
		j=0
		degree_sum=0
		for i in nodes:
			degree[i]=SBAG.degree(i)
			degree_sum=degree_sum+degree[i]
		prob=[]
		while j < nodes_number:
			if pos==j:
				prob.append(0)
			if pos!=j:
				prob.append(probability[pos][j]*(float(degree[j])/float(degree_sum)))
			j = j + 1;
		G_add_nodes=np.random.choice(len(prob), mlinks, replace=False,  p=Normalize(prob))	
		
		for i in G_add_nodes:
			SBAG.add_edge(pos,i)
		pos = pos + 1
	
def drawGraph(Graph,color,name):
	edges=Graph.edges()
	pos_G=nx.get_node_attributes(Graph,'pos')
	nx.draw_networkx_nodes(Graph,pos_G,nodes,node_color=color,node_size=200,alpha=1)
	nx.draw_networkx_edges(Graph,pos_G,edges,width=2,alpha=0.5)
	plt.savefig(str(name)+'.png', format="PNG")
	plt.show()

def RemoveEdge(Graph):
	for i in Graph.edges():
		Graph.remove_edge(i[0],i[1])

def callRGG():
	print("Generating RGG")
	RandomGeometricGraph()
	if nx.is_connected(RGG):
		file = open('Model_RGG_edges.txt', 'w')
		for i in RGG.edges():
			file.write(str(i[0])+str(' ')+str(i[1])+str(' ')+str(distances[i[0]][i[1]])+'\n')
			file.write(str(i[1])+str(' ')+str(i[0])+str(' ')+str(distances[i[0]][i[1]])+'\n')
		drawGraph(RGG,'blue','RandomGeometricGraph')
	else:
		print("RGG is not connected")
		sys.exit()
	

def callWG():
	print("Generating WG")
	while True:		
		WaxmanGraph()
		if nx.is_connected(WG):
			file = open('Model_WG_edges.txt', 'w')
			for i in WG.edges():
				file.write(str(i[0])+str(' ')+str(i[1])+str(' ')+str(distances[i[0]][i[1]])+'\n')
				file.write(str(i[1])+str(' ')+str(i[0])+str(' ')+str(distances[i[0]][i[1]])+'\n')	
			drawGraph(WG,'yellow','WaxmanGraph')
			break
				
def callGG():
	print("Generating GG")
	while True:
		GabrielGraph()
		if nx.is_connected(GG):
			file = open('Model_GG_edges.txt', 'w')
			for i in GG.edges():
				file.write(str(i[0])+str(' ')+str(i[1])+str(' ')+str(distances[i[0]][i[1]])+'\n')
				file.write(str(i[1])+str(' ')+str(i[0])+str(' ')+str(distances[i[0]][i[1]])+'\n')
			drawGraph(GG,'coral','GabrielGraph')
			break

def callRNG():
	print("Generating RNG")
	while True:
		RelativeNeighborhoodGraph()
		if nx.is_connected(RNG):
			file = open('Model_RNG_edges.txt', 'w')
			for i in RNG.edges():
				file.write(str(i[0])+str(' ')+str(i[1])+str(' ')+str(distances[i[0]][i[1]])+'\n')
				file.write(str(i[1])+str(' ')+str(i[0])+str(' ')+str(distances[i[0]][i[1]])+'\n')
			drawGraph(RNG,'green','RelativeNeighborhoodGraph')
			break
		
def callKNNG():
	print("Generating KNNG")
	KNearestNeighborGraph()
	if nx.is_connected(KNNG):
		file = open('Model_KNNG_edges.txt', 'w')
		for i in KNNG.edges():
			file.write(str(i[0])+str(' ')+str(i[1])+str(' ')+str(distances[i[0]][i[1]])+'\n')
			file.write(str(i[1])+str(' ')+str(i[0])+str(' ')+str(distances[i[0]][i[1]])+'\n')		
		drawGraph(KNNG,'red','KNearestNeighborGraph')
	else:
		print("KNNG is not connected")
		sys.exit()
		
def callSBAG():
	print("Generating SBAG")
	while True:	
		SpatialBarabasiAlbertGraph()
		if nx.is_connected(SBAG):
			file = open('Model_SBAG_edges.txt', 'w')
			for i in SBAG.edges():
				file.write(str(i[0])+str(' ')+str(i[1])+str(' ')+str(distances[i[0]][i[1]])+'\n')
				file.write(str(i[1])+str(' ')+str(i[0])+str(' ')+str(distances[i[0]][i[1]])+'\n')			
			drawGraph(SBAG,'purple','SpatialBarabasiAlbertGraph')
			break

Coordinates()

nodes=RGG.nodes()
for i in nodes:
	labels[i]=i
#nodes distances
distances = [[0 for i in nodes] for i in nodes]
for i in nodes:
	for j in nodes:
		n1=coordinates[i]
		x1=n1[0]
		y1=n1[1]
		n2=coordinates[j]
		x2=n2[0]
		y2=n2[1]
		d=math.sqrt(((x2-x1)*(x2-x1))+((y2-y1)*(y2-y1)))
		distances[i][j]=d
		
callRGG()
callRNG()
callGG()
callKNNG()
callWG()
callSBAG()


print("RGG",nx.number_of_edges(RGG))
print('GG',nx.number_of_edges(GG))
print('RNG',nx.number_of_edges(RNG))
print('KNNG',nx.number_of_edges(KNNG))
print('WG',nx.number_of_edges(WG))
print('SBAG',nx.number_of_edges(SBAG))

		

