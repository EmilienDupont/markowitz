#!/usr/bin/env python

from gurobipy import *
from pylab import *

# Create Model
m = Model()

# Data for problem (MOSEK example data to debug)
pBar = [0.1073, 0.0737, 0.0627]
Sigma = [[0.02778, 0.00387, 0.00021],
    [0.00387, 0.01112, -0.00020],
    [0.00021, -0.00020, 0.00115]]
maxStdDev = [0.035, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09]
n = len(pBar)

# Add variables
x = {};
for i in range(n):
    x[i] = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name = 'x' + str(i))

m.update()

# Add constraints
# 1.x = 1
m.addConstr(quicksum(x[i] for i in range(n)) == 1)

# Variance constraint (use symmetry here to make calculation faster)
variance = 0
for i in range(n):
    for j in range(n):
        variance += x[i]*Sigma[i][j]*x[j]

# Set objective
m.setObjective(quicksum(pBar[i]*x[i] for i in range(n)), GRB.MAXIMIZE)

solution = [];
k = len(maxStdDev)

for i in range(k):
    
    m.addConstr(variance <= maxStdDev[k-1-i]*maxStdDev[k-1-i])

    m.update()

    m.optimize()
    
    solution.insert(0, m.ObjVal)

print solution

print maxStdDev

plot(maxStdDev, solution)

xlabel('risk')
ylabel('return')
title('Markowitz portfolio optimization')
grid(True)
show()



