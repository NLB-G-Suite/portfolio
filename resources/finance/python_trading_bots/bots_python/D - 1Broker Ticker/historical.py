#!/usr/bin/python
import API1brokerlib
import shared
try:
    import qt
except ImportError:
    shared.gui = False# qt not available

import csv
import json
import sys

import time
import datetime
import threading
import logging
import numpy as np
import talib
import math
import warnings


if sys.version_info[0] == 3:
    from urllib.request import Request, urlopen
    from urllib.parse import urlencode
else:
    from urllib2 import Request, urlopen
    from urllib import urlencode



def broker_update():
    broker = API1brokerlib.Connection(shared.API_KEY, 2)
    print("Updating 1broker info for following instruments:")
    print(shared.SYMBOLS)
    shared.broker_fetch_count += 1
    overview = broker.account_overview()
    
    # check if failed
    if overview == False:
        print("Error when updating 1broker info.")
        return False
    shared.overview = overview
     
    
    for symbol in shared.SYMBOLS:
        # get bars
        print("Updating 1broker info (bars) for %s. [%s seconds]" % (symbol, shared.BARS_TIME) )
        shared.broker_fetch_count += 1
        bars = broker.market_get_bars(symbol, shared.BARS_TIME,from_time=1284101485)
        numbars= len(bars['response'])                    
        print ("Total rows imported in %s = %s " % (symbol,numbars))
        
        # check if ok
        if bars == False:
            print("Error when updating 1broker info (bars).")
            return False
        shared.bars[symbol] = bars
       
        try:        
            f=csv.writer(open(symbol+"_1broker.csv","w+", newline=''),delimiter=';',dialect='excel')
            # H C O L
            for x in reversed(range(1,numbars+1)):
                f.writerow([datetime.datetime.fromtimestamp(float(bars['response'][-x]['time'])).strftime('%Y-%m-%d %H:%M'),bars['response'][-x]['h'],bars['response'][-x]['c'],bars['response'][-x]['o'],bars['response'][-x]['l']])
        except Exception as inst:
            print ("writer. Maybe you have the excel file opened??")
            print (type(inst))
            print (inst.args)

        
def main_thread():
    while shared.running == True:
        #try:
        broker_update()
        shared.running = False
        #except:
        #    print("Unknown error occurred")
    print("Main thread exited cleanly.")


if __name__ == "__main__":
    main_thread()
