import numpy as np
import pandas as pd
import glob
import sys

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
#from bokeh.sampledata.stocks import AAPL, GOOG, IBM, MSFT

def datetime(x):
    return np.array(x, dtype=np.datetime64)

print("#########################")
print("        STARTING")
print("#########################")

print(sys.platform)
if sys.platform == 'win32':
    datafiles= glob.glob("c://teleferi//stats//get_reddit_metrics//output//outfile_total-subscribers_*")
    print(datafiles)
else:
    if len(sys.argv)>0:
        print(sys.argv)
        candlesize=sys.argv[1]
        asset=sys.argv[2]
        print(candlesize)
        print(asset)
    else:
        print("No arguments received")
    if candlesize=="":
        candlesize="1h" #"15min"
        print("No candlesize provided. Using 5min")
    if asset=="":
        asset="CNY"
        print("No asset provided. Using OK_BTC_CNY")
    datafiles= glob.glob("/home/CSV_Tickers/??_BTC_"+asset+".csv")
    
print(datafiles)      

p1 = figure(x_axis_type="datetime", title="Major Cryptoassets Total Reddit Subscribers - Historical Growth")
p1.grid.grid_line_alpha = 0
p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Total Subscribers'
p1.ygrid.band_fill_color = "olive"
p1.ygrid.band_fill_alpha = 0.1

for f in sorted(datafiles):
    # outfile_total-subscribers_litecoin
    pair_name = f.split('_')[4]
    data = pd.read_csv(f, sep=',', header=0, error_bad_lines=False)
    data = np.array(data)
    print("data just received")
    print(data)
    data_dates = np.array(data[:, 0], dtype=np.datetime64)
    print("data_dates")
    print(data_dates)
    data = data[:, 1]
    print("data")
    print(data)
    
    window_size = 30
    window = np.ones(window_size)/float(window_size)
    
    
    p1.line(data_dates, data, legend= pair_name)
    
    p1.legend.location = "top_left"
    
    output_file("stocks.html", title="stocks.py example")
    
show(gridplot([[p1]], plot_width= 780, plot_height=450))  # open a browser