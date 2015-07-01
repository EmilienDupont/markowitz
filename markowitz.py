#!/usr/bin/env python

from gurobipy import *
from pylab import *


###### Input received
Data = [[0.02778, 0.00387, 0.00021],
    [0.00387, 0.01112, -0.00020],
    [0.00021, -0.00020, 0.00115]]
######

def optimize(Data):
    print "in markowitz!"
    m = Model()
    
    D = np.array(Data)
    
    n = D.shape[1] # number of stocks
    N = D.shape[0] # number of days traded
    
    print 'Number of stocks %d' % n
    print 'Number of days %d' % N
    
    # Mean return for each stock
    e = np.ones(N)
    r = np.dot(D.T,e)/N
    
    print r
    
    # Covariance matrix
    Dbar = (D - np.outer(e,r))/(math.sqrt(N-1))
    Sigma = dot(Dbar.T, Dbar)
    
    print Sigma
    
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
    k = 0
    
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
    
    return solution

    ''' Uncomment to plot
    plot(stdDev, solution)
    
    xlabel('risk')
    ylabel('return')
    title('Markowitz portfolio optimization')
    grid(True)
    show()
    '''


