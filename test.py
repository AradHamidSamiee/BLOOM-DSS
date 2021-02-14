from flask import Flask, render_template, request
import sqlite3
from datetime import datetime, date

from el3 import electre_iii
from topsis import topsis_method
from fuzzy_topsis import fuzzy_topsis_method
from vikor import vikor_method
from fuzzy_vikor import fuzzy_vikor_method

import numpy as np

# ---------- electre_iii ----------
# # Parameters
Q = [0.30, 0.30, 0.30, 0.30]
P = [0.50, 0.50, 0.50, 0.50]
V = [0.70, 0.70, 0.70, 0.70]
W = [9.00, 8.24, 5.98, 8.48]

# Dataset
dataset = np.array([
    [8.84, 8.79, 6.43, 6.95],   #a1
    [8.57, 8.51, 5.47, 6.91],   #a2
    [7.76, 7.75, 5.34, 8.76],   #a3
    [7.97, 9.12, 5.93, 8.09],   #a4
    [9.03, 8.97, 8.19, 8.10],   #a5
    [7.41, 7.87, 6.77, 7.23]    #a6
])

rank_D = electre_iii(dataset, P, Q, V, W, graph = True)[2]

# # Rank - Descending
# for i in range(0, len(rank_D)):
#     print(str(i+1), rank_D[i])

# ---------- topsis ----------
# # Weights
# weights = np.array([ [0.1, 0.4, 0.3, 0.2] ])

# # Load Criterion Type: 'max' or 'min'
# criterion_type = ['max', 'max', 'max', 'min']

# # Dataset
# dataset = np.array([
#                 [7, 9, 9, 8],   #a1
#                 [8, 7, 8, 7],   #a2
#                 [9, 6, 8, 9],   #a3
#                 [6, 7, 8, 6]    #a4
#                 ])
# relative_closeness = topsis_method(dataset, weights, criterion_type, graph = False)
# print(relative_closeness)

# ---------- fuzzy topsis ----------

# ---------- VIKOR ----------

# ---------- fuzzy vikor ----------

