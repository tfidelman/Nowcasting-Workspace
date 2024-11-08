#-------------------------------------------------Libraries
#%%

from Functions.load_data import load_data
from Functions.load_spec import load_spec
from Functions.update_Nowcast import update_nowcast
import os
import pickle
import datetime
import pandas as pd

#%%
#-------------------------------------------------User Inputs
series = 'GDPC1'  # Nowcasting real GDP (GDPC1) <fred.stlouisfed.org/series/GDPC1>
period = '2024q4' # Forecasting target quarter


#-------------------------------------------------Load model specification and first vintage of data.
Spec   = load_spec('Spec_US_update_COVID.xls')


#-------------------------------------------------Load DFM estimation results structure `Res`
with open('ResFINAL.pickle', 'rb') as handle:
    Res = pickle.load(handle)
#%%
#-------------------------------------------------Update nowcast and decompose nowcast changes into news.
# Nowcast update from week of December 7 to week of December 16, 2016
vintage_old  = '2024-10-02'
vintage_today = datetime.datetime.now().strftime("%Y-%m-%d")
vintage_new = vintage_today
#%%
datafile_old = os.path.join('data','US',vintage_old + '.xlsx')
datafile_new = os.path.join('data','US',vintage_new + '.xlsx')

# Load datasets for each vintage
X_old,_,_    = load_data(datafile_old,Spec)
X_new,Time,_ = load_data(datafile_new,Spec)


Res = Res['Res']

old_gdp_today, new_gdp_today, impact_today, impact_rev_today = update_nowcast(X_old,X_new,Time,Spec,Res,series,period,vintage_old,vintage_new)
# prints new nowcast and vintage nowcast
# prints the news and then prints the impact by variable and overall revision. 
# revision cannot be broken into different vars


###########################################################
################    HISTORICAL FOR FIGURE  ################
###########################################################
#%% OCT 31 2024
vintage_old  = '2024-10-02'
vintage_new  = '2024-10-31'
datafile_old = os.path.join('data','US',vintage_old + '.xlsx')
datafile_new = os.path.join('data','US',vintage_new + '.xlsx')

# Load datasets for each vintage
X_old,_,_    = load_data(datafile_old,Spec)
X_new,Time,_ = load_data(datafile_new,Spec)

with open('ResFINAL.pickle', 'rb') as handle:
    Res = pickle.load(handle)
    
Res = Res['Res']

old_gdp_10_31, new_gdp_10_31, impact_10_31, impact_rev_10_31 = update_nowcast(X_old,X_new,Time,Spec,Res,series,period,vintage_old,vintage_new)

# OCT 24 2024
vintage_new  = '2024-10-24'
datafile_old = os.path.join('data','US',vintage_old + '.xlsx')
datafile_new = os.path.join('data','US',vintage_new + '.xlsx')

# Load datasets for each vintage
X_old,_,_    = load_data(datafile_old,Spec)
X_new,Time,_ = load_data(datafile_new,Spec)


old_gdp_10_24, new_gdp_10_24, impact_10_24, impact_rev_10_24 = update_nowcast(X_old,X_new,Time,Spec,Res,series,period,vintage_old,vintage_new)

# OCT 17 2024

vintage_new = '2024-10-17'
datafile_old = os.path.join('data','US',vintage_old + '.xlsx')
datafile_new = os.path.join('data','US',vintage_new + '.xlsx')

# Load datasets for each vintage
X_old,_,_    = load_data(datafile_old,Spec)
X_new,Time,_ = load_data(datafile_new,Spec)


old_gdp_10_17, new_gdp_10_17, impact_10_17, impact_rev_10_17 = update_nowcast(X_old,X_new,Time,Spec,Res,series,period,vintage_old,vintage_new)


# OCT 10 2024

vintage_new = '2024-10-10'

datafile_old = os.path.join('data','US',vintage_old + '.xlsx')
datafile_new = os.path.join('data','US',vintage_new + '.xlsx')

# Load datasets for each vintage
X_old,_,_    = load_data(datafile_old,Spec)
X_new,Time,_ = load_data(datafile_new,Spec)


