import numpy as np
import pandas as pd
import glob
import sys
import matplotlib.colors as colors

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file, vplot

#from bokeh.sampledata.stocks import AAPL, GOOG, IBM, MSFT

def datetime(x):
    return np.array(x, dtype=np.datetime64)

def rgb_to_hex(red, green, blue):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)

def rgb_to_hex2(rgb_tuple):
    return colors.rgb2hex([1.0*x/255 for x in rgb_tuple])



print("#########################")
print("        STARTING")
print("#########################")

print(sys.platform)
if sys.platform == 'win32':
    datafiles= glob.glob("c://teleferi//stats//get_reddit_metrics//output//outfile_total-subscribers_*")
else:
    datafiles= glob.glob("/home/stats/get_reddit_metrics/output/outfile_total-subscribers_*")
    
print(datafiles)      

p1 = figure(x_axis_type="datetime", width = 780, height = 650, title="Major Cryptoassets Total Reddit Subscribers - Historical Growth")
p1.grid.grid_line_alpha = 0
p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Total Subscribers'
p1.ygrid.band_fill_color = "olive"
p1.ygrid.band_fill_alpha = 0.1

p2 = figure(x_axis_type="datetime", y_axis_type = "log", width = 780, height = 650, title="Major Cryptoassets Total Reddit Subscribers - Historical Growth (LOG SCALE)")
p2.grid.grid_line_alpha = 0
p2.xaxis.axis_label = 'Date'
p2.yaxis.axis_label = 'Total Subscribers'
p2.ygrid.band_fill_color = "olive"
p2.ygrid.band_fill_alpha = 0.1

window_size = 30
window = np.ones(window_size)/float(window_size)


j = len(datafiles)
k = 0
for f in sorted(datafiles):
    
    # outfile_total-subscribers_litecoin
    pair_name = f.split('_')[4]
    print(pair_name)
    data = pd.read_csv(f, sep=',', header=0, error_bad_lines=False)
    data = np.array(data)
    #print("data just received")
    #print(data)
    data_dates = np.array(data[:, 0], dtype=np.datetime64)
    #print("data_dates")
    #print(data_dates)
    data = data[:, 1]
    #print("data")
    #print(data)
    #print(get_hex_color(k, len(datafiles)))
    col1 = 0
    col2 = 0
    col3 = 0
    colx = 1 - k / (j )
    if k % 3 == 0: col1 = colx
    if k % 3 == 1: col2 = colx
    if k % 3 == 2: col3 = colx
        
    print("col1: %s, col2: %s, col3: %s" % (col1, col2, col3))
    rangocolor = colors.rgb2hex((col1 ,col2 ,col3) )

    p1.line(data_dates, data, legend= pair_name, color = rangocolor)
    p2.line(data_dates, data, legend= pair_name, color = rangocolor)
    k += 1
    
p1.legend.location = "top_left"
p2.legend.location = "top_left"
    
output_file("stocks.html", title="stocks.py example")
    
show(vplot(p1, p2))
#show(gridplot([[p1, p2]], plot_width= 780, plot_height= 650))  # open a browser