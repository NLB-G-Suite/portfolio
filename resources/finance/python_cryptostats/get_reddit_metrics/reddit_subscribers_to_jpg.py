# ----------------------------------
# subreddit subscribers csv to graph
# ----------------------------------

import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn
import sys
from datetime import datetime

import matplotlib as mpl
mpl.rcParams['lines.linewidth']=0.65

def create_total_subscribers_chart(dx,logscale=False):
    fig=plt.figure(figsize=(12,6),dpi=100)
    ax=fig.add_subplot(111)
    plt.plot_date(dx.index[:],dx[:],'-')
    
    if logscale==True:
        ax.set_yscale('log')
        logtext="(Log Scale)"
    else:
        logtext=""
    plt.suptitle("Total Subscribers to Major Cryptofinance Subreddits - Updated:"+str(datetime.now().strftime('%Y-%m-%d %H:%M'))+" "+str(logtext))
    
    plt.subplots_adjust(left=0.05,bottom=0.16, right=0.84, top=0.91)
    
    for k in range(0,len(dx.columns)):
        mm=dx[[k]]
        
        if k==0:
            dates1=mm.index[:]
        values1=mm[:]
        ax=fig.add_subplot()
        
        if k==0:
            plt.plot_date(dates1,values1,'-')
        plt.plot_date(dates1,values1,'-',label=dx.columns[k])
        
        plt.yticks(rotation=0) 
        plt.xticks(rotation=90)    
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5),)

    if logscale==False:
        filename="total_subscribers_crypto_subreddits_linear.jpg"
    else:
        filename="total_subscribers_crypto_subreddits_log.jpg"
    if sys.platform == 'win32':
        plt.savefig(filename)
    else:
        plt.savefig("/home/stats/output/"+filename) 

print("#########################")
print("        STARTING")
print("#########################")

dataframes=dict()

if sys.platform == 'win32':
    datafiles= glob.glob("c://act2//@TOOLS//get_reddit_metrics//outfile_total-subscribers_*")
else:
    datafiles= glob.glob("/home/stats/get_reddit_metrics/output/outfile_total-subscribers_*")    
    
for f in sorted(datafiles):
    print(f)
    pair_name = f.split(os.path.sep)[-1].split('_')[2]
    print(f.split(os.path.sep)[-1].split('_')[2])
    print("")
    print("Reading %s => %s CSV" % (f,pair_name))
            
    df = pd.read_csv(f, sep=',', header=0, index_col=[0],error_bad_lines=False)
    df=df.ix[:,[0]]
    df.columns=[pair_name]
    dataframes[pair_name]=df
    print(df)
    
final_df = None
for k,v in dataframes.items():  # MIO: python 3 renamed dict.iteritems a  dict.items
    if (final_df is None):
        final_df = v
    else:
        ## Panda's join operation is similar to an SQL join. In this case
        ## we are using a 'left' join.
        ##http://pandas.pydata.org/pandas-docs/stable/merging.html
        final_df = final_df.join(v, how='left')

create_total_subscribers_chart(final_df,logscale=True)
create_total_subscribers_chart(final_df,logscale=False)

