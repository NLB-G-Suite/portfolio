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

import poloniex
from random import randint


polo=poloniex.Poloniex('L59Q7PUP-1SN6IGH6-AIK6GUNP-KYDO3AZF','3e921956e80717e12ac5b7f6222f04ff873961760fa73e08cd7fa3b6e57de59005a9e88a4b4a5d106c74f85e2e1f69669f48746b51850c38490cca4665083e0a')

def update_info():
    try:
        val=polo.api('returnTicker')
        shared.ticker=float(val['BTC_ETH']['last'])
        shared.balance=polo.api('returnBalances')
        shared.assets=float(shared.balance['ETH'])
        shared.curr=float(shared.balance['BTC'])
        try:
            val2=polo.api('returnCompleteBalances')
            shared.net=float(val2['BTC']['btcValue'])+float(val2['ETH']['btcValue'])
        except ZeroDivisionError:
            shared.net=0
        shared.total=shared.net
        shared.price=shared.ticker            
        if shared.TICK==1 and shared.JUST_STARTED==0:
            print("We are on tick %s so storing starting balance data" % shared.TICK)
            shared.stassets = shared.assets
            shared.stcurr   = shared.curr
            shared.stnet    = shared.net
            shared.sttotal  = shared.total
            shared.stprice  = shared.price
            shared.JUST_STARTED=1
    except:
        if shared.DEBUG:
            raise
        else:
            print("ERROR: there was a problem getting the ticker or the balance information")
    return 1

def broker_update():
    
    def calculate_close(period):
        valor=[]
        for x in reversed(range(1,period+1)):
            valor.append(bars[-x]['close'])
        valor2=np.array(valor,dtype='float')
        return valor2    
    
    try:
        bars=polo.directpublic('https://poloniex.com/public?command=returnChartData&currencyPair=BTC_ETH&start=1405699200&end=9999999999&period=900')
    except:
        if shared.DEBUG==True:
            raise
        else:
            print("ERROR: There was an unexpected problem when downloading the historical bars from the exchange")
            
    if shared.TICK==0 :  
        try:
            OpenOrders=polo.api('returnOpenOrders',{'currencyPair':'BTC_ETH'})
            #loadOrders=json.loads(OpenOrders)
            numOrders= len(OpenOrders)        
            if shared.CheckCode==False:
                print("Just Started. We have %s orders. Closing all open orders from previous sessions" % numOrders)
            for x in reversed(range(1,numOrders+1)):
                actual=str(OpenOrders[-x]['orderNumber'])
                if shared.CheckCode==False:
                    print("Closing order %s" % (actual))
                    print(polo.api('cancelOrder',{'currencyPair':shared.PAIR,'orderNumber':actual}))
                else:
                    co=polo.api('cancelOrder',{'currencyPair':shared.PAIR,'orderNumber':actual})
            if shared.CheckCode==False:
                print("Ended closing orders")
        except:
            if shared.DEBUG:
                raise
            else:
                print("ERROR: At bot start, when cancelling orders from other sessions something failed")                
    
    
    shared.ck=calculate_close(shared.NUMVELAS)
    shared.vCR2LinRegSTD=common.CR2LinRegSTD(shared.ck,shared.P1,shared.P2,shared.Q1,shared.Q2,shared.lag)
    
    
