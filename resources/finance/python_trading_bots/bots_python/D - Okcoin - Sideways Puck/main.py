#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8

import json
import shared
import common
import talib
import math
import random
import numpy as np

import time

from OkcoinSpotAPI import OKCoinSpot
from OkcoinFutureAPI import OKCoinFuture

apikey='011eaa4f-4a14-4ba3-93df-36f86e3e7ee9'
secretkey='725F9EDBCE71326C3A230732F0C24C95'

okcoinRESTURL = 'www.okcoin.cn'   #请求注意：国内账号需要 修改为 www.okcoin.cn  

okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)

running=True





def return_balance():
    uinfo=okcoinSpot.userinfo()
    loadinfo=json.loads(uinfo)       
    return loadinfo

def return_ticker():
    ticker=okcoinSpot.ticker('btc_cny')
    return float(ticker['ticker']['buy'])

def broker_update():

    #///////////////////////////////////////////////    
    #        Date;Open;Close;High;Low;Volume
    #///////////////////////////////////////////////    
    from numpy import genfromtxt
    
    bars=genfromtxt('C:/AMIBROKER/Formulas/CSV_Tickers/OK-BTCCNY-15m.csv',delimiter=';',dtype=[('d','S16'),('o','<f8'),('c','<f8'),('h','<f8'),('l','<f8'),('v','<f8')],usemask=False)
            
    try:
        balance=return_balance()
    
        print("------------------------------------------")
        print("Balance CNY: %s " % balance['info']['funds']['free']['cny'])
        print("Balance BTC: %s " % balance['info']['funds']['free']['btc'])
        print("------------------------------------------")
    except:
        print("ERROR: Something failed when tried to get the user balance")
 
    try:
        print("Actual BTCCNY Value: %s - %s" % (time.strftime("%Y-%m-%d %H:%M:%S") , return_ticker() ))
    except:
        print("ERROR: Something failed when tried to get last TICK info")

    print(bars['c'])
    shared.ck=bars['c']
    
    shared.vSidewaysPuck=common.SidewaysPuck(shared.ck,shared.P1,shared.P2,shared.Th1, shared.Th2, 2)    
    print(shared.vSidewaysPuck)
    

