
# coding: utf-8

# In[ ]:

#Load pandas reader to read data from google finance


# In[1]:

from pandas_datareader import data, wb
import pandas as pd
import numpy as np
import datetime
get_ipython().magic('matplotlib inline')


# In[ ]:

#using google finance as source


# In[2]:

start = datetime.datetime(2006, 1, 1)
end = datetime.datetime(2016, 1, 1)


# In[3]:

# Bank of America
BAC = data.DataReader("BAC", 'google', start, end)

# CitiGroup
C = data.DataReader("C", 'google', start, end)

# Goldman Sachs
GS = data.DataReader("GS", 'google', start, end)

# JPMorgan Chase
JPM = data.DataReader("JPM", 'google', start, end)

# Morgan Stanley
MS = data.DataReader("MS", 'google', start, end)

# Wells Fargo
WFC = data.DataReader("WFC", 'google', start, end)


# In[ ]:

# doing this for a Panel Object


# In[4]:

df = data.DataReader(['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC'],'google', start, end)


# In[ ]:

#Creating a list of the ticker symbols (as strings) in alphabetical order


# In[5]:

tickers = ['BAC', 'C', 'GS', 'JPM', 'MS', 'WFC']


# In[ ]:

#Using pd.concat to concatenate the bank dataframes together to a single data frame called bank_stocks. Setting the keys argument equal to the tickers list


# In[6]:

bank_stocks = pd.concat([BAC, C, GS, JPM, MS, WFC],axis=1,keys=tickers)


# In[ ]:

#Setting the column name levels


# In[7]:

bank_stocks.columns.names = ['Bank Ticker','Stock Info']


# In[ ]:

#Checking the head of the bank_stocks dataframe


# In[8]:

bank_stocks.head()


# In[ ]:

#EDA..Sample questions


# In[ ]:

#What is the max Close price for each bank's stock throughout the time period?


# In[9]:

bank_stocks.xs(key='Close',axis=1,level='Stock Info').max()


# In[ ]:

#Creating a new empty DataFrame called returns. This dataframe will contain the returns for each bank's stock.


# In[10]:

returns = pd.DataFrame()


# In[ ]:

#using pandas pct_change() method on the Close column to create a column representing this return value. Creating a for loop that goes and for each Bank Stock Ticker creates this returns column and set's it as a column in the returns DataFrame.


# In[11]:

for tick in tickers:
    returns[tick+' Return'] = bank_stocks[tick]['Close'].pct_change()
returns.head()


# In[ ]:

#Creating a pairplot using seaborn of the returns dataframe. I will get to know the stock stands out to you? 


# In[12]:

#returns[1:]
import seaborn as sns
sns.pairplot(returns[1:])


# In[ ]:

#Using this returns DataFrame, figuring out on what dates each bank stock had the best and worst single day returns.
#I notice that 4 of the banks share the same day for the worst drop, did anything significant happen that day?


# In[13]:

# Worst Drop (4 of them on Inauguration day)
returns.idxmin()


# In[ ]:

# I have noticed that Citigroup's largest drop and biggest gain were very close to one another,
#did anythign significant happen in that time frame?


# In[14]:

# Best Single Day Gain
# citigroup stock split in May 2011, but also JPM day after inauguration.
returns.idxmax()


# In[ ]:

#By looking standard deviation of the returns,I would classify which stock is the riskiest over the entire time period? 
#classifying the riskiest for the year 2015?


# In[15]:

returns.std() # Citigroup riskiest


# In[16]:

returns.ix['2015-01-01':'2015-12-31'].std() # Very similar risk profiles, but Morgan Stanley or BofA


# In[ ]:

#Creating a distplot using seaborn of the 2015 returns for Morgan Stanley


# In[17]:

sns.distplot(returns.ix['2015-01-01':'2015-12-31']['MS Return'],color='green',bins=100)


# In[ ]:

#Creating a distplot using seaborn of the 2008 returns for CitiGroup


# In[18]:

sns.distplot(returns.ix['2008-01-01':'2008-12-31']['C Return'],color='red',bins=100)


# In[ ]:

#for visualization importing libraries


# In[19]:

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')
get_ipython().magic('matplotlib inline')

# Optional Plotly Method Imports
import plotly
import cufflinks as cf
cf.go_offline()


# In[ ]:

#Creating a line plot showing Close price for each bank for the entire index of time


# In[20]:

for tick in tickers:
    bank_stocks[tick]['Close'].plot(figsize=(12,4),label=tick)
plt.legend()


# In[21]:

bank_stocks.xs(key='Close',axis=1,level='Stock Info').plot()


# In[22]:

# plotly
bank_stocks.xs(key='Close',axis=1,level='Stock Info').iplot()


# In[ ]:

#analyzing the moving averages for these stocks in the year 2008.


# In[ ]:

#Plotting the rolling 30 day average against the Close Price for Bank Of America's stock for the year 2008


# In[23]:

plt.figure(figsize=(12,6))
BAC['Close'].ix['2008-01-01':'2009-01-01'].rolling(window=30).mean().plot(label='30 Day Avg')
BAC['Close'].ix['2008-01-01':'2009-01-01'].plot(label='BAC CLOSE')
plt.legend()


# In[ ]:

#Creating a heatmap of the correlation between the stocks Close Price.


# In[24]:

sns.heatmap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)


# In[ ]:

#Using seaborn's clustermap to cluster the correlations together:


# In[25]:

sns.clustermap(bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr(),annot=True)


# In[26]:

close_corr = bank_stocks.xs(key='Close',axis=1,level='Stock Info').corr()
close_corr.iplot(kind='heatmap',colorscale='rdylbu')


# In[ ]:

#using cufflinks library to create some Technical Analysis plots
#Using .iplot(kind='candle) to create a candle plot of Bank of America's stock from Jan 1st 2015 to Jan 1st 2016


# In[27]:

BAC[['Open', 'High', 'Low', 'Close']].ix['2015-01-01':'2016-01-01'].iplot(kind='candle')


# In[ ]:

#Using .ta_plot(study='sma') to create a Simple Moving Averages plot of Morgan Stanley for the year 2015


# In[28]:

MS['Close'].ix['2015-01-01':'2016-01-01'].ta_plot(study='sma',periods=[13,21,55],title='Simple Moving Averages')


# In[ ]:

#Using .ta_plot(study='boll') to create a Bollinger Band Plot for Bank of America for the year 2015


# In[29]:

BAC['Close'].ix['2015-01-01':'2016-01-01'].ta_plot(study='boll')


# In[ ]:



