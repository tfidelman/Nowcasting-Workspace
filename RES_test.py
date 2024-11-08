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

with open('ResDFM_4Factor.pickle', 'rb') as handle:
    Res0 = pickle.load(handle)

Res_df = pd.DataFrame(Res0)

with open('ResDFM.pickle', 'rb') as handle:
    Res = pickle.load(handle)

#%%
Res5F_df = pd.DataFrame(Res)
Res5F_df['Res']['C'].shape
Res5F_df
#%%
Res_df['Res']['C'].shape
#%%
Res_df['Res']['p']
Res_df['Res']['loglik']
Res5F_df['Res']['p']
Res5F_df['Res']['loglik']
#%%
for key in Res5F_df['Res'].index:
    if Res_df['Res'][key].shape == Res5F_df['Res'][key].shape:
        print("Same shape")
    else:
        print(f"{key} has Different shape")

"""

Z has Different shape, expectations, use 5f full sample
C has Different shape, obvservation matrix; changed 20-24
A has Different shape, transition matrix; changed 20-24
Q has Different shape, covariance matrix of trans eqns, changed 20-24
Z_0 has Different shape, initial value of states, replaced 20-24
V_0 has Different shape, initial value of state transition matrix; changed 20-24

r has Different shape, just the number of blocks, can be change trivially

p and loglik are irreleant to the gdp nowcast
"""

#%% Combine the COVID ResDFM with the 4Factor

with open('ResDFM_jC.pickle', 'rb') as handle:
    Res1 = pickle.load(handle)

ResCOVID_df = pd.DataFrame(Res1)
#%%

keylist = ResCOVID_df['Res'].keys()
# drop last two
keylist = keylist[:-2]
keylist
#%%

for k in keylist:
    if isinstance(k, int):
        continue  # Skip integer keys
    print(f"Key: {k}, Shape: {ResCOVID_df['Res'][k].shape}")

for k in keylist:
    if isinstance(k, int):
        continue  # Skip integer keys
    print(f"Key: {k}, Shape: {Res_df['Res'][k].shape}")

#%%
for k in keylist:
    if isinstance(k, int):
        continue  # Skip integer keys
    print(f"Key: {k}, Shape: {Res5F_df['Res'][k].shape}")
# %% store Z, C, A, Q, Z_0, V_0 as dfs and then to csvs in params folder

keylist = keylist[:-1]

for k in keylist:
    if isinstance(k, int):
        continue  # Skip integer keys
    df = ResCOVID_df['Res'][k]
    
    # Check if df is a numpy.ndarray and convert it to a DataFrame or Series
    if isinstance(df, np.ndarray):
        df = pd.DataFrame(df)  # Convert to DataFrame if it's an ndarray
    df.to_csv(f"params/{k}COVID.csv")

# Second loop for saving '4F' params
for k in keylist:
    if isinstance(k, int):
        continue  # Skip integer keys
    df = Res_df['Res'][k]
    
    # Check if df is a numpy.ndarray and convert it to a DataFrame or Series
    if isinstance(df, np.ndarray):
        df = pd.DataFrame(df)  # Convert to DataFrame if it's an ndarray
    df.to_csv(f"params/{k}4F.csv")

for k in keylist:
    if isinstance(k, int):
        continue
    df = Res5F_df['Res'][k]

    if isinstance(df, np.ndarray):
        df = pd.DataFrame(df)
    df.to_csv(f"params/{k}5F.csv")


#%% Rewrite FULL4F to include the COVID factor

#%% find the values of x_sm and X_sm to replace with COVID values 
#%% OK, now 

#%%
Z_05F = Res5F_df['Res']['Z_0']
# to csv
Z_05F = pd.DataFrame(Z_05F)
Z_05F.to_csv("params/Z_05F.csv")

#%%
V_05F = Res5F_df['Res']['V_0']
# to csv
V_05F = pd.DataFrame(V_05F)
V_05F.to_csv("params/V_05F.csv")

V4F = Res_df['Res']['V_0']
# to csv
V4F = pd.DataFrame(V4F)
V4F.to_csv("params/V4F.csv")

V_covid = ResCOVID_df['Res']['V_0']
# to csv
V_covid = pd.DataFrame(V_covid)
V_covid.to_csv("params/V_covid.csv")

######################################################################
######### Putting it all together          ###########################
######################################################################
#%%
ResFINAL_df = Res_df.copy()
ResFINAL_df['Res']['r'] = np.append(ResFINAL_df['Res']['r'], 1)

#%% set ResFINAL_df['Res']['A'] to 0
ResFINAL_df['Res']['A'] = np.zeros((66, 66))

ResFINAL_df['Res']['C'] = np.zeros((29, 66))

ResFINAL_df['Res']['Q'] = np.zeros((66, 66))

ResFINAL_df['Res']['Z_0'] = np.zeros((66, 1))

ResFINAL_df['Res']['V_0'] = np.zeros((66, 66))

ResFINAL_df['Res']['Z'] = np.zeros((474, 66))


#%%
"""
Z has Different shape, expectations, use 5f full sample (474 x 66)
C has Different shape, obvservation matrix; changed 20-24 (29 x 66) 
A has Different shape, transition matrix; changed 20-24 (66 x 66)
Q has Different shape, covariance matrix of trans eqns, changed 20-24 (66 x 66)
Z_0 has Different shape, initial value of states, replaced 20-24, (66 x 1)
V_0 has Different shape, initial value of state transition matrix; changed 20-24 (66 x 66)
"""
Z_new = pd.read_csv("params/Z_Final_Matrix.csv")
C_new = pd.read_csv("params/C_Final.csv")
A_new = pd.read_csv("params/A_Final.csv")
Q_new = pd.read_csv("params/Q_Final.csv")
Z0_new = pd.read_csv("params/Z0_Final.csv")
V0_new = pd.read_csv("params/V_Final.csv")
#%% drop first column for all and then convert to numpy array
Z_new = Z_new.drop(columns=Z_new.columns[0]).to_numpy()
C_new = C_new.drop(columns=C_new.columns[0]).to_numpy()
A_new = A_new.drop(columns=A_new.columns[0]).to_numpy()
Q_new = Q_new.drop(columns=Q_new.columns[0]).to_numpy()
Z0_new = Z0_new.drop(columns=Z0_new.columns[0]).to_numpy()
V0_new = V0_new.drop(columns=V0_new.columns[0]).to_numpy()
#%%
# overwrite the old arrays
ResFINAL_df['Res']['C'] = C_new
ResFINAL_df['Res']['A'] = A_new
ResFINAL_df['Res']['Q'] = Q_new
ResFINAL_df['Res']['Z_0'] = Z0_new
ResFINAL_df['Res']['V_0'] = V0_new
ResFINAL_df['Res']['Z'] = Z_new
#%%
for k in keylist:
    if isinstance(k, int):
        continue  # Skip integer keys
    print(f"Key: {k}, Shape: {ResFINAL_df['Res'][k].shape}")

#%% save as pickle

with open('ResFINAL.pickle', 'wb') as handle:
    pickle.dump(ResFINAL_df, handle, protocol=pickle.HIGHEST_PROTOCOL)

