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
import csv
import os

import time

from OkcoinSpotAPI import OKCoinSpot
from OkcoinFutureAPI import OKCoinFuture

from random import randint

#Guayaba
apikey= '3cdfe4e2-6503-4f31-aa23-75f3f5128a23'
secretkey= '75E3C73F1ACABA51C3D410A21EBE3F31'


okcoinRESTURL = 'www.okcoin.cn'   #请求注意：国内账号需要 修改为 www.okcoin.cn  

okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)

running=True

def return_balance():
    uinfo=okcoinSpot.userinfo()
    loadinfo=json.loads(uinfo)       
    return loadinfo

def return_ticker():
    ticker=okcoinSpot.ticker('btc_cny')
    if shared.CheckCode==False:
        ret=float(ticker['ticker']['buy'])
    else:
        ret=float(ticker['ticker']['buy'])        
    return ret

def broker_update():

    #///////////////////////////////////////////////    
    #        Date;Open;Close;High;Low;Volume
    #///////////////////////////////////////////////    
    from numpy import genfromtxt
    if os.name=='nt':
        bars=genfromtxt('c:/Amibroker/Formulas/CSV_Tickers/OK-BTCCNY-15m.csv',delimiter=';',dtype=[('d','S16'),('o','<f8'),('c','<f8'),('h','<f8'),('l','<f8'),('v','<f8')],usemask=False)        
    else:
        bars=genfromtxt('/home/CSV_Tickers/OK-BTCCNY-15m.csv',delimiter=';',dtype=[('d','S16'),('o','<f8'),('c','<f8'),('h','<f8'),('l','<f8'),('v','<f8')],usemask=False)        

        
    shared.ck=bars['c']

    shared.TICK=shared.TICK+1
    if shared.CheckCode==False:
        print("   ")
        print("********************************************************************************************************************")
        print("       T I C K = %s" % (shared.TICK))
        print("   ")
        print("     %s " % shared.ALGO)
        print("********************************************************************************************************************")
    
   # try:
    ticker=return_ticker()
    shared.price=ticker            
    balance=return_balance()     
    if shared.CheckCode==False:
        print("Balance CNY: %s " % balance['info']['funds']['free']['cny'])
        print("Balance BTC: %s " % balance['info']['funds']['free']['btc'])
        print("--------------------------------------------------------------------------------------------------------------------")
    #except:
    #    print("ERROR: Something failed when tried to get the user ticker/balance")
        
    try:
        if shared.CheckCode==False:
            print("Exporting model performance stats to /home/CSV_Tickers/starts_Okcoin_Sideways_Puck_STD.csv")
            f=csv.writer(open("/home/CSV_Tickers/stats_Okcoin_Sideways_Puck_STD.csv","a+"),delimiter=';')
            f.writerow([time.strftime("%Y-%m-%d %H:%M") , ticker, balance['info']['funds']['asset']['net'], float(balance['info']['funds']['asset']['net'])/float(ticker), balance['info']['funds']['asset']['total']])
    except:
        print("ERROR: Could not export performance stats to file. Have you got the CSV file opened?")

    shared.vSidewaysPuckSTD=common.SidewaysPuckSTD(shared.ck,shared.A,shared.Th, shared.lag)    
    
