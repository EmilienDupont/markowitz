# markowitz.py
# For now we MOSEK example data to debug
from gurobipy import *

import numpy as np

# Data for problem
pbar = np.array([ 0.1073, 0.0737, 0.0627])
S = np.array([0.2778, 0.0387, 0.0021],
              [0.0387, 0.1112, -0.0020],
              [0.0021, -0.0020, 0.0115])

