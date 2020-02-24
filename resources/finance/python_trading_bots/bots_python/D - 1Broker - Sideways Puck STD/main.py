import API1brokerlib
import shared
import common
import json
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import time
import datetime
import threading
import logging
import numpy as np
import talib

import math
#import warnings
import csv
#import win32com.client



def broker_update():
    broker = API1brokerlib.Connection("1bc840b53d889be84a08f912fbc3b6bc", 5)
    print("Updating 1broker info (overview).")
    shared.broker_fetch_count += 1
    overview = broker.account_overview()
    
    
    
    # check if failed
    if overview == False:
        print("Error when updating 1broker info.")
        return False
    shared.overview = overview
     
    # calc P/L (DEPRECATED)
    shared.profitloss = int((float(overview['response']['positions_worth_btc'])-float(shared.MARGIN))*100000000)
    
    # remove positions data (in case of SL/TP)
    print("Clearing positions data.")
    for symbol in shared.SYMBOLS:
        shared.position[symbol] = (False, False)
    
    # check for open positions for all pairs
    print("Getting positions data.")
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
        bars = broker.market_get_bars(symbol, shared.BARS_TIME)
        # check if ok
        if bars == False:
            logging.error("Error when updating 1broker info (bars).")
            return False
        shared.bars[symbol] = bars
        

        def calculate_sma(sma_range, delay=0):
            sma = 0
            for x in range(1+delay, sma_range+1+delay):
                sma += float(bars['response'][-x]['c'])
            return sma/sma_range


        def calculate_close(period):
            valor=[]
            for x in range(1,period+1):
                valor.append(bars['response'][-x]['c'])
            valor2=np.array(valor,dtype='float')
            
            return valor2

        
        def calculate_logbasek(basek,period):
            arr=np.random.random(period)
            for x in reversed(range(1,period+1)):
                np.append(arr, float(np.log(float(bars['response'][-x]['c']))/np.log(basek)))
            return arr           
    
    
        #BaseK=shared.BASE
        #Period=shared.NUMVELAS
        
        ## shared.ck=calculate_logbasek(BaseK,Period)
        #shared.ck=calculate_close(2000)
        #logging.debug("Here i show what i actually got into shared.ck after using numpy.log instead of mp.log =")
        #logging.debug(shared.ck)
        #logging.debug("Here i show talib.STDDEV")
        #print talib.STDDEV(shared.ck,3)
            
        
        #main.vZF4=common.zf4(shared.ck,shared.A1,shared.LRp1,shared.FL1,shared.STDp1,shared.B1,shared.LRp2,shared.FL2,shared.STDp2,shared.C1,shared.LRp3,shared.FL3,shared.STDp3,shared.D1,shared.LRp4,shared.FL4,shared.STDp4)
        #logging.debug("Here i show vZF4")
        #print main.vZF4
     

        common.writetoCSV(symbol,bars)   #time, h, c, o, l

            

        
def main_algo():
    # for all pairs
    for symbol in shared.SYMBOLS:
        logging.debug("Main algorithm started for "+symbol+".")
        logging.debug("Actual Model =>"+shared.ALGO)
        sig=0
        if shared.ALGO=="ZF4":
            if main.vZF4[-1]>shared.Th1:
                logging.debug("BUY SIGNAL")
                sig= 1
            if main.vZF4[-1]<shared.Th2:
                logging.debug("SELL SIGNAL")
                sig=-1
        
        if shared.ALGO=="P3F2":
            c1=common.puckII(shared.ck,shared.P1,shared.S1,shared.K1,shared.ThL,1)
            c2=common.marketfomoing(shared.ck,shared.Fo1,shared.Fo2,shared.FT)
            c3=common.puckII(shared.ck,shared.P2,shared.S2,shared.K2,shared.ThS,0)
            c4=common.marketcrashing(shared.ck,shared.Cr1,shared.Cr2,shared.CT)                 
            sig= 0
            if (c1 and not c4) or c2:
                logging.debug("BUY SIGNAL")
                sig= 1
            else:
                if (c3 and not c2) or c4:
                    logging.debug("SELL SIGNAL")
                    sig=-1
                else:
                    logging.debug("NULL SIGNAL")
                    sig= 0

        broker = API1brokerlib.Connection(shared.API_KEY, 1)

        if sig == -1:
            #close long position, if open
            if shared.position[symbol][0] == "long":
                broker.position_edit(int(shared.position[symbol][1]), market_close="true")
                logging.info(symbol+": Closed long position: cross. P/L: "+str(shared.profitloss))
                shared.position[symbol] = (False, False)# reset position info; I think we dont need any of this anymore
        if sig == 1:
            # close short position, if open
            if shared.position[symbol][0] == "short":
                broker.position_edit(int(shared.position[symbol][1]), market_close="true")
                logging.info(symbol+": Closed short position: cross. P/L: "+str(shared.profitloss))
                shared.position[symbol] = (False, False)
        if sig == -1:
            # open short position, if not opened and if no open orders
            if shared.position[symbol][0] == False and shared.orders == False:
                rate = float(shared.bars[symbol]['response'][-1]['c'])
                stop_loss = rate+rate*shared.STOP_LOSS_PERCENT/100
                take_profit = rate-rate*shared.TAKE_PROFIT_PERCENT/100
                #broker.order_create(symbol, shared.MARGIN, "short", shared.LEVERAGE, "Market", stop_loss=float(stop_loss), take_profit=float(take_profit))
                broker.order_create(symbol, shared.MARGIN, "short", shared.LEVERAGE, "Market")
                logging.info(symbol+": Opened short position, SL: "+str(stop_loss)+", TP: "+str(take_profit))
                shared.position[symbol] = ("short", True)
        if sig == 1:
            # open long position, if not opened and if no open orders
            if shared.position[symbol][0] == False and shared.orders == False:
                rate = float(shared.bars[symbol]['response'][-1]['c'])
                stop_loss = rate-rate*shared.STOP_LOSS_PERCENT/100
                take_profit = rate+rate*shared.TAKE_PROFIT_PERCENT/100
                #broker.order_create(symbol, shared.MARGIN, "long", shared.LEVERAGE, "Market", stop_loss=float(stop_loss), take_profit=float(take_profit))
                broker.order_create(symbol, shared.MARGIN, "long", shared.LEVERAGE, "Market")
                logging.info(symbol+": Opened long position, SL: "+str(stop_loss)+", TP: "+str(take_profit))
                shared.position[symbol] = ("long", True)
        if sig == 0:
            # do nothing
            logging.debug("No crosses - doing nothing.")

def main_thread():
    print("Initializing main daemon.")
    while shared.running == True:
        broker_update()
        #main_algo()
        #logging.debug("Sleeping for "+str(shared.MAIN_SLEEP_TIME)+" sec.")
        shared.running=False
        time.sleep(shared.MAIN_SLEEP_TIME)
            #shared.running=False
        #except Exception as inst:
            #print "main_thread"
            #print type(inst)
            #print inst.args
    
    #broker_update()
    
    logging.debug("Main thread exited cleanly.")

def main():
    main_thread()
    #try:
        ## run all threads
        #threading.Thread(target=main_thread).start()
        
        ## start qt
        #if shared.gui == True:
            #ui = qt.UserInterface()
            #ui.run()
            #ui.ui_exit()
        #else:
            #while True:
                #time.sleep(1)
    #except KeyboardInterrupt:
        #logging.warning("Keyboard interrupt")
        #shared.running = False
        #quit()

if __name__ == "__main__":
    main()
