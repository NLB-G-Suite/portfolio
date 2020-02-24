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

okcoinRESTURL="www.okcoin.cn"
apikey= '3cdfe4e2-6503-4f31-aa23-75f3f5128a23'
secretkey= '75E3C73F1ACABA51C3D410A21EBE3F31'

okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)



def return_balance():
    uinfo=okcoinSpot.userinfo()
    loadinfo=json.loads(uinfo)       
    return loadinfo

def return_ticker():
    ticker=okcoinSpot.ticker('btc_cny')
    return float(ticker['ticker']['buy'])

def update_info():
    try:
        shared.ticker=return_ticker()
        shared.balance=return_balance()     
        shared.assets=float(shared.balance['info']['funds']['free']['btc'])
        shared.curr=float(shared.balance['info']['funds']['free']['cny'])
        shared.net=float(shared.balance['info']['funds']['asset']['net'])
        shared.total=float(shared.balance['info']['funds']['asset']['total'])    
        shared.price=shared.ticker            
        if shared.TICK==1:
            shared.stassets = shared.assets
            shared.stcurr   = shared.curr
            shared.stnet    = shared.net
            shared.sttotal  = shared.total
            shared.stprice  = shared.price
    except:
        if shared.DEBUG:
            raise
        else:
            print("ERROR: there was a problem getting the ticker or the balance information")
    return 1

def broker_update():
    # DOCHLV
    from numpy import genfromtxt
    try:
        if os.name=='nt':
            shared.bars=genfromtxt('c:/Amibroker/Formulas/CSV_Tickers/OK-BTCCNY-15m.csv',delimiter=';',dtype=[('d','S16'),('o','<f8'),('c','<f8'),('h','<f8'),('l','<f8'),('v','<f8')],usemask=False)        
        else:
            shared.bars=genfromtxt('/home/CSV_Tickers/OK-BTCCNY-15m.csv',delimiter=';',dtype=[('d','S16'),('o','<f8'),('c','<f8'),('h','<f8'),('l','<f8'),('v','<f8')],usemask=False)
        shared.ck=shared.bars['c']
    except:
        if shared.DEBUG:
            raise
        else:
            print("ERROR: There was a problem reading the OK-BTCCNY-15m.csv file.")
            
    # Closing all orders still open from previous sessions of execution of the bot
    if shared.TICK==0 :  
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
            if shared.DEBUG:
                raise
            else:
                print("ERROR: At bot start, when cancelling orders from other sessions something failed")            

    shared.TICK=shared.TICK+1
    if shared.CheckCode==False:
        if shared.CheckCode==False:
            print("   ")
            print("********************************************************************************************************************")
            print(" T I C K = %s  [%s H] [Model:%s] [OKCOIN BTCCNY 15m]" % (shared.TICK, format(shared.TICK/4,'.2f'),shared.ALGO))
            print("********************************************************************************************************************")
    
    try:
        update_info()
        
        if shared.CheckCode==False:
            ActualBalanceCNY=shared.net
            StartBalanceCNY=shared.stcurr + shared.stassets * shared.stprice
            ProfitBalanceCNY=(ActualBalanceCNY/StartBalanceCNY-1)*100
            
            ActualBalanceBTC=shared.net/shared.price
            StartBalanceBTC=shared.stcurr/shared.stprice+shared.stassets
            ProfitBalanceBTC=(ActualBalanceBTC/StartBalanceBTC-1)*100
            
            ProfitBH=(shared.price/shared.stprice-1)*100
            print("Balance now consists in %s CNY and %s BTC" % (format(shared.curr,'.4f'),format(shared.assets,'.4f')))
            print("Actual Balance in CNY: %s | Start Belance in CNY: %s | PCT Profit: %s" % (format(ActualBalanceCNY,'.4f'), format(StartBalanceCNY,'.4f') , format(ProfitBalanceCNY,'.4f') ))
            print("Actual Balance in BTC: %s | Start Balance in BTC: %s | PCT Profit: %s" % (format(ActualBalanceBTC,'.4f'),format(StartBalanceBTC,'.4f'),format(ProfitBalanceBTC,'.4f') ))
            print("Buy & Hold Profit: %s" % (format(ProfitBH,'.4f') ))

    except:
        if shared.DEBUG:
            raise
        else:
            print("ERROR: Something failed when tried to get the user ticker/balance")
        
    try:
        if shared.CheckCode==False:
            if os.name=='nt':
                f=csv.writer(open("c:/Amibroker/Formulas/CSV_Tickers/stats_CR2LinRegSTD_Okcoin_15m.csv","a+"),delimiter=';')
                f.writerow([time.strftime("%Y-%m-%d %H:%M") , shared.ticker, shared.net, shared.net/shared.ticker, shared.total])                
            else:
                f=csv.writer(open("/home/CSV_Tickers/stats_CR2LinRegSTD_Okcoin_15m.csv","a+"),delimiter=';')
                f.writerow([time.strftime("%Y-%m-%d %H:%M") , shared.ticker, shared.net, shared.net/shared.ticker, shared.total])
    except:
        if shared.DEBUG:
            raise
        else:
            print("ERROR: Could not export performance stats to file. Have you got the CSV file opened?")


    try:
        if shared.CheckCode==False:
            if os.name=='nt':
                f=csv.writer(open("c:/Amibroker/Formulas/CSV_Tickers/stats_CR2LinRegSTD_Okcoin_15m.csv","a+"),delimiter=';')
                f.writerow([time.strftime("%Y-%m-%d %H:%M") , shared.ticker, shared.net, shared.net/shared.ticker, shared.total])
            else:
                f=csv.writer(open("/home/CSV_Tickers/stats_CR2LinRegSTD_Okcoin_15m.csv","a+"),delimiter=';')
                f.writerow([time.strftime("%Y-%m-%d %H:%M") , shared.ticker, shared.net, shared.net/shared.ticker, shared.total])
    except:
        if shared.DEBUG:
            raise
        else:
            print("ERROR: Could not export performance stats to file. Have you got the CSV file opened?")


    shared.vCR2LinRegSTD=common.CR2LinRegSTD(shared.ck,shared.P1,shared.P2,shared.Q1,shared.Q2,shared.lag)
    
    
    
    
