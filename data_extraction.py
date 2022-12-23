from bs4 import BeautifulSoup
import pandas as pd
from browser_automation import page_source
import datetime
import os


def store_updated_IPO_data(page_source):
    '''
    '''
    # Parsing the page source
    soup = BeautifulSoup(page_source,'html.parser')

    # getting the division of table of IPOs
    div = soup.find('div',{'id':"replacetext"})

    # extracting the header of table
    col_list = [col_name.text.strip().replace('\n','').replace('\t','') for col_name in div.find_all("th")]

    # extracting the table values in ordered form
    table_data = [[td.text.strip().replace('\n','').replace('\t','') for td in tr.find_all('td')] for tr in div.find_all('tr')]
    
    # storing the table data into a dataframe
    ipo_df = pd.DataFrame(table_data,columns=col_list)
    ipo_df.dropna(how='all',inplace=True)
    ipo_df=ipo_df[(ipo_df['Issue Price ( )']!='-')
        & (ipo_df['Date ofListing']!='-')]
    ipo_df=ipo_df[['Name of the issue','Issue Price ( )', 'LTP',
            'Issue Start Date', 'Issue End Date', 'Price Range', 'Date ofListing']].reset_index(drop=True)
    if not os.path.exists('IPO_file'):
        os.mkdir('IPO_file')
        ipo_df.to_csv(f'IPO_file/ipo_data.csv')
    else:
        ipo_df.to_csv(f'IPO_file/ipo_data.csv')

    print(f"IPOs data updated on {datetime.datetime.now()}")

if __name__=='__main__':
    store_updated_IPO_data(page_source)