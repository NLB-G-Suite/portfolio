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


polo=poloniex.Poloniex('I3NZ27JU-SW65T8V2-MSQ67158-TOA2RM2Z','8ef3dfd3c1f229a8edb162f83779f855ffeaaa1daf8528d704243fa926d9dca73c870f278ac160d96d87655059e0a17e095172dd129b0c3d50f1f8f10973741d')


   

def ice_buy():
    n = 1
    buying=True
    maxassets=float(shared.curr/shared.price+shared.assets)
    orderSize=float(maxassets/shared.SPLIT)
    if shared.curr>shared.MinOrderCurr:
        print("There is enough Curr to buy")
        buying=True
        selling=False
    else:
        buying=False 
        selling=False

    print("MaxAssets = %s | OrderSize = %s | LastPrice = %s" % (maxassets,orderSize,shared.price))
    while buying:
        amount=max(1,(0.8+0.4*random.random())*orderSize)                
        if shared.SPLIT>1 and float(shared.curr/shared.price) > max(1,float(orderSize*1.2)) and shared.curr > shared.MinOrderCurr:
            update_info()
            print("Iceberg Order ##%s" % n)
            print(polo.api('buy', {'currencyPair': shared.PAIR, 'rate': shared.price*(1+shared.PriceOverlap) , 'amount': amount }))
            n=n+1
            print("Waiting %s seconds until next order (TIMEOUT)" %shared.TIMEOUT)
            time.sleep(shared.TIMEOUT)
        else:
            time.sleep(shared.TIMEOUT)
            update_info()
            print("Lastprice %s" % shared.price)
            if shared.curr/shared.price > 0.01:
                precio=shared.price*1.01
                cantidad=0.95*(shared.curr/precio)
                print("Iceberg last order. Trying to spend the last %s %s buying %s at price %s" % (shared.curr, shared.PairCurr, cantidad, precio))
                print(polo.api('buy', {'currencyPair': shared.PAIR, 'rate': precio , 'amount': cantidad }))
                
                
            else:
                print("The exchange does not accept orders smaller than 0.01")
            buying=False
            print("Finished buying")
    
def ice_sell():
    n = 1
    selling=True
    maxassets=float(shared.curr/shared.price+shared.assets)
    orderSize=float(maxassets/shared.SPLIT)
    if shared.assets>shared.MinOrderAsset:
        print("There are enough assets to sell")
        selling=True
        buying=False
    else:
        selling=False
        buying=False
    
    while selling:
        amount=max(1,(0.8+0.4*random.random())*orderSize)
        if shared.SPLIT>1 and shared.assets > max(1,orderSize*1.2):
            update_info()
            print("Iceberg Order ##%s" % n)
            print(polo.api('sell', {'currencyPair': shared.PAIR, 'rate': shared.price*(1-shared.PriceOverlap) , 'amount': amount }))
            n=n+1
            print("Waiting %s seconds until next order (TIMEOUT)" %shared.TIMEOUT)
            time.sleep(shared.TIMEOUT)
        else:
            time.sleep(shared.TIMEOUT)
            update_info()
            print("Lastprice %s" % shared.price)
            if shared.assets>0.01:
                precio=shared.price*0.99
                cantidad=0.95*(shared.assets)
                print("Iceberg last order. Trying to sell the last %s %s for %s at price %s" % (shared.assets, shared.PairAsset, cantidad, precio))
                print(polo.api('sell', {'currencyPair': shared.PAIR, 'rate': precio , 'amount': cantidad }))

            else:
                print("The exchange does not accept orders smaller than 0.01")
            selling=False
            print("Finished selling")

def return_balance():
    uinfo=okcoinSpot.userinfo()
    loadinfo=json.loads(uinfo)       
    return loadinfo

