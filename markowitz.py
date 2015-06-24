#!/usr/bin/env python

from gurobipy import *
from pylab import *


###### Input received
A = [[0.02778, 0.00387, 0.00021],
    [0.00387, 0.01112, -0.00020],
    [0.00021, -0.00020, 0.00115]]
######

m = Model()

A = np.array(A)

n = A.shape[1] # number of stocks
N = A.shape[0] # number of days traded

# Mean return for each stock
e = np.ones(N)
r = np.dot(A.T,e)

# Covariance matrix
Abar = (A - np.outer(e,r))/(math.sqrt(N-1))
Sigma = dot(Abar.T, Abar)

# Add variables (one for each stock)
x = {};
for i in range(n):
    x[i] = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name = 'x' + str(i))

m.update()

# Add constraints
m.addConstr(quicksum(x[i] for i in range(n)) == 1)

variance = 0
for i in range(n):
    for j in range(n):
        variance += x[i]*Sigma[i][j]*x[j]

# Set objective
m.setObjective(quicksum(r[i]*x[i] for i in range(n)), GRB.MAXIMIZE)

solution = []
stdDev = []
k = 20

# Compute solution for k different points
for i in range(k):
    stdDev.insert(0, 0.03 + 0.005*(k-i))
    
    m.addConstr(variance <= stdDev[0]*stdDev[0])

    m.update()

    m.optimize()
    
    # Check if model is infeasible or unbounded
    if (m.status == 3 or m.status == 4):
        sol = 0
    else:
        sol = m.ObjVal
    
    solution.insert(0, sol)

print solution

plot(stdDev, solution)

xlabel('risk')
ylabel('return')
title('Markowitz portfolio optimization')
grid(True)
show()



