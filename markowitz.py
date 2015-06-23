#!/usr/bin/env python

from gurobipy import *

# Create Model
m = Model()

# Data for problem (MOSEK example data to debug)
pBar = [0.1073, 0.0737, 0.0627]
Sigma = [[0.02778, 0.00387, 0.00021],
    [0.00387, 0.01112, -0.00020],
    [0.00021, -0.00020, 0.00115]]
maxStdDev = 0.035
n = 3

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

m.addConstr(variance <= maxStdDev*maxStdDev)

m.update()

# Set objective
m.setObjective(quicksum(pBar[i]*x[i] for i in range(n)), GRB.MAXIMIZE)

m.optimize()

