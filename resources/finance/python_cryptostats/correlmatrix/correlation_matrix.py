
import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import sys
from datetime import datetime


if sys.platform == 'win32':
    candlesize="15min"
else:
    print(str(sys.argv))
    candlesize=str(sys.argv[1])
    print(candlesize)
    if candlesize=="":
        candlesize="5min"
        print("No candlesize provided. Using 5min")


# These settings modify the way  pandas prints data stored in a DataFrame.
# In particular when we use print(data_frame_reference); function - all
#  column values of the frame will be printed in the same  row instead of
# being automatically wrapped after 6 columns by default. This will be
# for looking at our data at the end of the program.
pd.set_option('display.height', 1000)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


# Using glob library to create a list of file names using regular expression.
if sys.platform == 'win32':
    datafiles= glob.glob("c://teleferi//CSV_Tickers//??_BTC_*.csv")
else:
    datafiles= glob.glob("/home/CSV_Tickers/??_BTC_*.csv")
print(datafiles)
# Create an empty python dictionary which will contain currency pairs' data.
# Keys will be currency pair names, and values- 'pandas' data frames with 
# close prices read from the files.
dataframes = dict()
# In the following loop we'll read each file into a pandas data frame and 
# store them in the 'dataframes' dictionary.
# for each file...
for f in sorted(datafiles):
    #parse currency pair name from the file name
    pair_name = "BTC"+f.split(os.path.sep)[-1].split('_')[2].split('.')[0].upper()
    # Using read_csv function read file into a DataFrame 'df'.
    print("%s    ->  %s" % (pair_name,f))
    print(pair_name)
    # Notice that we are reading only two columns from each file: 'date', and 'close'. 
    # We'll be using 'date' to index each record in data frame (think of it a a primary
    # key value for the record) , and the close price will be used to  calculate correlations. 
    
    #df = pd.read_csv(f, sep=',', header=0, index_col=[0], usecols=[0, 1])
    
    df = pd.read_csv(f, sep=',', header=0, index_col=[0],error_bad_lines=False)
    #print("finished reading csv")
    #print(df.head())
    #df.index = pd.to_datetime(df.index, infer_datetime_format=True)
    cols=df.columns.tolist()
    print(cols)
    
    #La salida de Poloniex csv tiene formato: Date+OCHLV y queremos Date+OHLCV luego
    #                                              01234                 02314
    #===============================================================================
    # La salida de Poloniex es Date + OCHLV
    # La salida de Okcoin es Date + OCHLV    
    
    df=df[[1]]
    cols=df.columns.tolist()
    print(cols)
    
    if pair_name=='BTCCNY':
        # 2013/07/01 11:15,584.53,583.81,584.66,583.17,15.633
        df.index = pd.to_datetime(df.index, format='%Y/%m/%d %H:%M')  # <----- esta era la solucion
        df.head()
        dfXXX=df.resample(candlesize).ohlc().bfill().ffill()
    else:
        #19/01/2014 07:05,5.0e-5,5.0e-5,5.0e-5,5.0e-5,0
        df.index = pd.to_datetime(df.index, format='%d/%m/%Y %H:%M')  # <----- esta era la solucion
        df.head()
        dfXXX=df.resample(candlesize).ohlc().bfill().ffill()
    
    print(dfXXX.ix[:,[3]].head())                                 #<--------- esto
    # Rename 'close' column the the currency pair name pair.
    # This will help us identify each pair's close price below when we join all 
    # data frames into a single fame.
    df=dfXXX.ix[:,[3]]                                           # <--------- esto
    df.columns = [pair_name]

    # Read each of files into a pandas data frame.
    dataframes[pair_name] = df
    #print(df.columns)
    


# In this section we'll join all data frames create above into a single 'final_df' 
# data frame. This data frame will contain a single 'date' column, and 1 column 
# for each currency pair containing that pair's close prices.
final_df = None
for k,v in dataframes.items():  # MIO: python 3 renamed dict.iteritems a  dict.items
    if (final_df is None):
        final_df = v
    else:
        # Panda's join operation is similar to an SQL join. In this case
        # we are using a 'left' join.
        #http://pandas.pydata.org/pandas-docs/stable/merging.html
        final_df = final_df.join(v, how='left')

final_df=final_df.sort_index(axis=1)

#final_df=final_df.TimeGrouper(key=final_df.columns[0],freq='1H')

#print("--------------- FINAL DATA FRAME ---------------")
#print(final_df.head(10))

# And now.. the "hard" part- calculating correlations between pairs.
# DataFrames corr() function calculates pairwise correlations using specified 
# algorithm: 'peason, 'kendall', and 'spearman' are supported.
# Correlations are returned in a new DataFrame instance (corr_df below).
corr_df = final_df.corr(method='pearson')
#print("--------------- CORRELATIONS ---------------")
#print(corr_df.head(len(dataframes)))

print("--------------- CREATE A HEATMAP ---------------")
# Create a mask to display only the lower triangle of the matrix (since it's mirrored around its 
# top-left to bottom-right diagonal).
mask = np.zeros_like(corr_df)
mask[np.triu_indices_from(mask)] = True
# Create the heatmap using seaborn library. 
# List if colormaps (parameter 'cmap') is available here: http://matplotlib.org/examples/color/colormaps_reference.html
#seaborn.heatmap(corr_df, cmap='RdYlGn_r', vmax=1.0, vmin=-1.0 , mask = mask, linewidths=2.5, robust=True)
#seaborn.heatmap(corr_df, cmap='GyRd_r', vmax=1.0, vmin=-1.0 , mask = mask, linewidths=0.5)
seaborn.heatmap(corr_df, cmap='RdGy', vmax=1.0, vmin=-1.0 , linewidths=0.5)
seaborn.set(font_scale=0.8)
plt.subplots_adjust(left=0.15,bottom=0.19, right=1.00, top=0.92)
plt.suptitle("Bitcoin Markets Correlation Matrix ("+candlesize+") Last Update: "+str(datetime.now().strftime('%Y-%m-%d %H:%M')))
# Show the plot we reorient the labels for each column and row to make them easier to read.
plt.yticks(rotation=0) 
plt.xticks(rotation=90) 
#plt.show()




if sys.platform == 'win32':
    #plt.savefig("alt_correl_"+candlesize+".jpg")
    plt.show()
    
else:
    plt.savefig("/home/stats/output/alt_correl_"+candlesize+".jpg")