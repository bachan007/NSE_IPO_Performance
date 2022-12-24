import matplotlib.pyplot as plt
import seaborn as sns

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