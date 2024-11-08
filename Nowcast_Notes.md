# Nowcasting-Python

This file contains a collection of notes on the NYFED Nowcast model. The variables are as follows:

    [PAYEMS – All Employees]: Total Nonfarm Payrolls (Seasonally Adjusted): Represents the number of employees on nonfarm payrolls in the U.S.

    [JTSJOL – Job Openings]: Total Nonfarm (Seasonally Adjusted) Reflects the number of job openings available in the U.S. labor market.
    
    [CPIAUCSL – Consumer Price Index for All Urban Consumers]: All Items (Seasonally Adjusted) A measure of the average change in prices paid by urban consumers for a basket of goods and services.
    
    [DGORDER – Manufacturers' New Orders]: Durable Goods (Seasonally Adjusted) Tracks new orders placed with domestic manufacturers for the production of durable goods.
    
    [HSN1F – New One-Family Houses Sold]: United States (Seasonally Adjusted) Represents the number of new single-family houses sold in the U.S.
    
    [RSAFS – Advanced Real Retail and Food Services Sales]: Monthly reatail trade survey. (Seasonally Adjusted) Measures retail and food services sales adjusted for inflation.
    
    [UNRATE – Unemployment Rate]: (Seasonally Adjusted) The percentage of the total labor force that is unemployed but actively seeking employment.
    
    [PPIACO – Producer Price Index]: All Commodities (Seasonally Adjusted) Measures the average change over time in the selling prices received by domestic producers for their output.
    
    [RETAIL – Retail Sales]: Total (Seasonally Adjusted) Tracks the total receipts of retail stores, providing a measure of consumer spending.
    
    [M2SL – M2 Money Stock]: (Seasonally Adjusted) Represents the total amount of money in circulation, including cash, checking deposits, and easily convertible near money.
    
    [ICSA – Initial Claims]: Unemployment Insurance (Seasonally Adjusted) Reflects the number of new claims filed by individuals seeking unemployment benefits.
    
    [NAPM – ISM Manufacturing PMI]: (Seasonally Adjusted) An indicator of the economic health of the manufacturing sector, based on surveys of purchasing managers.
    
    [UMCSENT – University of Michigan: Consumer Sentiment]: (Seasonally Adjusted) Measures consumer confidence in economic activity, based on surveys of households.
        
    [HOUST – Housing Starts]: Total: New Privately Owned Housing Units Started (Seasonally Adjusted) Indicates the number of new housing construction projects begun in a given period.
    
    [INDPRO – Industrial Production Index]: (Seasonally Adjusted) Tracks the real output of all relevant establishments located in the U.S. within the industrial sector.
    
    [PPIFIS – Producer Price Index by Commodity]: Final Demand: Finished Goods (Seasonally Adjusted) Measures the average change over time in the selling prices received by domestic producers for their output.

    [DSPIC96 – Real Disposable Personal Income]: (Chained 2012 Dollars) Measures the total amount of money available to individuals for spending and saving after income taxes.
    
    [BOPTEXP – Exports of Goods and Services]: Balance of Payments Basis (Seasonally Adjusted) Represents the total value of goods and services exported by a country.
    
    [BOPTIMP – Imports of Goods and Services]: Balance of Payments Basis (Seasonally Adjusted) Represents the total value of goods and services imported by a country.
    
    [WHLSLRIMSA – Wholesale Trade]: Inventories to Sales Ratio (Seasonally Adjusted) The ratio of wholesale trade inventories to sales, reflecting how much stock wholesalers have relative to their sales.

    [TTLCONS – Total Consumer Credit Outstanding]: (Seasonally Adjusted) Represents the total amount of outstanding credit used by consumers.
    
    [IR – Import Price Index]: (End Use) Import Price Index == All Commodities.

    [CPILFESL – Consumer Price Index for All Urban Consumers]: All Items Less Food & Energy (Seasonally Adjusted) A measure of core inflation that excludes food and energy prices.
    
    [PCEPILFE – Personal Consumption Expenditures Excluding Food and Energy]: (Seasonally Adjusted) Measures inflation in the prices paid by consumers for goods and services excluding food and energy.

    [PCEPI – Personal Consumption Expenditures Price Index]: (Seasonally Adjusted) Tracks changes in the prices of goods and services purchased by consumers in the U.S.

    [PERMIT – New Private Housing Units Authorized by Building Permits]: (Seasonally Adjusted) Reflects the number of new private housing units authorized by building permits.

    [TCU – Capacity Utilization]: Total Industry (Seasonally Adjusted) The percentage of resources used by manufacturers, miners, and utilities.

    [BUSINV – Manufacturing and Trade Inventories]: (Seasonally Adjusted) Represents the combined value of inventories in manufacturing and trade.
    
    [IQ – Inventories to Sales Ratio]: (Manufacturing and Trade) Measures the ratio of inventories to sales in the manufacturing and trade sectors.
    
    [GACDISA066MSFRBNY – Empire State Manufacturing Survey General Business Conditions Index]: A regional manufacturing index derived from surveys of businesses in New York state.
    
    [PCEC96 – Real Personal Consumption Expenditures]: (Chained 2012 Dollars) Measures real spending by households on goods and services.
    
    [GACDFSA066MSFRBPHI – Philadelphia Fed Manufacturing Index]: A measure of regional manufacturing activity based on a survey of manufacturers in the Philadelphia Federal Reserve district.
    
    [GDPC1 – Real Gross Domestic Product]: (Chained 2012 Dollars) The inflation-adjusted value of goods and services produced by the economy.
    
    [ULCNFB – Unit Labor Costs]: Nonfarm Business Sector (Seasonally Adjusted) Tracks the average cost of labor per unit of output produced in the nonfarm business sector.
    
    [A261RX1Q020SBEA – Real Gross Private Domestic Investment]: Fixed Investment: Residential (Chained 2012 Dollars) Represents inflation-adjusted expenditures by private businesses on residential structures.
    
The model should be run as follows:

    (1a) Use "pull_data.py" to produce data for the most recent vintage -- typically today's date -- and the previous vintage -- typically one week prior. 
    (1b) Insert non-public data available to CEA into xlsx file manually. 
    (2) Update recent vintage in "example_DFM.py" and run to porudce RESDFM.pickle and RES. These results will be used to produce forecasts for variables of interest. 
    (3) Use "example_Nowcast.py" to produce estimate of variables of interest, after updating dates, variable to be forecasted, and horizon date. 

This NYFED Liberty Street note (https://libertystreeteconomics.newyorkfed.org/2018/08/opening-the-toolbox-the-nowcasting-code-on-github/) claims: "Moreover, the nowcasting framework allows us to decompose the nowcast changes into the contributions due to each data release. The impact from a data release is computed multiplying the economic surprise (the difference between a release and its expected value according to the model) by its weight, which reflects how individual indicators affect aggregate economic activity at any given time." 

    How can we do this with our code? 


Might be worth it to do a comparison against NYFed using their recent dates (9/27 and 10/4). And compare with our forecasts (Atlanta, professionals, etc.).

The new NYFED model augments the existing in the following ways:

(1) stochastic volatility, outlier adj to latent variable dynamics. allow for lead-lag relationships (do not assume lags have zero dependency). goal is to introduce nonlinearity which hopefully reduce model's sensitivity to large shocks.
(2) modify loading structure. introduce several other factors to capture COVID data reelases, nominal series correlation (price levels, etc.)
(3) Bayesian estimation approach to generate probability intervals for each point estimate of real GDP growth.


New NY Fed Technical paper
-- add growth LR trend
-- add quarterly transformation to convert to monthly data 
-- start estimation of parameters in 1/1/1985 instead of 1/1/2000 
-- 2 var changes: remove capacity utilization (collinear with industrial production?) and remove PPI