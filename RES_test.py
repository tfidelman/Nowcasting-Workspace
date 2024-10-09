"""
Tomer Fidelman
Ocober 2024

A short file to examine the RESDFM.pickle file.

"""
#%% Import Packages

import pickle
import pandas as pd
import numpy as np

#%% Load the RESDFM.pickle file

with open('ResDFM.pickle', 'rb') as handle:
    Res = pickle.load(handle)

Res_df = pd.DataFrame(Res)
# %%
Res_df