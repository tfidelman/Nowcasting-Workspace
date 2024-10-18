#-------------------------------------------------Libraries
#%%
from Functions.load_data import load_data
from Functions.load_spec import load_spec
from Functions.update_Nowcast import update_nowcast
import os
import pickle


#-------------------------------------------------User Inputs
series = 'GDPC1'  # Nowcasting real GDP (GDPC1) <fred.stlouisfed.org/series/GDPC1>
period = '2024q3' # Forecasting target quarter


#-------------------------------------------------Load model specification and first vintage of data.
Spec   = load_spec('Spec_US_update.xls')


#-------------------------------------------------Load DFM estimation results structure `Res`
with open('ResDFM.pickle', 'rb') as handle:
    Res = pickle.load(handle)


#-------------------------------------------------Update nowcast and decompose nowcast changes into news.
# Nowcast update from week of December 7 to week of December 16, 2016
vintage_old  = '2024-10-09'
vintage_new  = '2024-10-16'
datafile_old = os.path.join('data','US',vintage_old + '.xlsx')
datafile_new = os.path.join('data','US',vintage_new + '.xlsx')

# Load datasets for each vintage
X_old,_,_    = load_data(datafile_old,Spec)
X_new,Time,_ = load_data(datafile_new,Spec)

Res = Res['Res']

update_nowcast(X_old,X_new,Time,Spec,Res,series,period,vintage_old,vintage_new)

#%%
"""
With params run up until July 1 2024 we have real GDP growth estimate of 2.35% for Q3 (annualized)

Without COVID adjustment and with variables from MK Github, not NY Fed papers. 

"""