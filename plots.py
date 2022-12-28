# different graphs which are being called on other scripts

import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpf
import numpy as np

import warnings
warnings.filterwarnings('ignore')


def addlabels(x,y):
    '''Displays the values on bars'''
    for i in range(len(x)):
        plt.text(i, np.round(y[i],2), np.round(y[i],2), ha = 'center')


def donut_chart(value_series,save=False):
    '''
    This function returns the donut chart according to the provided data.
    For saving the chart locally use save = True
    '''
    def my_fmt(x):
        return '{:.2f}%\n({:.0f})'.format(x, total*x/100)
    total = len(value_series)    
    plt.figure(figsize=(10,7))
    plt.pie(list(value_series.value_counts()),
    labels=list(value_series.value_counts().index),
    wedgeprops=dict(width=0.3,edgecolor='w',radius=1),autopct=my_fmt,shadow=True)
    plt.show()


# def candlestick_graph(df,symbol,Flag=True):
#     mpf.plot(df,type='candle',volume=True)
#     plt.title(f"{symbol} average price movement from the data of listing till last traded day")
#     plt.xlabel('date')
#     plt.ylabel('price in INR')
#     if Flag:
#         plt.show()
#     else:
#         plt.savefig(f"Plots/{symbol}.png")
#         img_path = f"Plots/{symbol}.png"
#         print(f"{symbol} saved in Plots directory")
#         return img_path


def line_graph(x,y,title=None,Flag=True):
    '''
    If you want to save the chart with the path as a returning variable,
    make Flag=False
    '''
    plt.figure(figsize=(12,7))
    sns.lineplot(x,y)
    plt.title(title)
    addlabels(x,y)
    plt.xticks(rotation=90)
    plt.title(title)
    if Flag:
        plt.show()
    else:
        plt.savefig(f"Plots/{title}.png")
        img_path = f"Plots/{title}.png"
        print(f"{title} saved in Plots directory")
        return img_path