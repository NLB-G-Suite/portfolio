#!/usr/bin/python
import API1brokerlib
import shared
try:
    import qt
except ImportError:
    shared.gui = False# qt not available

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
            for x in range(1+shared.DELAY,period+1+shared.DELAY):
                valor.append(bars['response'][-x]['c'])
            valor2=np.array(valor,dtype='float')
            
            return valor2
        
        def logbasek(valor,basek):
            return math.log(valor)/math.log(basek)
        
        def calculate_logbasek(basek,period):
            v=[]
            for x in reversed(range(1,period+1)):
                num1=bars['response'][-x]['c']
                num2=logbasek(float(num1),basek)
                valor.append(num2)
            v2=np.array(v,dtype='float')
            return v2
        
        def dx(a,b):
            try:
                k=(a-b)/((a+b)/2)
            except ZeroDivisionError:
                print "Division by zero!"
            else:
                return k
            
        
                
        
        def puckII(arr,per, pers,k, th,direc):
            retorno=False
            calc=0.000001
            try:
                LR1=talib.LINEARREG(arr,per)
            except Exception as inst:
                print "function puckII failed [LR1]"
                print type(inst)

            try:
                ST1=talib.STDDEV(arr,pers)                    
            except Exception as inst:
                print "function puckII failed [ST1]"
                print type(inst)

            try:                                                        
                calc=LR1[-1]+ST1[-1] * k
            except Exception as inst:
                print "function puckII failed [calc]"
                print type(inst)

            try:
                if direc==0 and calc > th:
                    retorno= True
                if direc==1 and calc < th:
                    retorno= True
            except Exception as inst:
                print "function puckII failed [retorno]"
                print type(inst)
            else:
                return retorno
        
        
        def marketfomoing(arr,per1,per2,th):
            try:
                LR1=talib.LINEARREG(arr,per1)
                LR2=talib.LINEARREG(arr,per2)
                DXResult=dx(LR1[-1],LR2[-1])
            except Exception as inst:
                print "function marketfomoing failed"
                print type(inst)
            else:
                return DXResult>th
        
        def marketcrashing(arr,per1,per2,th):
            try:
                LR1=talib.LINEARREG(arr,per1)
                LR2=talib.LINEARREG(arr,per2)
                DXResult=dx(LR1[-1],LR2[-1])
            except Exception as inst:
                print "function marketcrashing failed"
                print type(inst)
            else:
                return DXResult<th
            
        def writetoCSV():
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


        shared.ck=calculate_logbasek(shared.BASE,shared.NUMVELAS)
        shared.c1=puckII(shared.ck,shared.P1,shared.S1,shared.K1,shared.ThL,1)
        shared.c2=marketfomoing(shared.ck,shared.Fo1,shared.Fo2,shared.FT)
        shared.c3=puckII(shared.ck,shared.P2,shared.S2,shared.K2,shared.ThS,0)
        shared.c4=marketcrashing(shared.ck,shared.Cr1,shared.Cr2,shared.CT)        

        try:
            for x in reversed(range(1,100+1)):
                #logging.debug([datetime.datetime.fromtimestamp(float(bars['response'][-x]['time'])).strftime('%Y-%m-%d %H:%M:%S'),bars['response'][-x]['h'],bars['response'][-x]['c'],bars['response'][-x]['o'],bars['response'][-x]['l'],shared.ck[-x]])
                logging.debug([datetime.datetime.fromtimestamp(float(bars['response'][-x]['time'])).strftime('%Y-%m-%d %H:%M:%S'),shared.ck[-x],shared.c1[-x],shared.c2[-x],shared.c3[-x],shared.c4[-x]])
        except Exception as inst:
            print "displaydata"
            print type(inst)
            print inst.args
            
           
        
        
        #fecha=datetime.datetime.fromtimestamp(float(bars['response'][-x]['time'])).strftime('%Y-%m-%d %H:%M:%S')
        #logging.debug("ck:"+str(shared.ck))
        


        
def main_algo():
    # for all pairs
    for symbol in shared.SYMBOLS:
        logging.debug("Main algorithm started for "+symbol+".")
        
        try:
            if shared.c1:
                logging.debug("c1:"+str(shared.c1))
        except Exception as inst:
            print "shared.c1 falla"
            print type(inst)
            print inst.args
            
        try:                
            if shared.c2:
                logging.debug("c2:"+str(shared.c2))
        except Exception as inst:
            print "shared.c2 falla"
            print type(inst)
            print inst.args
                
        try:                
            if shared.c3:
                logging.debug("c3:"+str(shared.c3))
        except Exception as inst:
            print "shared.c3 falla"
            print type(inst)
            print inst.args

        try:                
            if shared.c4:
                logging.debug("c4:"+str(shared.c4))
        except Exception as inst:
            print "shared.c4 falla"
            print type(inst)
            print inst.args



            
        sig=0
        if (shared.c1 and not shared.c4) or shared.c2:
            logging.debug("BUY SIGNAL")
            sig=1
        else:
            if (shared.c3 and not shared.c2) or shared.c4:
                logging.debug("SELL SIGNAL")
                sig=-1
            else:
                logging.debug("NULL SIGNAL")
                sig=0
        
        

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
    logging.info("Initializing main daemon.")
    while shared.running == True:
        try:
            broker_update()
            main_algo()
            logging.debug("Sleeping for "+str(shared.MAIN_SLEEP_TIME)+" sec.")
            time.sleep(shared.MAIN_SLEEP_TIME)
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
