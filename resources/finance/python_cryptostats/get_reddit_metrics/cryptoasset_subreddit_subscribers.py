import numpy as np
import pandas as pd
import glob
import sys
import matplotlib.colors as colors

from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file, vplot, ColumnDataSource, save
from bokeh.models import HoverTool

tools_to_show = 'box_zoom,pan,save,hover,resize,reset,tap,wheel_zoom'  

def datetime(x):
    return np.array(x, dtype=np.datetime64)

if sys.platform == 'win32':
    datafiles= glob.glob("c://teleferi//stats//get_reddit_metrics//output//outfile_total-subscribers_*")
else:
    datafiles= glob.glob("/home/stats/get_reddit_metrics/output/outfile_total-subscribers_*")
    
print(datafiles)      

p1 = figure(x_axis_type="datetime", width = 640, height = 650, title="Major Cryptoassets Total Reddit Subscribers - Historical Growth", tools = tools_to_show)
p1.grid.grid_line_alpha = 0
p1.xaxis.axis_label = 'Date'
p1.yaxis.axis_label = 'Total Subscribers'
p1.ygrid.band_fill_color = "olive"
p1.ygrid.band_fill_alpha = 0.1

p2 = figure(x_axis_type="datetime", y_axis_type = "log", width = 640, height = 650, title="Major Cryptoassets Total Reddit Subscribers - Historical Growth (LOG SCALE)", tools = tools_to_show)
p2.grid.grid_line_alpha = 0
p2.xaxis.axis_label = 'Date'
p2.yaxis.axis_label = 'Total Subscribers'
p2.ygrid.band_fill_color = "olive"
p2.ygrid.band_fill_alpha = 0.1

window_size = 30
window = np.ones(window_size)/float(window_size)
pair_list = []

j = len(datafiles)
k = 0
for f in sorted(datafiles):
    pair_name = f.split('_')[4]
    pair_list.append(pair_name)

for f in sorted(datafiles):    
    print(pair_list[k])
    datax = pd.read_csv(f, sep=',', header=0, error_bad_lines=False)
    datax = np.array(datax)
    data_dates = np.array(datax[:, 0] , dtype=np.datetime64)
    datax = datax[:, 1]
    col1 = 0
    col2 = 0
    col3 = 0
    colx = 1 - k / (j )
    if k % 3 == 0: col1 = colx
    if k % 3 == 1: col2 = colx
    if k % 3 == 2: col3 = colx
       
    rangocolor = colors.rgb2hex((col1 ,col2 ,col3) )

    p1.line(data_dates, datax, legend = pair_list[k], color = rangocolor)
    p2.line(data_dates, datax, legend = pair_list[k], color = rangocolor)
    
    k += 1
    
p1.legend.location = "top_left"
p2.legend.location = "top_left"
p1.legend.background_fill_alpha = 0.3
p2.legend.background_fill_alpha = 0.3

hover1 = p1.select(dict(type=HoverTool))
hover1.tooltips = [("Subreddit" , '@pair_list'),   ("Value", '@datax.tolist()')]
hover1.mode = 'mouse'

hover2 = p2.select(dict(type=HoverTool))
hover2.tooltips = [("Subreddit" , '@pair_list'),   ("Value", '@datax.tolist()')]
hover2.mode = 'mouse'
    
output_file("/home/stats/output/cryptoasset_subreddit_subscribers.html", title="Major Cryptoassets Total Reddit Subscribers - Historical Growth")

if sys.platform == 'win32':
    output_file("cryptoasset_subreddit_subscribers.html", title="Major Cryptoassets Total Reddit Subscribers - Historical Growth")
    show(vplot(p1, p2))
else:
    output_file("/home/stats/output/cryptoasset_subreddit_subscribers.html", title="Major Cryptoassets Total Reddit Subscribers - Historical Growth")
    save(vplot(p1, p2))
    