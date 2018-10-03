from pulp import *
import random
import time
#Problem Definition
prob=pulp.LpProblem("POC-problem",pulp.LpMinimize)#Problem definition- Title and type( Minimize or Maximize)
#supply points and the quantities available
s={1:900,2:400,3:800} 
#demand points and the quantities demanded
d={4:100,5:300,6:900,7:450,8:200} 
Tc=100# Truck Capacity- We assume that all trucks have the same capacity
Ta=700 # Total Time available for all the trucks combined
# A dictionary containing the price per unit mass of the products.
P_unit={1:2,2:2.2,3:1.9}  
distance={1: {8: 127, 4: 152, 5: 268, 6: 94, 7: 273}, 2: {8: 83, 4: 345, 5: 92, 6: 94, 7: 322}, 3: {8: 230, 4: 101, 5: 230, 6: 140, 7: 283}}
# Initializing the distance between the supply and demand points
cost={} # Initializing the cost to traverse the distance between the supply and demand points
Time={} # Initializing the Time taken to traverse the distance between the supply and demand points
for i in s.keys():
    cost[i]={}
    Time[i]={}
    #distance[i]={}
    for j in d.keys():
     #   distance[i][j]=int(random.uniform(70,400)) # A random distance is assigned for every supply point and demand point pair.
        cost[i][j]=round(2*0.4*distance[i][j]+P_unit[i]*Tc,1) # Cost includes cost of procuring and transportation costs.
        #0.4 is the cost of transporting a product per unit distance 
        Time[i][j]=distance[i][j]/60 # Assuming speed to be 60 units for all the trucks, Time is calculated
print "The distance between every supply and demand point pair is", distance
print "The cost of traversing the distance is", cost
print "The Time taken in travelling is", Time 

#Objective function
routes=[[a,b] for a in s.keys() for b in d.keys()] # all possible routes listed here

#Problem formulation
x=pulp.LpVariable.dicts('',(s.keys(),d.keys()),lowBound=0,cat=pulp.LpInteger)# Decision Variables used to denote the number of trips made
#objective Function
prob+= sum([x[r][t]*cost[r][t] for [r,t] in routes])
# Supply Constraints
for i in s.keys():
    prob+=sum([x[i][j]*Tc for j in d.keys()])<=s[i],i
#demand constraints
for j in d.keys():
    prob+=sum([x[i][j]*Tc for i in s.keys()])>=d[j],j
#Time constraint
prob+=sum([x[i][j]*Time[i][j] for i in s.keys() for j in d.keys()])<=Ta/2
solution= prob.solve()#Command to solve the ILP
print("Status:", LpStatus[prob.status])# Solution Status
k={}
for v in prob.variables():# Each of the variables is printed with it optimum value
    k[v.name[1:]]=v.varValue
#code to extract only the used paths
output={}
for i in k.keys():
    if k[i]!=0:
        output[i]=k[i]
print("Optimal cost =",value(prob.objective)) # The optimised objective function value is printed on the screen

print output

#sensitivity
sub_output=input("enter the trip sequences you prefer: ")
#sub_output={'2_8': 1.0, '3_4': 1.0, '3_7': 5.0, '3_6': 1.0, '2_5': 2.0,'3_5':1.0,'1_6': 8.0, '1_8': 1.0}

def sensitivity(sub_optimal_output,optimal_solution):
  sub_cost=0
  for k in  sub_optimal_output.keys():
        sub_cost+=cost[int(k[0])][int(k[2])]*sub_optimal_output[k]
  print "The new cost is ", sub_cost  
  return sub_cost-optimal_solution 

change=sensitivity(sub_output,value(prob.objective)) 
print "The increase in cost from optimal is:" , change     

    


        
        
        



