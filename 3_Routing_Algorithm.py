from gurobipy import *
from sys import getsizeof
from itertools import repeat
import re
import random
import math
from operator import itemgetter


init=0
Fmax_models=[]
models_names=['RGG','GG','RNG','KNNG','WG','SBAG'] 
models_edges=['Model_RGG_edges.txt','Model_GG_edges.txt','Model_RNG_edges.txt','Model_KNNG_edges.txt','Model_WG_edges.txt','Model_SBAG_edges.txt'] 


for mod in models_edges:
	print(mod)
	# Create optimization model
	m = Model('netflow')

	#Read network arcs from file
	with open(mod, "r") as ins:
		arcs = []
		for line in list(ins):
			numbers =  line.split()
			if line != '\n':
				first = numbers[0]
				second= numbers[1]
				arcs1=(int(first),int(second))
				arcs.append(arcs1)


	arcs = tuplelist(arcs)				
	nodes_number=(max(arcs,key=itemgetter(0))[0])+1

	#network nodes
	nodes = []
	i=0
	while i <nodes_number:
		nodes.append(i)
		i=i+1
		
	#network connection request
	with open("Connection_request.txt", "r") as ins:
		connection_request=[]
		i=0
		for line in list(ins):
			numbers =  line.split()
			if line != '\n':
				first = numbers[0]
				second= numbers[1]
				arcs1=(i,int(first),int(second))
				#print(arcs1)
				connection_request.append(arcs1)
				i=i+1
	'''
	i=0
	connection_request= {(1, 12),(17, 30),(10, 15),(14, 8),(23, 32),(1,7),(6, 4),(13, 18),(16, 24),(3, 28) }

	while i<10:
		first=random.uniform(1,nodes_number)
		second=random.uniform(1,nodes_number)
		if first!=second:
			o=(int(first),int(second))
			i=i+1
			connection_request.append(o)'''

	connection_request = tuplelist(connection_request)
	#print connection_request

	# Create lambda
	lambda1= {}
	connection_request_size= len(connection_request) 
	t=0
	for i in nodes:
		for j in nodes:
			lambda1[i,j]=0
			
	for i in nodes:
		for j in nodes:
			for c,s,d in connection_request:
				if i==s and j==d:
					lambda1[i,j] = 1
				
	



	#add variable FSD
	FSD={}
	for c,s,d in connection_request:
		for i,j in arcs:
			FSD[i,j,s,d] = m.addVar(vtype=GRB.BINARY,name='FSD_%s_%s_%s' % (i, j, c))
		


	#add variable FMAX
	FMAX=m.addVar(vtype=GRB.INTEGER,name='FMAX')	
		
			
	#Update variables
	m.update()	


	#Flow conservation constraints
	for c,s,d in connection_request:
		#c=csd[0]
		#s=csd[1]
		#d=csd[2]
		for j in nodes:
			if s==j:
				m.addConstr(quicksum(FSD[i,j,s,d] for i,j in arcs.select('*',j)) - quicksum(FSD[j,k,s,d] for j,k in arcs.select(j,'*'))== (-1*lambda1[s,d]),'node_%s_%s_%s' % (s,d, j))
			elif d==j:
				m.addConstr(quicksum(FSD[i,j,s,d] for i,j in arcs.select('*',j)) - quicksum(FSD[j,k,s,d] for j,k in arcs.select(j,'*')) == (lambda1[s,d]),'node_%s_%s_%s' % (s,d, j))
			else:
				m.addConstr(quicksum(FSD[i,j,s,d] for i,j in arcs.select('*',j)) - quicksum(FSD[j,k,s,d] for j,k in arcs.select(j,'*')) == 0,'node_%s_%s_%s' % (s,d, j))

				
	#SUM
	for i,j in arcs:
		m.addConstr( FMAX >=(quicksum(FSD[i,j,s,d] for c,s,d in connection_request)+quicksum(FSD[j,i,s,d] for c,s,d in connection_request)),'FMAX1_%s_%s_%s_%s' % (i, j,s,d))
		

	m.setObjective(FMAX, GRB.MINIMIZE)
	m.optimize()



	#Print variables 
	print "Variables"
	for var in m.getVars():
		if var.varName=='FMAX':
			Fmax_models.append(int(var.x))
			

	#CR Path	
	path=[[] for i in repeat(None, connection_request_size)]
	vars=m.getVars()
	del vars[-1]
	for var in vars:
		name=var.varName
		var_name=name.split('_')
		i=int(var_name[1])
		j=int(var_name[2])
		c=int(var_name[3])
		if var.x!=0:
			path[c].append((i,j))




	#Save nodes(lightpath) in nodes.txt
	nodes_file_name='WA_'+str(models_names[init])+'_nodes.txt'
	file = open(nodes_file_name, 'w')
	node1=0
	for n in path:
		file.write(str(node1) + '\n')
		node1=node1+1

	#Save paths
	links= []
	indicator=0
	currentNode=0
	j=0
	for p1 in path:
		j=0
		for p2 in path:
			if(currentNode==j):
				j=j+1
			else:
				for element1 in p1:
					for element2 in p2:
						if(element1[0]==element2[0] and element1[1]==element2[1]) or (element1[1]==element2[0] and element1[0]==element2[1]):
							o=(int(currentNode+1),int(j+1))
							links.append(o)
							indicator=indicator+1
				j=j+1
		currentNode=currentNode+1

	#Save links(edge between two vertices in graph if the corresponding lightpaths pass through a common physical fiber link) in arcs.txt
	x = list(set(links))
	arcs_file_name='WA_'+str(models_names[init])+'_arcs.txt'
	file1 = open(arcs_file_name, 'w')
	for element in x:
		file1.write(str(element[0])+str(' ')+str(element[1])+'\n')
		
	init=init+1


file = open('Fmax.txt', 'a')
j=0
for i in models_names:
	file.write(str(Fmax_models[j])+' ')
	j=j+1
file.write('\n')