def main_algo():
    shared.sig=0


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
                    if shared.DEBUG:
                        raise
                    else:
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
                    if shared.DEBUG:
                        raise
                    else:
                        print("ERROR: Tried to cancel a sell order that reached the timeout but something failed")

    if shared.CheckCode==False:
        print("--------------------------------------------------------------------------------------------------------------------")
        print("[ Bot Okcoin CR2LinRegSTD BTCCNY 15m - %s ] : LAST SIGNAL = %s - Dif Cross = %s PCT ]" %(time.strftime("%Y-%m-%d %H:%M:%S"), shared.vCR2LinRegSTD, ((talib.LINEARREG(shared.ck,shared.P1)[-shared.lag]/talib.LINEARREG(shared.ck,shared.P2)[-shared.lag])-1)*100) )
        print("--------------------------------------------------------------------------------------------------------------------")
        
    if shared.ALGO=="CR2LinRegSTD":
        
        sellprice=max(float(shared.price)*float(1+shared.FEEPCT/200),float(talib.LINEARREG(shared.ck,shared.P)[-shared.lag]) * (1 + (float(shared.KH)/50000)*float(talib.STDDEV(shared.ck,shared.S2)[-shared.lag])))
        buyprice =min(float(shared.price)*float(1-shared.FEEPCT/200),float(talib.LINEARREG(shared.ck,shared.P)[-shared.lag]) * (1 - (float(shared.KL)/50000)*float(talib.STDDEV(shared.ck,shared.S1)[-shared.lag])))
        
        try:
            balance=return_balance()
            assets=float(balance['info']['funds']['free']['btc'])
            curr=float(balance['info']['funds']['free']['cny'])    
        except:
            if shared.DEBUG:
                raise
            else:
                print("ERROR: Tried to get the balance from the exchange but something failed")
        try:
            update_info()
        except:
            if shared.DEBUG:
                raise
            else:
                print("ERROR: Tried to get the ticker data from the exchange but something failed")

        buyamount = float(shared.amountpct)*float(curr)/float(buyprice)
        if shared.vCR2LinRegSTD==1 and buyamount>shared.amountmin:
            try:
                neworder=okcoinSpot.trade('btc_cny', 'buy' , buyprice , buyamount )
                actual=json.loads(neworder)
                if shared.CheckCode==False:
                    print("NEW BUY ORDER SENT: Buyprice %s , Buyamount %s" % (format(buyprice,'.4f'), format(buyamount,'.4f')))
                    shared.TimeoutList1.append(actual['order_id'])
                    shared.TimeoutList2.append(shared.TICK)
                    shared.TimeoutList3.append('buy')
                else:
                    print(" %s ; buy ;  %s  ;  %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), format(buyprice,'.4f'), format(buyamount,'.4f')))
                    shared.TimeoutList1.append(randint(0,999999999))
                    shared.TimeoutList2.append(shared.TICK)
                    shared.TimeoutList3.append('buy')
                print("CLOSE PRICE : %s" % format(shared.price,'.4f'))
                print("BUY   PRICE : %s" % format(buyprice, '.4f'))
            except:
                if shared.DEBUG:
                    raise
                else:
                    print("ERROR: Tried to place a buy order but something failed")
        
        sellamount = float(shared.amountpct)*float(assets)
        if shared.vCR2LinRegSTD==-1 and sellamount>shared.amountmin:
            try:
                neworder=okcoinSpot.trade('btc_cny', 'sell' , sellprice , sellamount )
                actual=json.loads(neworder)
                if shared.CheckCode==False:
                    print("NEW SELL ORDER SENT: Sellprice %s , Sellamount %s" % ( format(sellprice,'.4f'),format(sellamount,'.4f')))                        
                    shared.TimeoutList1.append(actual['order_id'])
                    shared.TimeoutList2.append(shared.TICK)
                    shared.TimeoutList3.append('sell')
                else:
                    print(" %s ; sell ;  %s  ;  %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), format(sellprice,'.4f'),format(sellamount,'.4f')))                        
                    shared.TimeoutList1.append(randint(0,999999999))
                    shared.TimeoutList2.append(shared.TICK)
                    shared.TimeoutList3.append('sell')
                print("SELL  PRICE : %s" % format(sellprice,'.4f'))              
                print("CLOSE PRICE : %s" % format(shared.price,'.4f'))
                    
            except:
                if shared.DEBUG:
                    raise
                else:
                    print("ERROR: Tried to place a sell order but something failed")

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
                        print("SELL  PRICE : %s | %s PCT Above Close" % (format(minpricesell,'.4f'), format((float(minpricesell)/float(shared.price)-1)*100,'.4f')))
                    print("CLOSE PRICE : %s" % shared.price)                    
                    if maxXbuy<0:
                        print("BUY   PRICE : %s | %s PCT Below Close" % (format(maxpricebuy ,'.4f'), format((float(shared.price)/float(maxpricebuy)-1)*100,'.4f')))
                    print("--------------------------------------------------------------------------------------------------------------------")
                    if minXsell<0 and maxXbuy<0:
                        x1=minpricesell-maxpricebuy
                        x2=float(minpricesell)*(1-float(shared.FEEPCT/200)) - float(maxpricebuy)*(1+float(shared.FEEPCT/200))
                        x3=x1-x2
                        print("SPREAD in Price buy/sell = %s [Fee=%s] [NET=%s]" %(format(x1,'.4f'), format(x2,'.4f'), format(x3,'.4f'))) 
                        print("--------------------------------------------------------------------------------------------------------------------")
        except:
            if shared.DEBUG:
                raise
            else:            
                print("ERROR: Tried to get some stats but I Couldn't get the list of opened orders")
                print("----------------------------------------------------------------------------")



        
      


def main_thread():
    if shared.SHOWTABLE==False:
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
        running=True
        while running == True:
            try:
                broker_update()
                main_algo()
            except:
                if shared.DEBUG:
                    raise
                else:
                    print("ERROR: There was an unexpected error this tick. Retrying in two minutes")
            
            
            if shared.CheckCode==False:
                print("Tick processing ended at %s. Waiting %s Minutes for next tick" % (time.strftime("%Y-%m-%d %H:%M:%S"),shared.FRECUENCIA_MINUTOS))
            
            time.sleep(900-time.time()%900)
    else:
        broker_update()
        num=len(shared.bars)
        for k in reversed(range(1,num+1)):
            arr=shared.ck
            llag=-k
            val=common.dx(talib.LINEARREG(arr,shared.P1)[llag],talib.LINEARREG(arr,shared.P1+shared.P2)[llag])
            
            c1=val>0
            c2=val<0
            c3=talib.LINEARREG(arr,shared.Q1)[llag] > talib.LINEARREG(arr,shared.Q2)[llag] and talib.LINEARREG(arr,shared.Q1)[llag-1] < talib.LINEARREG(arr,shared.Q2)[llag-1]
            c4=talib.LINEARREG(arr,shared.Q1)[llag] > talib.LINEARREG(arr,shared.Q2)[llag] and talib.LINEARREG(arr,shared.Q1)[llag-1] < talib.LINEARREG(arr,shared.Q2)[llag-1]
            
            sig=0
            if c3 or c1:
                sig= 1
            if c4 or c2:
                sig=-1
                
            print("K: %s    |    %s    |    Close:    %s    |    CR2:    %s    |    c1:    %s    |    c2:    %s    |    c3:    %s    |    c4:    %s" % (num-k,shared.bars['d'][-k], format(shared.bars['c'][-k],'.4f'), sig, c1, c2 ,c3, c4 )       )

    


if __name__ == "__main__":
    main_thread()