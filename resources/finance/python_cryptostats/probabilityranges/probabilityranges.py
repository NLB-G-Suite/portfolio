import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates  as pltdates

import seaborn
import sys
import datetime 
import talib
import scipy
from natsort import natsorted,ns,index_natsorted,order_by_index

import matplotlib as mpl
mpl.rcParams['lines.linewidth']=1.0
mpl.rcParams.update({'font.size': 8})


SCALE=10000000
DEBUG_MAIN_ALGO=True


def replace_nan(num):
    if not numpy.nan_to_num(num):
        return 1

def calculate_close(bars,period):
    valor=[]
    for x in reversed(range(1,period+1)):
        valor.append(SCALE * bars[-x])
    valor2=np.array(valor, dtype='f8')
    return valor2  

def zscore(data1,data2,LRp):
    arr1=calculate_close(data1,LRp+1)
    arr2=calculate_close(data2,LRp+1)
    valor=(arr1[-1]-talib.LINEARREG(arr2,LRp)[-1])/talib.STDDEV(arr2,LRp)[-1]
    if DEBUG_MAIN_ALGO==True:
        print("zscore[%s] result = %s and its pvalue is %s percent" % (LRp,valor,pvalue(valor)))
    return valor

def pvalue(zscore_value):
    import scipy
    #p_value = format(float(100*scipy.stats.norm.sf(abs(zscore_value))*2),'.2f') #twosided
    p_value = int(100*scipy.stats.norm.sf(abs(zscore_value))*2)
    return p_value

asset=""
candlesize=""

if sys.platform == 'win32':
    asset="CNY"
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
    


print("#########################")
print("        STARTING")
print("#########################")

dataframe=dict()

ztable=[]
ptable=[]

if sys.platform == 'win32':
    asset="cny"
    datafiles= glob.glob("c://CSV_Tickers//??_btc_"+asset+"*.csv")
else:
    datafiles= glob.glob("/home/CSV_Tickers/??_BTC_"+asset+".csv")   
    

print("actual asset: %s  | datafile: %s | candlesize: %s " % (asset, datafiles, candlesize))    


for f in sorted(datafiles):
    #erasing at beginning
    #dataframe=None
    

    
    pair_name = f.split(os.path.sep)[-1].split('_')[2].split('.')[0]
    df = pd.read_csv(f, sep=',', header=0, index_col=[0],error_bad_lines=False)
    df=df[[1]] 
    
    print("number of rows before adjusting date")
    print(len(df))
    print(df.head())
    
    if asset=='CNY' or asset == 'cny':
        df.index = pd.to_datetime(df.index, format='%Y/%m/%d %H:%M')  # <----- esta era la solucion
        df.head()
        dfXXX=df.resample(candlesize).ohlc().bfill().ffill()
        print("esta entrando aqui??")
        print(len(dfXXX))
    else:
        df.index = pd.to_datetime(df.index, format='%d/%m/%Y %H:%M')  # <----- esta era la solucion
        df.head()
        dfXXX=df.resample(candlesize).ohlc().bfill().ffill()    





    df=dfXXX.ix[:,[3]]                
    data=df.ix[:,0]

    #print("number of rows AFTER adjusting date")
    #print(9999)
    #print(data.head())

    side_of_square=30
    
    pr_max=+ 33+1
    pr_min=-(33-1)
    jump1=int((pr_max-pr_min)/side_of_square)
    print("len(data)=%s, pr_min=%s, pr_max=%s, jump1=%s" % (len(data),pr_min, pr_max, jump1))
    
    zp_max=int(len(df)/10-10)  #8640+1
    jump2=int((zp_max-1)/(1+side_of_square))
    zp_min=jump2
    print("zp_min=%s, zp_max=%s, jump2=%s" % (zp_min, zp_max, jump2))

    for probability_range in range(pr_min,pr_max,jump1):
        print("****************************************")
        print("probability_range=%s" % probability_range)
        print("****************************************")
        ptable=[]
        
        for zscore_periods in range(zp_max, jump2,-jump2):
            z=zscore(data*(1 + probability_range/100),data,zscore_periods)
            ptable.append([str(zscore_periods)+"_Periods",pvalue(z)])
            DF_ptable=pd.DataFrame(ptable)
            

        IDF_ptable=DF_ptable.set_index(list(DF_ptable.columns[[0]]))
        
        if probability_range>0:
            simbolo="+"
        if probability_range<0:
            simbolo="-"
        if len(str(abs(probability_range)))<2:
            simbolo=simbolo+"0"+str(abs(probability_range))
        else:
            simbolo=simbolo+str(abs(probability_range))
        if probability_range==0:
            cadena="Actual Price"
        else:
            cadena="Price"+simbolo+"%"
        #cadena=str(data[-1]*(1 + probability_range/100))+" "+pair_name+" ["+cadena+"]"
        cadena=float(data[-1]*(1 + probability_range/100))
        #print(cadena)
        #print(simbolo)
        
        IDF_ptable=IDF_ptable.ix[:,[1]]
        IDF_ptable.columns=[cadena]  
        
        dataframe[cadena]=IDF_ptable
    
    final_df=None
    for k,v in dataframe.items():
        if (final_df is None):
            final_df=v
        else:
            final_df=final_df.join(v,how='left')
    
    final_df=final_df.sort_index(axis=1,ascending=False)
    
    new_index=index_natsorted(final_df.index)
    print(new_index)
    reversed_new_index=new_index[::-1]
    print(reversed_new_index)
    
    #final_df.reindex(index=natsorted(final_df.index,reverse=False))
    
    final_df.reindex(index=order_by_index(final_df.index,reversed_new_index))
    
    
    
    
    #final_df=final_df.sort_index(axis=0,ascending=True)
    
    print("final_df--------------------------")
    
    
    seaborn.heatmap(final_df.T, cmap='RdGy', vmax=100.0, vmin=0.0 , linewidths=0.5)
    plt.suptitle("BTC"+str(pair_name)+"-"+str(candlesize)+" ; Price Range Probabilities ; Updated: "+str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M')))
    plt.subplots_adjust(left=0.18,bottom=0.21, right=0.98, top=0.90)
    plt.yticks(rotation=0) 
    plt.xticks(rotation=90)
    


    #def update_ylabels(ax):
        #labels = ax.ylabel
        #print(labels)
        #for k in range(0, len(ax.yticks())):
            
            #ax.ylabel = format(ax.ylabel, ',.0f')
    
    #update_ylabels(plt)
    #update_xlabels(ax2)
    
    
    
    if sys.platform == 'win32':
        plt.show()
        #plt.savefig("probability_ranges_"+pair_name+".jpg")
    else:
        plt.savefig("/home/stats/output/probability_ranges_"+pair_name+"_"+str(candlesize)+".jpg")