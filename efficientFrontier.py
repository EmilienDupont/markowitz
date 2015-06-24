#!/usr/bin/env python

# gives a curve which depends on how much you weigh risk.
# If you really want to have a comparatively low risk => high alpha

import math
import numpy as np
from gurobipy import *
from pylab import *

# Create Model
m = Model()

# Data for problem (MOSEK example data to debug)
pBar = [0.1073, 0.0737, 0.0627]
Sigma = np.array([[0.02778, 0.00387, 0.00021],
                    [0.00387, 0.01112, -0.00020],
                    [0.00021, -0.00020, 0.00115]])

# note that this might not be square (so would need to change this after)
#L = np.linalg.cholesky(Sigma)
L = math.sqrt(0.1)*np.array([[0.5271, 0.0734, 0.0040], [0, 0.3253, -0.0070], [0, 0, 0.1069]]).T
n = L.shape[1]
k = L.shape[0]

alpha = [0, 0.01, 0.1, 0.25, 0.30, 0.35, 0.4, 0.45, 0.50, 0.75, 1, 1.5, 2, 3, 10]
p = len(alpha)

#print Lto check
print np.dot(L, L.T)
print Sigma

# Add variables
x = {};
for i in range(n):
    x[i] = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name = 'x' + str(i))

t = m.addVar(lb=0, vtype=GRB.CONTINUOUS, name = 't')

m.update()

# Add constraints
m.addConstr(quicksum(x[i] for i in range(n)) == 1)

# y = Lx (L might not be square)
y = {};
for i in range(k):
    y[i] = quicksum(L[i,j]*x[j] for j in range(n))

# y'*y <= t^2
m.addConstr(quicksum(y[i]*y[i] for i in range(k)) <= t*t)

# Return and risk
ret = []
risk = []

# Set objective
for j in range(p): #(change to p)
    m.setObjective(quicksum(pBar[i]*x[i] for i in range(n)) - alpha[j]*t, GRB.MAXIMIZE)

    m.update()
    
    m.optimize()
    
    v = m.getVars()
    
    ret.append(sum(pBar[i]*v[i].x for i in range(n)))
    
    risk.append(v[n].x)

for i in range(p):
    print 'alpha: {0:.2f} , return {1:.5f} , risk {2:.5f} '.format(alpha[i], ret[i], risk[i])

if (False):
    scatter(risk, ret)
        
    xlabel('risk')
    ylabel('return')
    title('Efficient Frontier')
    grid(True)
show()