def return_ticker():
    ticker=okcoinSpot.ticker('btc_cny')
    return float(ticker['ticker']['buy'])

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
            if shared.TICK==1:
                print("CRITICAL: there was a problem getting the ticker or the balance information.")
                print("Please restart and make sure that at least the first tick works properly.")
                shared.running=False
            else:
                print("ERROR: there was a problem getting the ticker or the balance information.")

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
    
    
            
    shared.TICK=shared.TICK+1
    if shared.CheckCode==False:
        print("   ")
        print("********************************************************************************************************************")
        print(" T I C K = %s  [%s H] [Model:%s] [POLONIEX ETHBTC 15m]" % (shared.TICK, format(shared.TICK/4,'.2f'), shared.ALGO))
        print("********************************************************************************************************************")
    
    shared.ck=calculate_close(shared.NUMVELAS)
    try:
        update_info()
        
        if shared.CheckCode==False:
            ActualBalanceBTC=shared.curr + shared.assets * shared.price
            StartBalanceBTC=shared.stcurr + shared.stassets * shared.stprice
            ProfitBalanceBTC=(ActualBalanceBTC/StartBalanceBTC-1)*100
            
            ActualBalanceETH=shared.curr/shared.price+shared.assets
            StartBalanceETH=shared.stcurr/shared.stprice+shared.stassets
            ProfitBalanceETH=(ActualBalanceETH/StartBalanceETH-1)*100
            
            ProfitBH=(shared.price/shared.stprice-1)*100
            print("Balance now consists in %s BTC and %s ETH" % (format(shared.curr,'.4f'),format(shared.assets,'.4f')))
            print("Actual Balance in BTC: %s | Start Belance in BTC: %s | PCT Profit: %s" % (format(ActualBalanceBTC,'.4f'), format(StartBalanceBTC,'.4f') , format(ProfitBalanceBTC,'.4f') ))
            print("Actual Balance in ETH: %s | Start Balance in ETH: %s | PCT Profit: %s" % (format(ActualBalanceETH,'.4f'),format(StartBalanceETH,'.4f'),format(ProfitBalanceETH,'.4f') ))
            print("Buy & Hold Profit: %s" % (format(ProfitBH,'.4f') ))
            print("Actual ETHBTC value: %s | ck value: %s" % (format(shared.ticker,'.4f'),format(shared.ck[-1],'.4f')))

    except:
        print("ERROR: Something failed when tried to get the user ticker/balance")
        if shared.DEBUG:
            raise
        
    try:
        if shared.CheckCode==False:
            if os.name=='nt':
                f=csv.writer(open("c:/Amibroker/Formulas/CSV_Tickers/stats_ZF4_PO_ETHBTC_15m.csv","a+"),delimiter=';')
                f.writerow([time.strftime("%Y-%m-%d %H:%M") , shared.ticker, shared.net, shared.net/shared.ticker, shared.total])
            else:
                f=csv.writer(open("/home/CSV_Tickers/stats_ZF4_PO_ETHBTC_15m.csv","a+"),delimiter=';')
                f.writerow([time.strftime("%Y-%m-%d %H:%M") , shared.ticker, shared.net, shared.net/shared.ticker, shared.total])
    except:
        print("ERROR: Could not export performance stats to file. Have you got the CSV file opened?")
        if shared.DEBUG:
            raise
        

    shared.vZF4=common.zf4(shared.ck,shared.A1,shared.LRp1,shared.FL1,shared.STDp1,shared.B1,shared.LRp2,shared.FL2,shared.STDp2,shared.C1,shared.LRp3,shared.FL3,shared.STDp3,shared.D1,shared.LRp4,shared.FL4,shared.STDp4)
    


    
def main_algo():
    shared.sig=0
    if shared.ALGO=="ZF4":
        

        if shared.vZF4[-1]>shared.Th1:
            shared.sig= 1
        if shared.vZF4[-1]<shared.Th2:
            shared.sig=-1                
        print("--------------------------------------------------------------------------------------------------------------------")
        print("[ Bot Poloniex ZF4 ETHBTC 15m - %s ] : LAST SIGNAL = %s [Sell %s < ZF4 = %s  > Buy %s ]" %(time.strftime("%Y-%m-%d %H:%M:%S"), shared.sig,shared.Th2 , format(shared.vZF4[-1],'.4f') , shared.Th1))
        print("--------------------------------------------------------------------------------------------------------------------")

        if shared.sig== 1 and shared.curr/shared.price > 0.01: 
            try:
                ice_buy()
            except:
                if shared.DEBUG:
                    raise
                else:
                    print("ERROR: There was a problem executing the BUY ORDER")
                
            
        if shared.sig==-1 and shared.assets>0.01:
            try:
                ice_sell()
            except:
                if shared.DEBUG:
                    raise
                else:
                    print("ERROR: There was a problem executing the SELL ORDER")
            



  


def main_thread():
    if shared.SHOWTABLE==False:
        print(".")
        print(".")
        print(".")
        print(".")
        print(".")
        print(".")
        
        print("Initializing main daemon at %s ...." % (time.strftime("%Y-%m-%d %H:%M:%S") ) )
        

        while shared.running == True:
            try:
                broker_update()
                main_algo()
            except:
                if shared.DEBUG:
                    raise
                else:
                    print("ERROR: There was an unexpected error this tick. Retrying in next tick")
            
            
            if shared.CheckCode==False:
                print("Tick processing ended at %s. Waiting %s Minutes for next tick" % (time.strftime("%Y-%m-%d %H:%M:%S"),shared.FRECUENCIA_MINUTOS))
            
            time.sleep(900-time.time()%900)


        
if __name__ == "__main__":
    main_thread()        