def main_algo():
    # for all pairs
    
    for symbol in shared.SYMBOLS:
        
        shared.TICK=shared.TICK+1
        print("   ")
        print("****************************")
        print("  T I C K = %s" % (shared.TICK))
        print("****************************")
        print("   ")
        print("=================== ALGO: PRECHECKS ====================")
        
        print("Main algorithm started for %s " % shared.PAIR)
        print("Actual Model => %s " % shared.ALGO)
        shared.sig=0
        
        
        try:
            OpenOrders=okcoinSpot.orderinfo('btc_cny','-1')
            print("Displaying list of opened orders at this moment")
            print(OpenOrders)
            loadOrders=json.loads(OpenOrders)
            numOrders= len(loadOrders['orders'])        
            print("There are %s opened orders" % (numOrders))
        except:
            print("ERROR: I Couldn't get the list of opened orders")
        
        try:
            if numOrders>0 and shared.TICK==1:  # HERE WE CLOSE ALL ORDERS FROM PREVIOUS EXECUTIONS OF THE BOT
                print("We have some orders BUT Algorithm Just started. Closing all open orders from previous sessions")
                try:
                    for x in reversed(range(1,numOrders+1)):
                        actual=str(loadOrders['orders'][-x]['order_id'])
                        print("We select an open order: %s" % (actual))
                        print("Closing order %s" % (actual))
                        print(okcoinSpot.cancelOrder('btc_cny',actual))
                    print("Ended closing orders")
                except:
                    print("ERROR: At bot start, when cancelling orders from other sessions something failed")
        except:
            print("ERROR: I could not check the list of orders from previous sessions and cancel them")


        numTimeouts=len(shared.TimeoutList1)
        if numTimeouts > 0 and shared.TICK > 1: # HERE WE CHECK FROM ALL THE OPEN ORDERS IF ANY HAS TIMEOUT OR NOT YET
            print("------------------------------------------------------")
            print("Checking if there are some orders to close due timeout")            
            print("This is the list of buy orders to check:")
            numTimeouts=len(shared.TimeoutList1)
            for x in reversed(range(1,numTimeouts+1)):
                print(shared.TimeoutList1[-x])
                if (shared.TimeoutList3[-x]=='buy' and ( shared.TICK - shared.TimeoutList2[-x] > shared.hb)):
                    try:
                        actual=shared.TimeoutList1[-x]
                        print(okcoinSpot.cancelOrder('btc_cny',actual))
                        print("AFTER DEL (Buy) NumTimeoutList1=%s | NumTimeoutList2=%s | NumTimeoutList3=%s" % (len(shared.TimeoutList1),len(shared.TimeoutList2),len(shared.TimeoutList3)))
                        del shared.TimeoutList1[-x]
                        del shared.TimeoutList2[-x]
                        del shared.TimeoutList3[-x]
                        print("AFTER DEL (Buy) NumTimeoutList1=%s | NumTimeoutList2=%s | NumTimeoutList3=%s" % (len(shared.TimeoutList1),len(shared.TimeoutList2),len(shared.TimeoutList3)))
                    except:
                        print("ERROR: Tried to cancel a buy order that reached the timeout but something failed")
            print("This is the list of sell orders to check:")
            numTimeouts=len(shared.TimeoutList1)
            for x in reversed(range(1,numTimeouts+1)):
                print(shared.TimeoutList1[-x])
                if (shared.TimeoutList3[-x]=='sell' and ( shared.TICK - shared.TimeoutList2[-x] > shared.hs)):
                    try:
                        actual=shared.TimeoutList1[-x]
                        print(okcoinSpot.cancelOrder('btc_cny',actual))
                        print("BEFORE DEL (Sell) NumTimeoutList1=%s | NumTimeoutList2=%s | NumTimeoutList3=%s" % (len(shared.TimeoutList1),len(shared.TimeoutList2),len(shared.TimeoutList3)))
                        del shared.TimeoutList1[-x]
                        del shared.TimeoutList2[-x]
                        del shared.TimeoutList3[-x]
                        print("AFTER DEL (Sell) NumTimeoutList1=%s | NumTimeoutList2=%s | NumTimeoutList3=%s" % (len(shared.TimeoutList1),len(shared.TimeoutList2),len(shared.TimeoutList3)))
                    except:
                        print("ERROR: Tried to cancel a sell order that reached the timeout but something failed")
                    
            

        print("=================== ALGO: MAIN LOGIC ===================")
        print("Checking buy/sell algorithm to see if we can create new orders")

        if shared.ALGO=="SIDEWAYS PUCK":
            if shared.vSidewaysPuck:
                print("Model vSidewaysPuck = %s wants to operate now" % (shared.vSidewaysPuck))
                print("Creating New Buy")
                try:
                    balance=return_balance()
                    assets=float(balance['info']['funds']['free']['btc'])
                    curr=float(balance['info']['funds']['free']['cny'])    
                except:
                    print("ERROR: Tried to get the balance from the exchange but something failed")
                
                try:
                    ticker=return_ticker()
                    shared.price=ticker            
                except:
                    print("ERROR: Tried to get the ticker data from the exchange but something failed")
                
                if float(curr)/(float(shared.price)*float(shared.KL)) > 0.02:
                    print("There is enough money to buy. Placing an order")
                    try:
                        neworder=okcoinSpot.trade('btc_cny', 'buy' , shared.price * shared.KL , 0.02 )
                        print("Adding the order to the timeout list")
                        actual=json.loads(neworder)
                        shared.TimeoutList1.append(actual['order_id'])
                        shared.TimeoutList2.append(shared.TICK)
                        shared.TimeoutList3.append('buy')
                        print(shared.TimeoutList1)
                        print(shared.TimeoutList2)
                        print(shared.TimeoutList3)
                    except:
                        print("ERROR: Tried to place a buy order but something failed")
                        print("curr=%s / (shared.price=%s * shared.KL=%s)" % (curr, shared.price,shared.KL))
                else:
                    print("Not enough money to buy")
                
                if assets > 0.02:
                    print("There are enough assets to sell. Placing an order")
                    try:
                        neworder=okcoinSpot.trade('btc_cny', 'sell' , shared.price * shared.KH , 0.02 )
                        print("Adding the order to the timeout list")
                        actual=json.loads(neworder)
                        shared.TimeoutList1.append(actual['order_id'])
                        shared.TimeoutList2.append(shared.TICK)
                        shared.TimeoutList3.append('sell')
                        print(shared.TimeoutList1)
                        print(shared.TimeoutList2)
                        print(shared.TimeoutList3)
                    except:
                        print("ERROR: Tried to place a sell order but something failed")
                else:
                    print("Not enough assets to sell")
            else:
                print("Model does not want to operate at this moment:")
                print("Ang1=%s | and should be lower than %s" % (abs(common.linregangle(shared.ck,shared.P1)[-2]), shared.Th1))
                print("Ang2=%s | and should be lower than %s" % (abs(common.linregangle(shared.ck,shared.P2)[-2]), shared.Th2))




        try:
            balance=return_balance()
            ticker=return_ticker()
            assets1=float(balance['info']['funds']['free']['btc'])                    
            curr1=float(balance['info']['funds']['free']['cny'])    
            price1=float(ticker)        
        except:
            print("ERROR: There was a problem when retrieving the balance/ticker data from the exchange")
        
      


def main_thread():
    print("Initializing main daemon.")
    while running == True:
        broker_update()
        main_algo()
        print("Tick processing ended. Waiting for next tick. Waiting %s Minutes" % (shared.FRECUENCIA_MINUTOS))
        time.sleep(shared.MAIN_SLEEP_TIME)
        

    


    


if __name__ == "__main__":
    main_thread()