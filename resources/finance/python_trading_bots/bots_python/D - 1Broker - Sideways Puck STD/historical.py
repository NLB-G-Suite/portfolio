#!/usr/bin/python
import API1brokerlib
import shared
try:
    import qt
except ImportError:
    shared.gui = False# qt not available

import csv
import json
import urllib2
import time
import datetime
import threading
import logging
import numpy as np
import talib
import math
import warnings

from win32com.client import Dispatch



#warnings.filterwarnings("ignore")

#from talib.abstract import *

def broker_update():
    broker = API1brokerlib.Connection(shared.API_KEY, 2)
    logging.debug("Updating 1broker info (overview).")
    shared.broker_fetch_count += 1
    overview = broker.account_overview()
    
    
    
    # check if failed
    if overview == False:
        logging.error("Error when updating 1broker info.")
        return False
    shared.overview = overview
     
    # calc P/L (DEPRECATED)
    shared.profitloss = int((float(overview['response']['positions_worth_btc'])-float(shared.MARGIN))*100000000)
    
    # remove positions data (in case of SL/TP)
    logging.debug("Clearing positions data.")
    for symbol in shared.SYMBOLS:
        shared.position[symbol] = (False, False)
    
    # check for open positions for all pairs
    logging.debug("Getting positions data.")
    for position in overview['response']['positions_open']:
        position_str = "Value: "+str(position['value'])+"; P/L: "+str(position['profit_loss'])
        if position['direction'] == "long":
            logging.debug(position['symbol']+": There is a long position open. "+position_str)
            shared.position[position['symbol']] = ("long", position['position_id'])
        elif position['direction'] == "short":
            logging.debug(position['symbol']+": There is a short position open. "+position_str)
            shared.position[position['symbol']] = ("short", position['position_id'])
        else:
            logging.debug(position['symbol']+": There is no position open. "+position_str)
            shared.position[position['symbol']] = (False, False)
    
    # get more data - balance, locked balance, total btc, open orders
    shared.balance = overview['response']['balance_btc']
    if shared.startup_balance == 0:
        shared.startup_balance = shared.balance
    shared.locked_balance = overview['response']['positions_worth_btc']
    shared.total_btc = overview['response']['net_worth_btc']
    
    # open orders
    if len(overview['response']['orders_open']) == 0:
        shared.orders = False
        logging.debug("No open orders.")
    else:
        shared.orders = True
        logging.debug("There is an order opened.")

    
    # get data for all symbols (bars, smas)
    for symbol in shared.SYMBOLS:
        # get bars
        logging.debug("Updating 1broker info (bars) for "+symbol+".")
        shared.broker_fetch_count += 1
        bars = broker.market_get_bars(symbol, shared.BARS_TIME,from_time=1284101485)
        # check if ok
        if bars == False:
            logging.error("Error when updating 1broker info (bars).")
            return False
        shared.bars[symbol] = bars
        
        # ##################################################################•
        # [{u'h': u'17.78', u'c': u'17.69', u'l': u'17.65', u'o': u'17.78', u'time': u'1449496800'},
                
        #Returns:
           
        #Array of OHLC (Open-, High-, Low-, Close-price) bars.
        #The field "time" is a string that contains the number of seconds since 1.1.1970. (UNIX epoch)
        #If there is no market data available for the specified range (see below), an empty array is returned.
        #Available resolution
        #Please expect that old historical data will be removed for performance reasons. However, you can safely assume that data is available for:
        #7 days	with 60s (1 minute) resolution
        #366 days	with 3600s (1 hour) resolution
        #forever	with 86400s (1 day) resolution
        # ##################################################################•    
        #try:
            #x=bars
        #except Exception as inst:
            #print "json.loads"
            #print type(inst)
            #print inst.args
        
        try:        
            f=csv.writer(open(symbol+"_1broker.csv","wb+"))
        except Exception as inst:
            print "writer"
            print type(inst)
            print inst.args
            
        try:
            numbars= len(bars['response'])
            print numbars
        except Exception as inst:
            print "len"
            print type(inst)
            print inst.args
        
    
        # H C O L
        try:
            for x in reversed(range(1,numbars+1)):
                f.writerow([datetime.datetime.fromtimestamp(float(bars['response'][-x]['time'])).strftime('%Y-%m-%d %H:%M:%S'),bars['response'][-x]['h'],bars['response'][-x]['c'],bars['response'][-x]['o'],bars['response'][-x]['l']])
        except Exception as inst:
            print "for"
            print type(inst)
            print inst.args
            
            
        # ///////////////////////////////////////////////
        
        # AQUI VOY A INTENTAR USAR PYWIN32 para importar en amibroker el CSV nuevo
        
        # ///////////////////////////////////////////////

        AMI = win32com.client.Dispatch("Broker.Application")
        
#1broker // custom99.format        
        
        kk=AMI.import(0,"C:/AmiBroker/Formats/custom99.format","custom99.format")
        kk2=AMI.RefreshAll
        
def main_thread():
    logging.info("Initializing main daemon.")
    while shared.running == True:
        try:
            broker_update()
            shared.running=False
        except:
            logging.error("Unknown error occurred.")
    logging.debug("Main thread exited cleanly.")

def main():
    try:
        # run all threads
        threading.Thread(target=main_thread).start()
        
        # start qt
        if shared.gui == True:
            ui = qt.UserInterface()
            ui.run()
            ui.ui_exit()
        else:
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        logging.warning("Keyboard interrupt")
        shared.running = False
        quit()

if __name__ == "__main__":
    main()
