#!/usr/bin/env python

from gurobipy import *

def optimize(r, Sigma, maxRisk):
    print "in markowitz!"
    m = Model()
    
    n = len(Sigma) # number of stocks
    
    print 'Number of stocks %d' % n
    
    print r
    
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
    
    solution = {'Stocks': [], 'Return': []}

    m.addConstr(variance <= maxRisk*maxRisk)
    
    m.update()
    
    m.optimize()

    stocks = []
    
    # Check if model is infeasible or unbounded (or numerical trouble)
    if (m.status == 3 or m.status == 4 or m.status == 12):
        sol = 0
        stocks = [0] * n # Send list of zeros if infeasible
    else:
        sol = m.ObjVal
        for v in m.getVars():
            stocks.append(v.x)
    
    solution['Return'] = sol
    
    solution['Stocks'] = stocks

    print solution
    
    return solution