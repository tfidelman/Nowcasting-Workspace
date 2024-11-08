"""
Before running this, pull_data.py must be run for the current date.

"""

# %%

from Functions.load_data import load_data
from Functions.load_spec import load_spec
from Functions.update_Nowcast import update_nowcast
import os
import pickle
import datetime
import pandas as pd

#%%

from Functions.load_data import load_data
from Functions.load_spec import load_spec
from Functions.update_Nowcast import update_nowcast
import os
import pickle
import datetime
import pandas as pd

#%% Load Historical CSVs for 
# cumulative 1) data/20241107_nowcast.csv
# incremental 2) data/20241107_nowcast_inc.csv

# Load data
df_cml = pd.read_csv('data/20241107_nowcast.csv', index_col=0, parse_dates=True)
df_inc = pd.read_csv('data/20241107_nowcast_incrmt.csv', index_col=0, parse_dates=True)

#%% Run Update
#%%
#-------------------------------------------------User Inputs
series = 'GDPC1'  # Nowcasting real GDP (GDPC1) <fred.stlouisfed.org/series/GDPC1>
period = '2024q4' # Forecasting target quarter

#-------------------------------------------------Load model specification and first vintage of data.
Spec   = load_spec('Spec_US_update_COVID.xls')

#-------------------------------------------------Load DFM estimation results structure `Res`
with open('ResFINAL.pickle', 'rb') as handle:
    Res = pickle.load(handle)

#-------------------------------------------------Update nowcast and decompose nowcast changes into news.
vintage_old  = '2024-10-31'
vintage_today = '2024-11-08'
vintage_new = vintage_today
datafile_old = os.path.join('data','US',vintage_old + '.xlsx')
datafile_new = os.path.join('data','US',vintage_new + '.xlsx')

# Load datasets for each vintage
X_old,_,_    = load_data(datafile_old,Spec)
X_new,Time,_ = load_data(datafile_new,Spec)


Res = Res['Res']

old_gdp_inc, new_gdp_inc, impact_inc, impact_rev_inc = update_nowcast(X_old,X_new,Time,Spec,Res,series,period,vintage_old,vintage_new)

#%%
## Cumulative

#-------------------------------------------------User Inputs
series = 'GDPC1'  # Nowcasting real GDP (GDPC1) <fred.stlouisfed.org/series/GDPC1>
period = '2024q4' # Forecasting target quarter

#-------------------------------------------------Load model specification and first vintage of data.
Spec   = load_spec('Spec_US_update_COVID.xls')

#-------------------------------------------------Load DFM estimation results structure `Res`
with open('ResFINAL.pickle', 'rb') as handle:
    Res = pickle.load(handle)

#-------------------------------------------------Update nowcast and decompose nowcast changes into news.
vintage_old  = '2024-10-02'
vintage_today = '2024-11-08'
vintage_new = vintage_today
datafile_old = os.path.join('data','US',vintage_old + '.xlsx')
datafile_new = os.path.join('data','US',vintage_new + '.xlsx')

# Load datasets for each vintage
X_old,_,_    = load_data(datafile_old,Spec)
X_new,Time,_ = load_data(datafile_new,Spec)

Res = Res['Res']

old_gdp_cm, new_gdp_cm, impact_cm, impact_rev_cm = update_nowcast(X_old,X_new,Time,Spec,Res,series,period,vintage_old,vintage_new)
#%% Adding new line to DF

# incremental

dt = [vintage_new]
gdp_estimates = [new_gdp_inc]
gdp_impact = [impact_inc]
gdp_rev = [impact_rev_inc]

spec_df = pd.read_excel('Spec_US_update_COVID.xls')
var_cols = spec_df['Category'] + '-'+ spec_df['SeriesID']

# make dt rows of df and gdp_estimates and gdp_impact columns
df_plot_inc = pd.DataFrame({'Date':dt, 'GDP Estimate':gdp_estimates, 'Revision':gdp_rev})
df_plot_inc = df_plot_inc.set_index('Date')

# add seriws_cols to df_plot
for i in range(len(var_cols)):
    df_plot_inc[var_cols[i]] = [0]*len(dt)

# fill each var_cols with Impact for the specific date-time
for i in range(len(dt)):
    df_plot_inc.loc[dt[i],var_cols] = gdp_impact[i]

#replace nan with 0
df_plot_inc = df_plot_inc.fillna(0)

df_plot_inc['Labor'] = df_plot_inc.filter(like='Labor').sum(axis=1)
df_plot_inc['NatAccts'] = df_plot_inc.filter(like='National Accounts').sum(axis=1)
df_plot_inc['Prices'] = df_plot_inc.filter(like='Prices').sum(axis=1)
df_plot_inc['Surveys'] = df_plot_inc.filter(like='Surveys').sum(axis=1)
df_plot_inc['Manuf'] = df_plot_inc.filter(like='Manufacturing').sum(axis=1)
df_plot_inc['Housing'] = df_plot_inc.filter(like='Housing and Construction').sum(axis=1)
df_plot_inc['IntlTrade'] = df_plot_inc.filter(like='International Trade').sum(axis=1)
df_plot_inc['Retail'] = df_plot_inc.filter(like='Retail and Consumption').sum(axis=1)

# add new line to df_inc
df_inc = pd.concat([df_inc, df_plot_inc])

# cumulative

dt = [vintage_new]
gdp_estimates = [new_gdp_cm]
gdp_impact = [impact_cm]
gdp_rev = [impact_rev_cm]

spec_df = pd.read_excel('Spec_US_update_COVID.xls')
var_cols = spec_df['Category'] + '-'+ spec_df['SeriesID']

# make dt rows of df and gdp_estimates and gdp_impact columns
df_plot_cm = pd.DataFrame({'Date':dt, 'GDP Estimate':gdp_estimates, 'Revision':gdp_rev})
df_plot_cm = df_plot_cm.set_index('Date')

# add seriws_cols to df_plot
for i in range(len(var_cols)):
    df_plot_cm[var_cols[i]] = [0]*len(dt)

# fill each var_cols with Impact for the specific date-time
for i in range(len(dt)):
    df_plot_cm.loc[dt[i],var_cols] = gdp_impact[i]

#replace nan with 0
df_plot_cm = df_plot_cm.fillna(0)

df_plot_cm['Labor'] = df_plot_cm.filter(like='Labor').sum(axis=1)
df_plot_cm['NatAccts'] = df_plot_cm.filter(like='National Accounts').sum(axis=1)
df_plot_cm['Prices'] = df_plot_cm.filter(like='Prices').sum(axis=1)
df_plot_cm['Surveys'] = df_plot_cm.filter(like='Surveys').sum(axis=1)
df_plot_cm['Manuf'] = df_plot_cm.filter(like='Manufacturing').sum(axis=1)
df_plot_cm['Housing'] = df_plot_cm.filter(like='Housing and Construction').sum(axis=1)
df_plot_cm['IntlTrade'] = df_plot_cm.filter(like='International Trade').sum(axis=1)
df_plot_cm['Retail'] = df_plot_cm.filter(like='Retail and Consumption').sum(axis=1)

# add new line to df_inc
df_cml = pd.concat([df_cml, df_plot_cm])

#%% Save to CSV
df_inc.to_csv(f'data/{vintage_new}_nowcast_inc.csv')
df_cml.to_csv(f'data/{vintage_new}_nowcast_cm.csv')