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


polo=poloniex.Poloniex(shared.API_Key,shared.API_SECRET)


   

def ice_buy():
    n = 1
    if shared.assets<0.0001:
        buying=True
        
        while buying:
            if shared.curr*shared.PARTE>shared.MinOrderCurr:
                print("There is enough Curr to buy = %s " % (shared.curr*shared.PARTE))
                buying=True
                selling=False
            else:
                buying=False 
                selling=False        
            print("Displaying DEBUGGING data for buy order for pair: %s   RATE: %s  AMOUNT:  %s   [curr: %s | price: %s | assets: %s]" % (shared.symbol,shared.price*(1+shared.PriceOverlap),shared.curr*shared.PARTE/shared.price,shared.curr,shared.price,shared.assets))            
            if float(shared.curr*shared.PARTE/shared.price) > 0.0001 and shared.assets < 0.0001:
                print("ORDER DATA FOR PAIR: %s   RATE: %s  AMOUNT:  %s   [curr: %s | price: %s | assets: %s]" % (shared.symbol,shared.price*(1+shared.PriceOverlap),shared.curr*shared.PARTE/shared.price,shared.curr,shared.price,shared.assets))            
                print(polo.api('buy', {'currencyPair': 'BTC_'+shared.symbol, 'rate': shared.price*(1+shared.PriceOverlap) , 'amount': shared.curr*shared.PARTE/shared.price }))
                time.sleep(shared.TIMEOUT)
                update_info()            
            else:
                buying=False
                print("Finished buying")
    else:
        print("We already have enough %s" % shared.symbol)
    
def ice_sell():
    n = 1
    selling=True

    if shared.assets>shared.MinOrderAsset:
        print("There are enough assets to sell")
        selling=True
        buying=False
    else:
        selling=False
        buying=False
    
    while selling:
        if shared.assets > 0.0001:
            print("SELLING PAIR: %s   RATE: %s  AMOUNT:  %s" % (shared.symbol,shared.price*(1-shared.PriceOverlap),shared.assets))
            print(polo.api('sell', {'currencyPair':'BTC_'+ shared.symbol, 'rate': shared.price*(1-shared.PriceOverlap) , 'amount': shared.assets }))
            time.sleep(shared.TIMEOUT)
            update_info()            
        else:
            selling=False
            print("Finished selling")

def return_balance():
    uinfo=okcoinSpot.userinfo()
    loadinfo=json.loads(uinfo)       
    return loadinfo

def update_info():
    try:
        val=polo.api('returnTicker')
        shared.ticker=float(val['BTC_'+shared.symbol]['last'])
        shared.balance=polo.api('returnBalances')
        shared.assets=float(shared.balance[shared.symbol])
        shared.curr=float(shared.balance['BTC'])
        try:
            val2=polo.api('returnCompleteBalances')
            shared.net=0+float(val2['BTC']['btcValue'])
            for allsymbols in shared.SYMBOLS:
                shared.net=shared.net+float(val2[allsymbols]['btcValue'])
        except ZeroDivisionError:
            shared.net=0
        shared.total=shared.net
        shared.price=shared.ticker            
        if shared.TICK==1 and shared.JUST_STARTED==0:
            print("We are on tick %s so storing starting balance data" % shared.TICK)
            shared.stassets.append( shared.assets)
            shared.stcurr.append(shared.curr)
            shared.stnet.append(shared.net)
            shared.sttotal.append(shared.total)
            shared.stprice.append(shared.price)
            
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
        bars=polo.directpublic('https://poloniex.com/public?command=returnChartData&currencyPair=BTC_'+shared.symbol+'&start=1469404801&end=9999999999&period=300')
    except:
        if shared.DEBUG==True:
            raise
        else:
            print("ERROR: There was an unexpected problem when downloading the historical bars from the exchange")
            
    
    try:
        OpenOrders=polo.api('returnOpenOrders',{'currencyPair':'BTC_'+shared.symbol})
        numOrders= len(OpenOrders)  
        if numOrders>0:
            if shared.CheckCode==False:
                print("We have %s orders to close" % numOrders)
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
            print("ERROR: error cancelling open orders in market %s" % shared.symbol)                
    
    
            
    
    
    shared.ck=calculate_close(shared.NUMVELAS)
    try:
        update_info()
        
        if shared.CheckCode==False:
            ActualBalanceBTC=shared.net
            StartBalanceBTC=shared.stnet[shared.Nsymbol]
            if StartBalanceBTC==0:
                ProfitBalanceBTC=0
            else:
                ProfitBalanceBTC=(ActualBalanceBTC/StartBalanceBTC-1)*100            

            ActualBalanceAST=shared.net/shared.price
            StartBalanceAST=shared.stnet[shared.Nsymbol]/shared.stprice[shared.Nsymbol]
            if StartBalanceAST==0:
                ProfitBalanceAST=0
            else:
                ProfitBalanceAST=(ActualBalanceAST/StartBalanceAST-1)*100
            
            ProfitBH=(shared.price/shared.stprice[shared.Nsymbol]-1)*100
            print("Balance now consists in %s BTC and %s %s" % (format(shared.curr,'.4f'),format(shared.assets,'.4f'),shared.symbol))
            print("Actual Balance in BTC: %s | Start Belance in BTC: %s | PCT Profit: %s" % (format(ActualBalanceBTC,'.4f'), format(StartBalanceBTC,'.4f') , format(ProfitBalanceBTC,'.4f') ))
            print("Actual Balance in %s: %s | Start Balance in %s: %s | PCT Profit: %s" % (shared.symbol,format(ActualBalanceAST,'.4f'),shared.symbol,format(StartBalanceAST,'.4f'),format(ProfitBalanceAST,'.4f') ))
            print("Buy & Hold Profit: %s" % (format(ProfitBH,'.4f') ))
            print("Actual %sBTC value: %s | ck value: %s" % (shared.symbol,format(shared.ticker,'.8f'),format(shared.ck[-1],'.8f')))

    except:
        print("ERROR: Something failed when tried to get the user ticker/balance")
        if shared.DEBUG:
            raise
        
    try:
        if shared.CheckCode==False:
            if os.name=='nt':
                f=csv.writer(open("c:/Amibroker/Formulas/CSV_Tickers/stats_PO_"+shared.ALGO+"_"+shared.symbol+"BTC_15m.csv","a+"),delimiter=';')
                f.writerow([time.strftime("%Y-%m-%d %H:%M") , shared.ticker, shared.net, shared.net/shared.ticker, shared.total])
            else:
                f=csv.writer(open("/home/CSV_Tickers/stats_PO_"+shared.ALGO+"_"+shared.symbol+"BTC_5m.csv","a+"),delimiter=';')
                f.writerow([time.strftime("%Y-%m-%d %H:%M") , shared.ticker, shared.net, shared.net/shared.ticker, shared.total])
    except:
        print("ERROR: Could not export performance stats to file. Have you got the CSV file opened?")
        if shared.DEBUG:
            raise
        


    