def main_algo():
    for symbol in shared.SYMBOLS:
        shared.sig=0
        # Closing all orders still open from previous sessions of execution of the bot
        if shared.TICK==1 :  
            try:
                OpenOrders=okcoinSpot.orderinfo('btc_cny','-1')
                loadOrders=json.loads(OpenOrders)
                numOrders= len(loadOrders['orders'])        
                if shared.CheckCode==False:
                    print("Just Started. We have %s orders. Closing all open orders from previous sessions" % numOrders)
                for x in reversed(range(1,numOrders+1)):
                    actual=str(loadOrders['orders'][-x]['order_id'])
                    if shared.CheckCode==False:
                        print("Closing order %s" % (actual))
                        print(okcoinSpot.cancelOrder('btc_cny',actual))
                    else:
                        co=okcoinSpot.cancelOrder('btc_cny',actual)
                if shared.CheckCode==False:
                    print("Ended closing orders")
            except:
                print("ERROR: At bot start, when cancelling orders from other sessions something failed")

        # Checking our own lists of Timeouts and closing those orders that have surpassed the timeout limit.
        numTimeouts=len(shared.TimeoutList1)
        if numTimeouts > 0 and shared.TICK > 1: 
            if shared.CheckCode==False:
                print("--------------------------------------------------------------------------------------------------------------------")
                print("Closing orders that reached timeout")            
            numTimeouts=len(shared.TimeoutList1)
            for x in reversed(range(1,numTimeouts+1)):
                if (shared.TimeoutList3[-x]=='buy' and ( shared.TICK - shared.TimeoutList2[-x] > shared.hb)):
                    try:
                        actual=shared.TimeoutList1[-x]
                        if shared.CheckCode==False: 
                            print(okcoinSpot.cancelOrder('btc_cny',actual))
                        else:
                            d=okcoinSpot.cancelOrder('btc_cny',actual)
                        del shared.TimeoutList1[-x]
                        del shared.TimeoutList2[-x]
                        del shared.TimeoutList3[-x]
                    except:
                        print("ERROR: Tried to cancel a buy order that reached the timeout but something failed")
            numTimeouts=len(shared.TimeoutList1)
            for x in reversed(range(1,numTimeouts+1)):
                if (shared.TimeoutList3[-x]=='sell' and ( shared.TICK - shared.TimeoutList2[-x] > shared.hs)):
                    try:
                        actual=shared.TimeoutList1[-x]
                        if shared.CheckCode==False: 
                            print(okcoinSpot.cancelOrder('btc_cny',actual))
                        else:
                            d=okcoinSpot.cancelOrder('btc_cny',actual)
                        del shared.TimeoutList1[-x]
                        del shared.TimeoutList2[-x]
                        del shared.TimeoutList3[-x]
                    except:
                        print("ERROR: Tried to cancel a sell order that reached the timeout but something failed")

        if shared.CheckCode==False:
            print("--------------------------------------------------------------------------------------------------------------------")
            print("Model vSidewaysPuckSTD wants to operate? %s [Why? Ang=%s < Th=%s ]" % (shared.vSidewaysPuckSTD, abs(common.linregangle(shared.ck,shared.A)[-1]), shared.Th))
        if shared.ALGO=="SIDEWAYS PUCK STD":
            if shared.vSidewaysPuckSTD:
                if shared.CheckCode==False:
                    print("--------------------------------------------------------------------------------------------------------------------")
                    print("DISPLAYING NEW PRICE CALCULATIONS FOR THIS TICK")
                    print("--------------------------------------------------------------------------------------------------------------------")
                
                sellprice=max(float(shared.price)*float(1+shared.FEEPCT/200),float(talib.LINEARREG(shared.ck,shared.P)[-shared.lag]) * (1 + (float(shared.KH)/10000)*float(talib.STDDEV(shared.ck,shared.S2)[-shared.lag])))
                buyprice =min(float(shared.price)*float(1-shared.FEEPCT/200),float(talib.LINEARREG(shared.ck,shared.P)[-shared.lag]) * (1 - (float(shared.KL)/10000)*float(talib.STDDEV(shared.ck,shared.S1)[-shared.lag])))
                
                if shared.CheckCode==False:
                    print("SELL  PRICE : %s | linreg(c,%s)=%s | overmodifier=%s" % (sellprice,shared.P,talib.LINEARREG(shared.ck,shared.P)[-shared.lag],+(float(shared.KH)/10000)*float(talib.STDDEV(shared.ck,shared.S2)[-shared.lag])))                
                    print("CLOSE PRICE : %s" % shared.price)
                    print("BUY   PRICE : %s | linreg(c,%s)=%s | undermodifier=%s" % (buyprice,shared.P,talib.LINEARREG(shared.ck,shared.P)[-shared.lag],-(float(shared.KL)/10000)*float(talib.STDDEV(shared.ck,shared.S1)[-shared.lag])))
                    print("--------------------------------------------------------------------------------------------------------------------")
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

                buyamount = float(shared.amountpct)*float(balance['info']['funds']['asset']['total'])/float(buyprice)
                if float(curr)/float(buyprice) > buyamount and buyamount > shared.amountmin:
                    try:
                        neworder=okcoinSpot.trade('btc_cny', 'buy' , buyprice , buyamount )
                        actual=json.loads(neworder)
                        if shared.CheckCode==False:
                            print("NEW BUY ORDER SENT: Buyprice %s , Buyamount %s" % (buyprice, buyamount))
                            shared.TimeoutList1.append(actual['order_id'])
                            shared.TimeoutList2.append(shared.TICK)
                            shared.TimeoutList3.append('buy')
                        else:
                            print(" %s ; buy ;  %s  ;  %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), buyprice, buyamount))                        
                            shared.TimeoutList1.append(randint(0,999999999))
                            shared.TimeoutList2.append(shared.TICK)
                            shared.TimeoutList3.append('buy')
                    except:
                        print("ERROR: Tried to place a buy order but something failed")
                #else:
                    #print("NO BUY order because condition is not true: (curr [%s]  / buyprice [%s] )> buyamount [%s] AND buyamount[%s] > shared.amountmin [%s]" % (curr, buyprice, buyamount, buyamount, shared.amountmin))
                
                sellamount = float(shared.amountpct)*float(balance['info']['funds']['asset']['total'])/float(buyprice)
                if assets > sellamount  and  sellamount > shared.amountmin:
                    try:
                        neworder=okcoinSpot.trade('btc_cny', 'sell' , sellprice , sellamount )
                        actual=json.loads(neworder)
                        if shared.CheckCode==False:
                            print("NEW SELL ORDER SENT: Sellprice %s , Sellamount %s" % ( sellprice,sellamount))                        
                            shared.TimeoutList1.append(actual['order_id'])
                            shared.TimeoutList2.append(shared.TICK)
                            shared.TimeoutList3.append('sell')
                        else:
                            print(" %s ; sell ;  %s  ;  %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), sellprice,sellamount))                        
                            shared.TimeoutList1.append(randint(0,999999999))
                            shared.TimeoutList2.append(shared.TICK)
                            shared.TimeoutList3.append('sell')
                    except:
                        print("ERROR: Tried to place a sell order but something failed")
                #else:
                    #print("NO SELL order because condition is not true: assets [%s] > sellamount [%s] AND sellamount[%s] > shared.amountmin [%s]" % (assets, sellamount,sellamount,shared.amountmin))
                    
                #print("--------------------------------------------------------------------------------------------------------------------")
                try:
                    if shared.CheckCode==False: 
                        okcoinSpot2 = OKCoinSpot(okcoinRESTURL,apikey,secretkey)
                        OpenOrders2=okcoinSpot.orderinfo('btc_cny','-1')
                        loadOrders2=json.loads(OpenOrders2)
                        numOrders2= len(loadOrders2['orders'])        
                        minpricesell=100000000
                        maxpricebuy=0
                        minXsell=0
                        maxXbuy=0
                        if numOrders2>0:
                            for x in reversed(range(1,numOrders2+1)):
                                if str(loadOrders2['orders'][-x]['type'])=='sell' and loadOrders2['orders'][-x]['price']< minpricesell :
                                    minXsell=-x
                                    minpricesell=loadOrders2['orders'][-x]['price']
                                if str(loadOrders2['orders'][-x]['type'])=='buy' and loadOrders2['orders'][-x]['price']> maxpricebuy :
                                    maxXbuy=-x
                                    maxpricebuy=loadOrders2['orders'][-x]['price']
                                    
                            print("DISPLAYING PRICE SPREAD CALCULATIONS BETWEEN MIN SELL AND MAX BUY OF EXISTING ORDERS")
                            print("--------------------------------------------------------------------------------------------------------------------")
                            if minXsell<0:
                                print("SELL  PRICE : %s | %s PCT Above Close" % (minpricesell, (float(minpricesell)/float(shared.price)-1)*100))
                            print("CLOSE PRICE : %s" % shared.price)                    
                            if maxXbuy<0:
                                print("BUY   PRICE : %s | %s PCT Below Close" % (maxpricebuy , (float(shared.price)/float(maxpricebuy)-1)*100))
                            print("--------------------------------------------------------------------------------------------------------------------")
                            if minXsell<0 and maxXbuy<0:
                                x1=minpricesell-maxpricebuy
                                x2=float(minpricesell)*(1-float(shared.FEEPCT/200)) - float(maxpricebuy)*(1+float(shared.FEEPCT/200))
                                x3=x1-x2
                                print("SPREAD in Price buy/sell = %s [Fee=%s] [NET=%s]" %(x1, x2, x3)) 
                                print("--------------------------------------------------------------------------------------------------------------------")
                except:
                    print("ERROR: Tried to get some stats but I Couldn't get the list of opened orders")
                    print("----------------------------------------------------------------------------")
            else:
                if shared.CheckCode==False:
                    print("Model does not want to operate at this moment:")


        
      


def main_thread():
    if shared.CheckCode==False:
        print(".")
        print(".")
        print(".")
        print(".")
        print(".")
        print(".")
        
        print("Initializing main daemon at %s ...." % (time.strftime("%Y-%m-%d %H:%M:%S") ) )
    else:
        print("date                ; type ;   btccny            ;  amount                ;")

    while running == True:
        try:
            broker_update()
            main_algo()
        except:
            print("ERROR: There was an unexpected error this tick. Retrying in two minutes")
        
        
        if shared.CheckCode==False:
            print("Tick processing ended at %s. Waiting %s Minutes for next tick" % (time.strftime("%Y-%m-%d %H:%M:%S"),shared.FRECUENCIA_MINUTOS))
        
        time.sleep(900-time.time()%900)
 
        

    


    


if __name__ == "__main__":
    main_thread()