#!/bin/bash
export GUROBI_HOME="/root/gurobi702/linux64" 
export PATH="${PATH}:${GUROBI_HOME}/bin"
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${GUROBI_HOME}/lib"
rm "FMAX.txt"
rm "WA.txt"
rm "CAPEX.txt"
rm "all_optical_nodes_cost.txt"
rm "all_links_cost.txt"
N=100
#echo "1_Generate Models"
#python 1_Generate_Models.py n
C=1000
while [ $C -le 1000 ]
do
	I=0
	while [ $I -lt 1 ]
	do
		echo "################################ Number of connections $C, iteration $I ###########################################"
		echo "2_Generate Connections"
		python "2_Generate_Connections.py" $N $C
		echo "3_Routing_Algorithm"
		/bin/bash gurobi.sh "3_Routing_Algorithm.py"
		echo "4_Wavelength_Assignment"
		python "4_Wavelength_Assignment.py"
		I=$[ $I + 1 ]
	done
	echo "5_Network_Cost"
	python "5_Network_Cost.py"
	C=$[ $C + 100 ]
done