def main_algo():
    shared.sig=0
    if shared.ALGO=="MultiNeuron3":
        
        k       =   65
        p1      =  402
        
        w1_1    =   -0.33576
        w1_2    =   -0.42649
        w1_3    =   -0.64747
        
        w2_1    =    0.95157
        w2_2    =   -0.09499
        w2_3    =   -0.25182
        
        w3_1    =   -0.32593
        w3_2    =   -0.14129
        w3_3    =   -0.43455

        f1      =   -0.18699
        f2      =    0.19483
        f3      =   -0.24852

        

        i1 = common.ZSROCLAG(shared.ck,p1,k*0)/5
        i2 = common.ZSROCLAG(shared.ck,p1,k*1)/5
        i3 = common.ZSROCLAG(shared.ck,p1,k*2)/5
        
        n0_1 = i1;
        n0_2 = i2;
        n0_3 = i3;
        
        n1_1 = common.neuron3(n0_1,n0_2,n0_3,w1_1,w1_2,w1_3);
        n1_2 = common.neuron3(n0_1,n0_2,n0_3,w2_1,w2_2,w2_3);
        n1_3 = common.neuron3(n0_1,n0_2,n0_3,w3_1,w3_2,w3_3);
        
        n2_1 = common.neuron3(n1_1,n1_2,n1_3,f1,f2,f3) * 100;
        
        buy =n2_1 < -2;
        sell=n2_1 >  2;
        
        if buy :
            shared.sig =  1
        if sell :
            shared.sig = -1
        print("The signal is %s (Buy -2 > n4[%s] > 2 Sell)" % (shared.sig,n2_1))

        if shared.sig== 1 and shared.curr/shared.price > 0.01 and shared.TICK>1: 
            try:
                ice_buy()
            except:
                if shared.DEBUG:
                    raise
                else:
                    print("ERROR: There was a problem executing the BUY ORDER")
                
            
        if shared.sig==-1 and shared.assets>0.01 and shared.TICK>1:
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
            shared.TICK=shared.TICK+1
            if shared.CheckCode==False:
                print("   ")
                print("********************************************************************************************************************")
                print(" T I C K = %s  [%s H] [Model:%s] [POLONIEX 5m - %s] DEBUG: %s" % (shared.TICK, format(shared.TICK/12,'.2f'), shared.ALGO,shared.ACCOUNT,shared.DEBUG))
                print("********************************************************************************************************************")
            
            for shared.symbol in shared.SYMBOLS:
                shared.Nsymbol=shared.SYMBOLS.index(shared.symbol) 
                print(" ")
                print("ACTUAL MARKET BTC_%s  Idx: %s" % (shared.symbol, shared.Nsymbol) )
                print("--------------------------------------------------------------------------------------------------------------------")
                try:
                    broker_update()
                    main_algo()
                except:
                    if shared.DEBUG:
                        raise
                    else:
                        print("ERROR: There was an unexpected error this tick. Retrying in next tick")
            
                time.sleep(20)
            
            if shared.CheckCode==False:
                print(" ")
                print("")
                print("Tick processing ended at %s. Waiting %s Minutes for next tick" % (time.strftime("%Y-%m-%d %H:%M:%S"),shared.FRECUENCIA_MINUTOS))

            if shared.JUST_STARTED==0:
                shared.JUST_STARTED=1
                
            
            time.sleep(300-time.time()%300)


        
if __name__ == "__main__":
    main_thread()        