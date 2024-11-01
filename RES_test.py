"""
Tomer Fidelman
Ocober 2024

A short file to examine the RESDFM.pickle file.

"""
#%% Import Packages

import pickle
import pandas as pd
import numpy as np

#%% test

N = 5
nQ = 2

i_idio = np.append(np.ones(N-nQ), np.zeros(nQ)).reshape((-1, 1), order="F") == 1
print(i_idio)

#%% Load the RESDFM.pickle file

with open('ResDFM.pickle', 'rb') as handle:
    Res = pickle.load(handle)

Res_df = pd.DataFrame(Res)
# %%
Res_df
# %% print Res value for index Q
print(Res['Res']['Q'])
# save it to csv
#%%
Q_inspect = Res['Res']['Q']
Q_inspect_csv = pd.DataFrame(Q_inspect)
Q_inspect_csv.to_csv('Q_inspect.csv')
#%% how many columns are zero
print(np.count_nonzero(Q_inspect))
# %% how many rows are zero
print(np.count_nonzero(Q_inspect, axis=0))
#%% hadamard division
Q_inspect.shape
# create 61 by 61 matrix of random values
random_matrix = np.random.rand(61, 61)

print(random_matrix)

QdivRand = Q_inspect / random_matrix 


# %%
QdivRand