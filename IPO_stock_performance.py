import pandas as pd
import numpy as np
import os
from datetime import datetime as dt
from IPOs_analysis import IPOs_data
from plots import donut_chart

ipo_df = IPOs_data(save=True)
# ipo_df = pd.read_excel('temp_ipo_output.xlsx')

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


donut_chart(ipo_df.sector)


# def sectorwise_listing(df):
#     df = df.groupby(['sector'])

# print(ipo_df.head())