def main_algo():    

    shared.TICK=shared.TICK+1
    if shared.CheckCode==False:
        print("   ")
        print("********************************************************************************************************************")
        print(" T I C K = %s  [%s H] [Model:%s] [POLONIEX ETHBTC 15m]" % (shared.TICK, format(shared.TICK/4,'.2f'), shared.ALGO))
        print("********************************************************************************************************************")
    
    try: #Showing a small table with the performance of the bot, assets, balances etc.
        update_info()
        if shared.CheckCode==False:
            ActualBalanceBTC=shared.net
            StartBalanceBTC=shared.stnet
            try:
                ProfitBalanceBTC=(ActualBalanceBTC/StartBalanceBTC-1)*100
            except ZeroDivisionError:
                ProfitBalanceBTC=0
            
            ActualBalanceETH=shared.net/shared.price
            StartBalanceETH=shared.stnet/shared.stprice
            try:
                ProfitBalanceETH=(ActualBalanceETH/StartBalanceETH-1)*100
            except ZeroDivisionError:
                ProfitBalanceETH=0
            
            ProfitBH=(shared.price/shared.stprice-1)*100
            print("Balance now consists in %s BTC and %s ETH" % (format(shared.curr,'.8f'),format(shared.assets,'.8f')))
            print("Actual Balance in BTC: %s | Start Belance in BTC: %s | PCT Profit: %s" % (format(ActualBalanceBTC,'.8f'),format(StartBalanceBTC,'.8f'),format(ProfitBalanceBTC,'.8f') ))
            print("Actual Balance in ETH: %s | Start Balance in ETH: %s | PCT Profit: %s" % (format(ActualBalanceETH,'.8f'),format(StartBalanceETH,'.8f'),format(ProfitBalanceETH,'.8f') ))
            print("Buy & Hold Profit: %s" % (format(ProfitBH,'.8f') ))
    except:
        if shared.DEBUG:
            raise
        else:
            print("ERROR: Something failed when tried to get the user ticker/balance")
        
    try: # We export statistics to an external file to keep track of the amounts curr y balance and study performance
        if shared.CheckCode==False:
            if os.name=='nt':
                f=csv.writer(open("c:/Amibroker/Formulas/CSV_Tickers/stats_CR2LinRegSTD_Poloniex_15m.csv","a+"),delimiter=';')
                f.writerow([time.strftime("%Y-%m-%d %H:%M") , shared.ticker, shared.net, shared.net/shared.ticker, shared.total])                
            else:
                f=csv.writer(open("/home/CSV_Tickers/stats_CR2LinRegSTD_Poloniex_15m.csv","a+"),delimiter=';')
                f.writerow([time.strftime("%Y-%m-%d %H:%M") , shared.ticker, shared.net, shared.net/shared.ticker, shared.total])
    except:
        if shared.DEBUG:
            raise
        else:
            print("ERROR: Could not export performance stats to file. Have you got the CSV file opened?")


    shared.sig=0


    # Checking our own lists of Timeouts and closing those orders that have surpassed the timeout limit.
    numTimeouts=len(shared.TimeoutList1)
    if numTimeouts > 0 and shared.TICK > 1: 
        if shared.CheckCode==False:
            print("--------------------------------------------------------------------------------------------------------------------")
            print("Checking out for orders that reached timeout to close them")            
        numTimeouts=len(shared.TimeoutList1)
        for x in reversed(range(1,numTimeouts+1)):
            if (shared.TimeoutList3[-x]=='buy' and ( shared.TICK - shared.TimeoutList2[-x] > shared.hb)):
                try:
                    actual=shared.TimeoutList1[-x]
                    if shared.CheckCode==False: 
                        print(polo.api('cancelOrder',{'currencyPair':shared.PAIR,'orderNumber':shared.TimeoutList1[-x]}))
                    else:
                        d=polo.api('cancelOrder',{'currencyPair':shared.PAIR,'orderNumber':shared.TimeoutList1[-x]})
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
                        print(polo.api('cancelOrder',{'currencyPair':shared.PAIR,'orderNumber':shared.TimeoutList1[-x]}))
                    else:
                        d=polo.api('cancelOrder',{'currencyPair':shared.PAIR,'orderNumber':shared.TimeoutList1[-x]})
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
        print("[ Bot Poloniex CR2LinRegSTD ETHBTC 15m - %s ] : LAST SIGNAL = %s - Dif Cross = %s PCT ]" %(time.strftime("%Y-%m-%d %H:%M:%S"), shared.vCR2LinRegSTD, format(((talib.LINEARREG(shared.ck,shared.P1)[-shared.lag]/talib.LINEARREG(shared.ck,shared.P2)[-shared.lag])-1)*100,'.8f')) )
        print("--------------------------------------------------------------------------------------------------------------------")
        
    if shared.ALGO=="CR2LinRegSTD":
        
        sellprice=max(float(shared.price)*float(1+shared.FEEPCT/200),float(talib.LINEARREG(shared.ck,shared.P)[-shared.lag]) * (1 + (float(shared.KH)/50000)*float(talib.STDDEV(shared.ck,shared.S2)[-shared.lag])))
        buyprice =min(float(shared.price)*float(1-shared.FEEPCT/200),float(talib.LINEARREG(shared.ck,shared.P)[-shared.lag]) * (1 - (float(shared.KL)/50000)*float(talib.STDDEV(shared.ck,shared.S1)[-shared.lag])))
        
        try:
            update_info()
        except:
            if shared.DEBUG:
                raise
            else:
                print("ERROR: Tried to get the ticker data from the exchange but something failed")

        buyamount = float(shared.amountpct)*float(shared.curr)/float(buyprice)
        if shared.vCR2LinRegSTD==1 and buyamount>shared.amountmin:
            try:
                actual=polo.api('buy', {'currencyPair': shared.PAIR, 'rate': buyprice , 'amount': buyamount })
            except:
                if shared.DEBUG:
                    raise
                else:
                    print("ERROR: Buy oder failed")
            try:
                if shared.CheckCode==False:
                    print("NEW BUY ORDER SENT: Buyprice %s , Buyamount %s" % (format(buyprice,'.8f'), format(buyamount,'.8f')))
                    shared.TimeoutList1.append(actual['orderNumber'])
                    shared.TimeoutList2.append(shared.TICK)
                    shared.TimeoutList3.append('buy')
                else:
                    print(" %s ; buy ;  %s  ;  %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), format(buyprice,'.8f'), format(buyamount,'.8f')))
                    shared.TimeoutList1.append(randint(0,999999999))
                    shared.TimeoutList2.append(shared.TICK)
                    shared.TimeoutList3.append('buy')
                print("CLOSE PRICE : %s" % format(shared.price,'.8f'))
                print("BUY   PRICE : %s" % format(buyprice, '.8f'))
            except:
                if shared.DEBUG:
                    raise
                else:
                    print("ERROR: Tried to place a buy order but something failed")
        
        sellamount = float(shared.amountpct)*float(shared.assets)
        if shared.vCR2LinRegSTD==-1 and sellamount>shared.amountmin:
            try:
                actual=polo.api('sell', {'currencyPair': shared.PAIR, 'rate': sellprice , 'amount': sellamount })
            except:
                if shared.DEBUG:
                    raise
                else:
                    print("ERROR: Sell oder failed")
            try:
                if shared.CheckCode==False:
                    print("NEW SELL ORDER SENT: Sellprice %s , Sellamount %s" % ( format(sellprice,'.8f'),format(sellamount,'.8f')))                        
                    shared.TimeoutList1.append(actual['orderNumber'])
                    shared.TimeoutList2.append(shared.TICK)
                    shared.TimeoutList3.append('sell')
                else:
                    print(" %s ; sell ;  %s  ;  %s" % (time.strftime("%Y-%m-%d %H:%M:%S"), format(sellprice,'.8f'),format(sellamount,'.8f')))                        
                    shared.TimeoutList1.append(randint(0,999999999))
                    shared.TimeoutList2.append(shared.TICK)
                    shared.TimeoutList3.append('sell')
                print("SELL  PRICE : %s" % format(sellprice,'.8f'))              
                print("CLOSE PRICE : %s" % format(shared.price,'.8f'))
            except:
                if shared.DEBUG:
                    raise
                else:
                    print("ERROR: Tried to place a sell order but something failed")

        try:
            if shared.CheckCode==False: 
                OpenOrders2=polo.api('returnOpenOrders',{'currencyPair':'BTC_ETH'})
                numOrders2= len(OpenOrders2)        
                minpricesell=100000000
                maxpricebuy=0
                minXsell=0
                maxXbuy=0
                if numOrders2>0:
                    for x in reversed(range(1,numOrders2+1)):
                        if str(OpenOrders2[-x]['type'])=='sell' and float(OpenOrders2[-x]['rate'])< minpricesell :
                            minXsell=-x
                            minpricesell=float(OpenOrders2[-x]['rate'])
                        if str(OpenOrders2[-x]['type'])=='buy' and float(OpenOrders2[-x]['rate'])> maxpricebuy :
                            maxXbuy=-x
                            maxpricebuy=float(OpenOrders2[-x]['rate'])
                            
                    print("DISPLAYING PRICE SPREAD CALCULATIONS BETWEEN MIN SELL AND MAX BUY OF EXISTING ORDERS")
                    print("--------------------------------------------------------------------------------------------------------------------")
                    if minXsell<0:
                        print("SELL  PRICE : %s | %s PCT Above Close" % (format(minpricesell,'.8f'), format((float(minpricesell)/float(shared.price)-1)*100,'.8f')))
                    print("CLOSE PRICE : %s" % shared.price)                    
                    if maxXbuy<0:
                        print("BUY   PRICE : %s | %s PCT Below Close" % (format(maxpricebuy ,'.8f'), format((float(shared.price)/float(maxpricebuy)-1)*100,'.8f')))
                    print("--------------------------------------------------------------------------------------------------------------------")
                    if minXsell<0 and maxXbuy<0:
                        x1=minpricesell-maxpricebuy
                        x2=float(minpricesell)*(1-float(shared.FEEPCT/200)) - float(maxpricebuy)*(1+float(shared.FEEPCT/200))
                        x3=x1-x2
                        print("SPREAD in Price buy/sell = %s [Fee=%s] [NET=%s]" %(format(x1,'.8f'), format(x2,'.8f'), format(x3,'.8f'))) 
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
                
            print("K: %s    |    %s    |    Close:    %s    |    CR2:    %s    |    c1:    %s    |    c2:    %s    |    c3:    %s    |    c4:    %s" % (num-k,shared.bars['d'][-k], format(shared.bars['c'][-k],'.8f'), sig, c1, c2 ,c3, c4 )       )

    


if __name__ == "__main__":
    main_thread()