old_gdp_10_10, new_gdp_10_10, impact_10_10, impact_rev_10_10 = update_nowcast(X_old,X_new,Time,Spec,Res,series,period,vintage_old,vintage_new)


#%% Plotting. Need line plot and then bar chart with impact

# store date time for each vintage

dt = ['2024-10-02', '2024-10-10','2024-10-17','2024-10-24','2024-10-31', vintage_today]
gdp_estimates = [old_gdp_today, new_gdp_10_10, new_gdp_10_17, new_gdp_10_24, new_gdp_10_31, new_gdp_today]
gdp_impact = [0 , impact_10_10, impact_10_17, impact_10_24, impact_10_31, impact_today]
gdp_rev = [0, impact_rev_10_10, impact_rev_10_17, impact_rev_10_24, impact_rev_10_31, impact_rev_today]
#%%
spec_df = pd.read_excel('Spec_US_update_COVID.xls')
var_cols = spec_df['Category'] + '-'+ spec_df['SeriesID']
var_cols

#%%
# make dt rows of df and gdp_estimates and gdp_impact columns
df_plot = pd.DataFrame({'Date':dt, 'GDP Estimate':gdp_estimates, 'Revision':gdp_rev})
df_plot = df_plot.set_index('Date')

# add seriws_cols to df_plot
for i in range(len(var_cols)):
    df_plot[var_cols[i]] = [0]*len(dt)

# fill each var_cols with Impact for the specific date-time
for i in range(len(dt)):
    df_plot.loc[dt[i],var_cols] = gdp_impact[i]

#replace nan with 0
df_plot = df_plot.fillna(0)

#%% add new columns, which sum up the impact by var_cols by grouping by term before the hyphen in column title name
# sum up the impact by term: Labor
# sum if column starts with "Labor-"

# sum up the impact by term: Labor

df_plot['Labor'] = df_plot.filter(like='Labor').sum(axis=1)
df_plot['NatAccts'] = df_plot.filter(like='National Accounts').sum(axis=1)
df_plot['Prices'] = df_plot.filter(like='Prices').sum(axis=1)
df_plot['Surveys'] = df_plot.filter(like='Surveys').sum(axis=1)
df_plot['Manuf'] = df_plot.filter(like='Manufacturing').sum(axis=1)
df_plot['Housing'] = df_plot.filter(like='Housing and Construction').sum(axis=1)
df_plot['IntlTrade'] = df_plot.filter(like='International Trade').sum(axis=1)
df_plot['Retail'] = df_plot.filter(like='Retail and Consumption').sum(axis=1)

#%% save as csv
df_plot.to_csv('data/20241107_nowcast.csv')

###########################################################
###########  Repeat but Incremental News   ################
###########################################################
#%% 
with open('ResFINAL.pickle', 'rb') as handle:
    Res = pickle.load(handle)
    
Res = Res['Res']

## OCT 10 2024
vintage_old  = '2024-10-02'
vintage_new = '2024-10-10'

datafile_old = os.path.join('data','US',vintage_old + '.xlsx')
datafile_new = os.path.join('data','US',vintage_new + '.xlsx')

# Load datasets for each vintage
X_old,_,_    = load_data(datafile_old,Spec)
X_new,Time,_ = load_data(datafile_new,Spec)

old_gdp_10_10, new_gdp_10_10, impact_10_10, impact_rev_10_10 = update_nowcast(X_old,X_new,Time,Spec,Res,series,period,vintage_old,vintage_new)

## OCT 17 2024
vintage_old  = '2024-10-10'
vintage_new = '2024-10-17'

datafile_old = os.path.join('data','US',vintage_old + '.xlsx')
datafile_new = os.path.join('data','US',vintage_new + '.xlsx')

# Load datasets for each vintage
X_old,_,_    = load_data(datafile_old,Spec)
X_new,Time,_ = load_data(datafile_new,Spec)

old_gdp_10_17, new_gdp_10_17, impact_10_17, impact_rev_10_17 = update_nowcast(X_old,X_new,Time,Spec,Res,series,period,vintage_old,vintage_new)

## OCT 24 2024
vintage_old  = '2024-10-17'
vintage_new = '2024-10-24'

