"""
Tomer Fidelman
October 2024

This files pulls in data and creates a .xls file in line with the existing NYFED data.
"""

#%% Import Libraries
import pandas as pd
import numpy as np
from fredapi import Fred

#%% Initialize the FRED API
api_key = '0a39e3ca58697605ed2076ae50067449'  # Replace with your actual API key
fred = Fred(api_key=api_key)
today = pd.Timestamp.today().date()

#%% Define ALFRED codes and date range
alfred_codes = {
    'PAYEMS': 'PAYEMS',
    'JTSJOL': 'JTSJOL',
    'CPIAUCSL': 'CPIAUCSL',
    'DGORDER': 'DGORDER',
    'HSN1F': 'HSN1F',
    'RSAFS': 'RSAFS',
    'UNRATE': 'UNRATE',
    'HOUST': 'HOUST',
    'INDPRO': 'INDPRO',
    'PPIFIS': 'PPIFIS',
    'DSPIC96': 'DSPIC96',
    'BOPTEXP': 'BOPTEXP',
    'BOPTIMP': 'BOPTIMP',
    'WHLSLRIMSA': 'WHLSLRIMSA',
    'TTLCONS': 'TTLCONS',
    'IR': 'IR',
    'CPILFESL': 'CPILFESL',
    'PCEPILFE': 'PCEPILFE',
    'PCEPI': 'PCEPI',
    'PERMIT': 'PERMIT',
    'TCU': 'TCU',
    'BUSINV': 'BUSINV',
    'IQ': 'IQ',
    'GACDISA066MSFRBNY': 'GACDISA066MSFRBNY',
    'PCEC96': 'PCEC96',
    'GACDFSA066MSFRBPHI': 'GACDFSA066MSFRBPHI',
    'GDPC1': 'GDPC1',
    'ULCNFB': 'ULCNFB',
    'A261RX1Q020SBEA': 'A261RX1Q020SBEA'
}

real_start_date = '1985-01-01'
real_end_date = '2024-07-03'
start_date = real_start_date
end_date = '2024-07-03' 

#%% Pull data for each variable from ALFRED and store in a dictionary
data = {}

for var_name, alfred_code in alfred_codes.items():
    try:
        # Fetch data from ALFRED
        series_data = fred.get_series(alfred_code, start=start_date, end=end_date, 
                                       realtime_start=real_start_date, realtime_end=real_end_date)
        series_data = series_data[series_data.index >= start_date]
        # Store the series in the dictionary
        data[var_name] = series_data
    except Exception as e:
        print(f"Error fetching {var_name}: {e}")

#%% Create a DataFrame from the dictionary
df = pd.DataFrame(data)
# shift GDPC1	ULCNFB	A261RX1Q020SBEA forward 2 periods
df['GDPC1'] = df['GDPC1'].shift(2)
df['ULCNFB'] = df['ULCNFB'].shift(2)
df['A261RX1Q020SBEA'] = df['A261RX1Q020SBEA'].shift(2)
# rename index column 'Date'
df.index.name = 'Date'


#%% Save to Excel
output_file = '{}.xlsx'.format(end_date)  # Specify the output file name
# Set path data / US 
output_file = 'data/US/' + output_file
df.to_excel(output_file, index=True, sheet_name='ALFRED Data')

print(f"Data has been successfully pulled and saved to {output_file} for date, {end_date}.")


# %%
