import pandas as pd
import numpy as np
import os
from datetime import dateteime as dt
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
ipo_df = pd.read_csv(os.path.join(os.path.abspath(os.getcwd()),'files/ipo_data.csv'),index_col=0)

# assigning the company symbol to the IPOs
for comp in ipo_df['Name of the issue'].to_list():
    ipo_df.loc[ipo_df['Name of the issue']==comp,'symbol']=get_symbol(comp)

def stock_info(symbol,index_symbol='.NS'):
    company = yf.Ticker(f'{symbol}.{index_symbol}')
    company_info = company.info
    dic = {}
    dic['Date']=dt.date.today()