datafile_old = os.path.join('data','US',vintage_old + '.xlsx')
datafile_new = os.path.join('data','US',vintage_new + '.xlsx')

# Load datasets for each vintage
X_old,_,_    = load_data(datafile_old,Spec)
X_new,Time,_ = load_data(datafile_new,Spec)

old_gdp_10_24, new_gdp_10_24, impact_10_24, impact_rev_10_24 = update_nowcast(X_old,X_new,Time,Spec,Res,series,period,vintage_old,vintage_new)

## OCT 31 2024
vintage_old  = '2024-10-24'
vintage_new = '2024-10-31'

datafile_old = os.path.join('data','US',vintage_old + '.xlsx')
datafile_new = os.path.join('data','US',vintage_new + '.xlsx')

# Load datasets for each vintage
X_old,_,_    = load_data(datafile_old,Spec)
X_new,Time,_ = load_data(datafile_new,Spec)

old_gdp_10_31, new_gdp_10_31, impact_10_31, impact_rev_10_31 = update_nowcast(X_old,X_new,Time,Spec,Res,series,period,vintage_old,vintage_new)

#
## TODAY
vintage_old  = '2024-10-31'
vintage_new = '2024-11-07'

datafile_old = os.path.join('data','US',vintage_old + '.xlsx')
datafile_new = os.path.join('data','US',vintage_new + '.xlsx')

# Load datasets for each vintage
X_old,_,_    = load_data(datafile_old,Spec)
X_new,Time,_ = load_data(datafile_new,Spec)

old_gdp_today, new_gdp_today, impact_today, impact_rev_today = update_nowcast(X_old,X_new,Time,Spec,Res,series,period,vintage_old,vintage_new)

#%% Plotting. Need line plot and then bar chart with impact

# store date time for each vintage

dt = ['2024-10-02', '2024-10-10','2024-10-17','2024-10-24','2024-10-31', vintage_new]
gdp_estimates = [old_gdp_today, new_gdp_10_10, new_gdp_10_17, new_gdp_10_24, new_gdp_10_31, new_gdp_today]
gdp_impact = [0 , impact_10_10, impact_10_17, impact_10_24, impact_10_31, impact_today]
gdp_rev = [0, impact_rev_10_10, impact_rev_10_17, impact_rev_10_24, impact_rev_10_31, impact_rev_today]
#
spec_df = pd.read_excel('Spec_US_update_COVID.xls')
var_cols = spec_df['Category'] + '-'+ spec_df['SeriesID']
var_cols

#
# make dt rows of df and gdp_estimates and gdp_impact columns
df_plot = pd.DataFrame({'Date':dt, 'GDP Estimate':gdp_estimates, 'Revision':gdp_rev})
df_plot = df_plot.set_index('Date')

# add seriws_cols to df_plot
for i in range(len(var_cols)):
    df_plot[var_cols[i]] = [0]*len(dt)

# fill each var_cols with Impact for the specific date-time
for i in range(len(dt)):
    df_plot.loc[dt[i],var_cols] = gdp_impact[i]

#replace nan with 0
df_plot = df_plot.fillna(0)

# add new columns, which sum up the impact by var_cols by grouping by term before the hyphen in column title name
# sum up the impact by term: Labor
# sum if column starts with "Labor-"

# sum up the impact by term: Labor

df_plot['Labor'] = df_plot.filter(like='Labor').sum(axis=1)
df_plot['NatAccts'] = df_plot.filter(like='National Accounts').sum(axis=1)
df_plot['Prices'] = df_plot.filter(like='Prices').sum(axis=1)
df_plot['Surveys'] = df_plot.filter(like='Surveys').sum(axis=1)
df_plot['Manuf'] = df_plot.filter(like='Manufacturing').sum(axis=1)
df_plot['Housing'] = df_plot.filter(like='Housing and Construction').sum(axis=1)
df_plot['IntlTrade'] = df_plot.filter(like='International Trade').sum(axis=1)
df_plot['Retail'] = df_plot.filter(like='Retail and Consumption').sum(axis=1)

df_plot
#%% save as csv
df_plot.to_csv('data/20241107_nowcast_incrmt.csv')