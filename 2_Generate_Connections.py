#connection request generator
import random
import sys

#num_CR=50
num_CR=int(sys.argv[2])
nodes_number=int(sys.argv[1])
i=0
file = open('Connection_request.txt', 'w')
random.seed()
connections=[]
while i<num_CR:
	first=i % nodes_number
	second=random.randint(0,nodes_number-1)
	
	if first!=second and (first,second) not in connections:
		connections.append((first,second))
		file.write(str(first)+str(' ')+str(second)+'\n')
		i=i+1
	