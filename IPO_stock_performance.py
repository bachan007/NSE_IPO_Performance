import pandas as pd
import numpy as np
import os
from datetime import datetime as dt
import yfinance as yf
from IPOs_analysis import IPOs_data
from plots import donut_chart, line_graph
pd.set_option('display.max_columns',None)

# ipo_df = IPOs_data(save=True)
ipo_df = pd.read_excel('temp_ipo_output.xlsx')

def listing_gain_or_loss(row):
    '''
    This function returns the gain or loss between issue price of IPO and listing price of the stock
    '''
    issue_price,listing_price = row['Issue Price ( )'],row['listing price']
    return np.round(((listing_price-issue_price)/issue_price)*100,2)

def current_gain_or_loss(row):
    '''
    This function returns the gain or loss between listing price and current price of the stock
    '''
    current_price,listing_price = row['LTP'],row['listing price']
    return np.round(((current_price-listing_price)/listing_price)*100,2)


ipo_df['listing_gain_percentage']=ipo_df.apply(listing_gain_or_loss,axis=1)
ipo_df['current_gain_percentage']=ipo_df.apply(current_gain_or_loss,axis=1)


def list_top():
    temp_df = ipo_df.sort_values(by=['current_gain_percentage'])
    loosers=temp_df.head()# returns 5 worst performing stocks
    temp_df = ipo_df.sort_values(by=['current_gain_percentage'],ascending=False)
    winners=temp_df.head()# returns top 5 performing stocks
    return loosers.reset_index(),winners.reset_index()


def adj_price_analysis(ticker):
    data = yf.download(ticker)
    x,y=data.index,data['Adj Close']
    path = line_graph(x,y,title=f" Stock Price Action graph for {ticker} since the date of listing till Last traded day",Flag=False)
    return path





