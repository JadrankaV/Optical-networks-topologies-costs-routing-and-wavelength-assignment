::DEL "FMAX.txt"
::DEL "WA.txt"
DEL "CAPEX.txt"
DEL "all_optical_nodes_cost.txt"
DEL "all_links_cost.txt"
SET /A n=100
::echo "1_Generate Models"
::call python 1_Generate_Models.py %n%
FOR %%c IN (100 200 300 400 500) DO (
::FOR /L %%i IN (1,1,10) DO (
::echo "################################ Number of connections %%c, iteration %%i ###########################################"
echo "2_Generate Connections"
call python 2_Generate_Connections.py %n% %%c
::echo "3_Routing_Algorithm"
::call gurobi.bat "3_Routing_Algorithm.py"
::echo "4_Wavelength_Assignment"
::call python 4_Wavelength_Assignment.py
::)
echo "5_Network_Cost"
call python 5_Network_Cost.py
)