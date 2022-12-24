import pandas as pd
import numpy as np
import os
from datetime import datetime as dt
import yfinance as yf

# reading the equity file which contains the nse listed companies info
equity_df = pd.read_csv(os.path.join(os.path.abspath(os.getcwd()),'input_files/EQUITY_L.csv'))

# cleaning the column names 
def clean_columns(columns):
    clean_cols = [col.strip() for col in columns]
    return clean_cols
cleaned_cols = clean_columns(equity_df.columns.to_list())
equity_df.columns = cleaned_cols
equity_df['NAME OF COMPANY'] = equity_df['NAME OF COMPANY'].apply(lambda x : x.title().strip())
equity_df['SYMBOL'] = equity_df['SYMBOL'].apply(lambda x : x.upper().strip())

def get_symbol(company_name):
    '''
    This function checks whether the company name is present in stocks list provided by NSEINDIA
    or not. If the name is correct and present int he list, then it return the symbol or ticker 
    of the company.
    I will recommend to download the updated list from when you extract the updated IPO list :
    https://www1.nseindia.com/content/equities/EQUITY_L.csv
    This file contains all the NSE listed companies information.
    '''
    company_name=company_name.title().strip()
    temp_df=equity_df[equity_df['NAME OF COMPANY']==company_name]
    if temp_df.shape[0]!=0:
        sym = temp_df['SYMBOL'].values[0]
        return sym
    else:
        print(f'Data not Found for {company_name}')
        return None

# reading the ipo list file 
ipo_df = pd.read_csv(os.path.join(os.path.abspath(os.getcwd()),'IPO_file/ipo_data.csv'),index_col=0)

# assigning the company symbol to the IPOs
for comp in ipo_df['Name of the issue'].to_list():
    ipo_df.loc[ipo_df['Name of the issue']==comp,'symbol']=get_symbol(comp)


def stock_info(df,symbol,index_symbol='NS'):
    # desired information list --> can be updated according to the requirements
    info_list = ['currentPrice','fiftyTwoWeekHigh','fiftyTwoWeekLow','dayHigh','dayLow','sector','website','industry']
    company = yf.Ticker(f'{symbol}.{index_symbol}')
    company_info = company.info
    for ele in info_list:
        df.loc[df['symbol']==symbol,ele]=company_info[ele]


def stock_price_action(symbol,index_symbol='NS'):
    ticker = f'{symbol}.{index_symbol}'
    data = yf.download(ticker)
    data.reset_index(inplace=True)
    data['High']=data['High'].round(decimals=1)
    data['Low']=data['Low'].round(decimals=1)
    listed_on = data.head(1)['Date'][0].strftime('%d-%b-%Y')
    opening_price = data.head(1)['Open'][0]
    max_price = max(data['High'])
    max_on = pd.to_datetime(data[data['High']==max_price]['Date'].values[0]).strftime('%d-%b-%Y')
    min_price = data['Low'].min()
    min_on = pd.to_datetime(data[data['Low']==min_price]['Date'].values[0]).strftime('%d-%b-%Y')
    current_price = data.tail(1)['Adj Close']
    stock_info(ipo_df,symbol)
    temp_df = ipo_df[ipo_df['symbol']==symbol]
    analysis = f'''
    {temp_df['Name of the issue'].values[0]} listed on NSE on {listed_on} with the opening price of {opening_price} INR. 
    It created a high of {max_price} on {max_on} and low of {min_price} on {min_on}.
    Currently trading at {temp_df['LTP'].values[0]} INR.

    '''
    ipo_df.loc[
        ipo_df['symbol']==symbol,
    ['max_on','min_on','max_high','max_low','listing price']
    ]=max_on,min_on,max_price,min_price,opening_price
    print(analysis)


def IPOs_data(save=False):
    
    for symbol in ipo_df['symbol'].to_list():
        stock_price_action(symbol)
    while save:
        ipo_df.to_excel('temp_ipo_output.xlsx',index=False)
        save=False

    return ipo_df





