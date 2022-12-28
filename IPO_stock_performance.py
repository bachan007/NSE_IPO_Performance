'''
calculations for, how the stock has performed since it's listing are being done here. 
'''

import pandas as pd
import numpy as np
import os
from datetime import datetime as dt
import yfinance as yf
from IPOs_analysis import IPOs_data
from plots import donut_chart, line_graph
pd.set_option('display.max_columns',None)

# Uncomment below line for latest data and comment the next line
ipo_df,analysis = IPOs_data(save=True)
# ipo_df = pd.read_excel('temp_ipo_output.xlsx')

def listing_gain_or_loss(row):
    '''
    This function returns the gain or loss between issue price of IPO and listing price of the stock
    '''
    try:
        issue_price,listing_price = row['Issue Price ( )'],row['listing price']
        return np.round(((listing_price-issue_price)/issue_price)*100,2)
    except:
        return None

def current_gain_or_loss(row):
    '''
    This function returns the gain or loss between listing price and current price of the stock
    '''
    try:
        current_price,listing_price = row['LTP'],row['listing price']
        return np.round(((current_price-listing_price)/listing_price)*100,2)
    except:
        return None

ipo_df['listing_gain_percentage']=ipo_df.apply(listing_gain_or_loss,axis=1)
ipo_df['current_gain_percentage']=ipo_df.apply(current_gain_or_loss,axis=1)


def list_top():
    '''
    This function returns the top 5 and worst 5 performers of stock IPOs.
    '''
    temp_df = ipo_df.sort_values(by=['current_gain_percentage'])
    loosers=temp_df.head()# returns 5 worst performing stocks
    temp_df = ipo_df.sort_values(by=['current_gain_percentage'],ascending=False)
    winners=temp_df.head()# returns top 5 performing stocks
    return loosers.reset_index(),winners.reset_index()


def adj_price_analysis(ticker):
    '''
    This function collects the price movement of the stock and 
    creates the line grapgh for the date vs adj close price.
    '''
    data = yf.download(ticker)
    x,y=data.index,data['Adj Close']
    path = line_graph(x,y,title=f" Stock Price Action graph for {ticker} since the date of listing till Last traded day",Flag=False)
    return path

def grouping(category,output_col):
    '''
    This function return the dictionay whith key as it's category (sector/industry) 
    and associated companies as it's values. 
    '''
    dictnry = {}
    temp = ipo_df.groupby([category,output_col]).size().reset_index()
    keys = temp[category].unique()
    for key in keys:
        vals = temp[temp[category]==key][output_col].tolist()
        dictnry[key]=vals
    return dictnry










