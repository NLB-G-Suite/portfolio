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
import sys

import poloniex
from random import randint

import importlib
import parameters

polo=poloniex.Poloniex(shared.API_Key,shared.API_SECRET)


class bcolors:                                
    HEADER = '\033[95m'
    RED = '\033[1;31m'
    GREEN = '\033[1;32m'
    PURPLE = '\033[1;35m'
    CYAN = '\033[36m'
    GREY = '\033[37m'
    WHITE = '\033[1;37m'
    YELLOW = '\033[33m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

rojo=bcolors.RED
verde=bcolors.GREEN
gris=bcolors.GREY
blanco=bcolors.WHITE
amarillo=bcolors.YELLOW
purpura=bcolors.PURPLE
neutro=bcolors.ENDC
azulclaro=bcolors.CYAN



def limit_buy():
    
    update_info() 
    
    if shared.AssetPrevSession[shared.Nsymbol]==0:
    
        PAIR   = shared.symbol
        RATE   = shared.price * (1-parameters.DentInOrderBook)
        AMOUNT = float(shared.PARTE/RATE)
        
        if parameters.VERBOSE==True:
            print ("%sLimitOrdersSince = %s %s" % (purpura,shared.LimitOrderSince[shared.Nsymbol],neutro))
        
        if AMOUNT > 0.0001 and shared.assets < 0.0001 and shared.curr > shared.PARTE:
            
            if shared.LimitOrderSince[shared.Nsymbol]==0:
                shared.LimitOrderSince[shared.Nsymbol]=1
                shared.LimitPrice[shared.Nsymbol]=RATE
                if parameters.VERBOSE==True:
                    print ("%sBuy order just started being executed in this tick, storing LimitOrderSince=1 and LimitPrice %s" % (purpura,neutro))
                
            else:
                if parameters.VERBOSE==True:
                    print ("%sBuy order being requested AGAIN LimitOrderSince += 1 %s" % (purpura,neutro))
                
                print("%s- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - %s" % (amarillo,neutro))
                print("%sThis BUY order could not be executed in %s ticks. RETRYING%s" %(amarillo,shared.LimitOrderSince[shared.Nsymbol],neutro) )
                if shared.LimitPrice[shared.Nsymbol] > 0:
                    PricePctDiff=(shared.price/shared.LimitPrice[shared.Nsymbol]-1)*100
                    print("%sThe original price was %s . Now it is %s . Diff is %s PCT %s" % (amarillo,format(shared.LimitPrice[shared.Nsymbol],'.8f'),format(shared.price,'.8f'),format(PricePctDiff,'.2f'),neutro) )                
                print("%s- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - %s" % (amarillo,neutro))        
                shared.LimitOrderSince[shared.Nsymbol]=shared.LimitOrderSince[shared.Nsymbol]+1                    
            
            print("BUYING PAIR: %s   RATE: %s  AMOUNT:  %s   [curr: %s | price: %s | assets: %s]" % ( PAIR , RATE , AMOUNT , shared.curr, shared.price , shared.assets ))            
            print(polo.api('buy', {'currencyPair': 'BTC_' + PAIR, 'rate': RATE , 'amount': AMOUNT, 'postOnly': 1 }))
            
        else:
            
            if parameters.VERBOSE==True:
                print("%s============================ %s" % (purpura,neutro))
                print("%sVERBOSE POST-BUY INFORMATION %s" % (purpura,neutro))
                print("%s============================ %s" % (purpura,neutro))
                print("%sWe are not buying anymore. WHAT ARE THE REASONS ? %s %s" % (purpura, shared.Nsymbol, neutro))
                if shared.assets >= 0.0001:
                    print("%s     + We already have assets bought => shared.assets=%s %s" % (purpura, shared.assets, neutro))
                if shared.curr <= shared.PARTE:    
                    print("%s     + We don't have any more currency %s to buy a PARTE %s of asset %s %s" % (purpura, shared.curr,shared.PARTE,shared.symbol, neutro))
                print("")
                print("%sADDITIONAL INFORMATION %s" % (purpura, neutro))                
                print("%s     - It took us %s ticks to execute the order %s" % (purpura, shared.LimitOrderSince[shared.Nsymbol],neutro))
                print("%s     - Previous Order Type = %s %s" % (purpura, shared.LastOrderType[shared.Nsymbol],neutro))
                print("%s             + NOTE of what I THINK IT <<<SHOULD>>> DO :  %s" % (purpura, neutro))                
                print("%s                     + If Order Type = `NONE YET` then we should accept the order as a new buy, add it to stats, reset the assetprevsession but don't calculate profits  %s" % (purpura, neutro))                
                print("%s                     + If Order Type = `BUY` then as we are in buy, probably we are just RETRYING. We don't add it to stats, we don't calculate profit. Maybe yes slippage  %s" % (purpura, neutro))                
                print("%s                     + If Order Type = `SELL` then as we add it to stats and calculate profit. Maybe slippage aswell? %s" % (purpura, neutro))                
                print("%s     - Do we still hold assets from a previous session? (1 or 0) AssetPrevSession=%s (this should not be the case ever inside this `if`) %s" % (purpura,shared.AssetPrevSession[shared.Nsymbol],neutro))
                print("%s     - The LimitPrice we used in the buy order (this last signal)was %s %s" % (purpura, shared.LimitPrice[shared.Nsymbol],neutro)
                print("%s     - The LastOrderPrice we stored with the price at what the previous order was executed was %s %s" % (purpura, shared.LastOrderPrice[shared.Nsymbol],neutro)
                print("")
               

    
            # LAST ORDER TYPE = BUY or NONE YET
                
            if shared.LastOrderType[shared.Nsymbol]=='buy' or shared.LastOrderType[shared.Nsymbol] == 'NONE YET':            
                shared.LastOrderPrice[shared.Nsymbol]=shared.LimitPrice[shared.Nsymbol]
                shared.LimitSlippage[shared.Nsymbol]=shared.LimitSlippage[shared.Nsymbol]+(shared.price/shared.LimitPrice[shared.Nsymbol]-1)*100
                shared.LimitOrderSince[shared.Nsymbol]=0                    
                shared.AssetPrevSession[shared.Nsymbol]=0     
                shared.LastOrderType[shared.Nsymbol]="buy"    

                
            # LAST ORDER TYPE = SELL                
                
            if shared.LastOrderType[shared.Nsymbol]=='sell':
                if shared.LimitPrice[shared.Nsymbol] < shared.LastOrderPrice[shared.Nsymbol]:
                    print("%sProfitable operation: We sold at %s and now we repurchase at %s [PCT = %s]%s" % (verde,shared.LastOrderPrice[shared.Nsymbol],shared.LimitPrice[shared.Nsymbol],format(float(shared.LastOrderPrice[shared.Nsymbol]/shared.LimitPrice[shared.Nsymbol]-1)*100,'.2f'),neutro))
                    shared.CorrectBuys[shared.Nsymbol]=shared.CorrectBuys[shared.Nsymbol]+1
                else:
                    print("%sNOT Profitable operation: We sold at %s and now we repurchase at %s [PCT = %s]%s" % (rojo,shared.LastOrderPrice[shared.Nsymbol],shared.LimitPrice[shared.Nsymbol],format(float(shared.LastOrderPrice[shared.Nsymbol]/shared.LimitPrice[shared.Nsymbol]-1)*100,'.2f'),neutro))
                shared.PointsEarned[shared.Nsymbol]=shared.PointsEarned[shared.Nsymbol]+points()

            # LAST ORDER TYPE = SELL or NONE YET
            
            if shared.LastOrderType[shared.Nsymbol]=='sell' or shared.LastOrderType[shared.Nsymbol] == 'NONE YET':
                shared.TotalBuys=shared.TotalBuys+1
                shared.BuysPerAsset[shared.Nsymbol]=shared.BuysPerAsset[shared.Nsymbol]+1

            print("Finished")                             
    else:
        print("We still have %s %s to sell from previous sessions. Not buying more" % (shared.assets,shared.symbol) )
        


def limit_sell():

    update_info() 
    
    PAIR   = shared.symbol
    RATE   = shared.price * (1+parameters.DentInOrderBook)
    AMOUNT = shared.assets
    
   
    if shared.assets > 0.0001:
       
        if shared.LimitOrderSince[shared.Nsymbol]==0:
            shared.LimitOrderSince[shared.Nsymbol]=1
            shared.LimitPrice[shared.Nsymbol]=RATE
            if parameters.VERBOSE==True:
                print ("%sSell order just started being executed in this tick, storing LimitOrderSince=1 and LimitPrice %s" % (purpura,neutro))
                
        else:                                            # Or if we just keep resending and resending the sell
        
            if parameters.VERBOSE==True:
                print ("%sSell order being requested AGAIN LimitOrderSince += 1 %s" % (purpura,neutro))
                
                
            print("%s- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - %s" % (amarillo,neutro))
            print("%sThis SELL order could not be executed in %s ticks. RETRYING%s" %(amarillo, shared.LimitOrderSince[shared.Nsymbol] ,neutro) )
            if shared.LimitPrice[shared.Nsymbol] > 0:
                PricePctDiff=(shared.price/shared.LimitPrice[shared.Nsymbol]-1)*100*-1
                print("%sThe original price was %s . Now it is %s . Diff is %s PCT %s" % (amarillo,format(shared.LimitPrice[shared.Nsymbol],'.8f'),format(shared.price,'.8f'),format(PricePctDiff,'.2f'),neutro) )                
            print("%s- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - %s" % (amarillo,neutro))

            shared.LimitOrderSince[shared.Nsymbol]=shared.LimitOrderSince[shared.Nsymbol]+1                    
        
        print("SELLING PAIR: %s   RATE: %s  AMOUNT:  %s    [curr: %s | price: %s | assets: %s]" % ( PAIR , RATE , AMOUNT , shared.curr, shared.price , shared.assets ))
        print(polo.api('sell', {'currencyPair':'BTC_'+ PAIR , 'rate': RATE , 'amount': AMOUNT, 'postOnly': 1 }))   #En cualquier caso vendemos.
        

    else:
        
        if parameters.VERBOSE==True:
            print("%s============================ %s" % (purpura,neutro))
            print("%sVERBOSE POST-SELL INFORMATION %s" % (purpura,neutro))
            print("%s============================ %s" % (purpura,neutro))
            print("%sWe are not selling anymore. WHAT ARE THE REASONS ? %s %s" % (purpura, shared.Nsymbol, neutro))
            if shared.assets <= 0.0001:
                print("%s     + We already have assets sold => shared.assets=%s %s" % (purpura, shared.assets, neutro))
            print("")
            print("%sADDITIONAL INFORMATION %s" % (purpura, neutro))                
            print("%s     - It took us %s ticks to execute the order %s" % (purpura, shared.LimitOrderSince[shared.Nsymbol],neutro))
            print("%s     - Previous Order Type = %s %s" % (purpura, shared.LastOrderType[shared.Nsymbol],neutro))
            print("%s             + NOTE of what I THINK IT <<<SHOULD>>> DO :  %s" % (purpura, neutro))                
            print("%s                     + If Order Type = `NONE YET` then we should accept the order as a new sell, DON'T add it to stats, reset the assetprevsession and somewhat calculate profits  %s" % (purpura, neutro))                
            print("%s                     + If Order Type = `BUY` then as we add it to stats and calculate profit. Maybe slippage aswell? %s" % (purpura, neutro))                
            print("%s                     + If Order Type = `SELL` then as we are in sell, probably we are just RETRYING. We don't add it to stats, we don't calculate profit. Maybe yes slippage  %s" % (purpura, neutro))                
            print("%s     - Do we still hold assets from a previous session? (1 or 0) AssetPrevSession=%s %s" % (purpura,shared.AssetPrevSession[shared.Nsymbol],neutro))
            print("%s     - The LimitPrice we used in the sell order (this last signal)was %s %s" % (purpura, shared.LimitPrice[shared.Nsymbol],neutro)
            print("%s     - The LastOrderPrice we stored with the price at what the previous order was executed was %s %s" % (purpura, shared.LastOrderPrice[shared.Nsymbol],neutro)
            print("")


        # it is clear we don't have more money here to sell but we have to update the statistics. And those statistics depend on the previous states.
            
        if shared.LastOrderType[shared.Nsymbol] == 'buy':               
            if shared.LimitPrice[shared.Nsymbol] > shared.LastOrderPrice[shared.Nsymbol]:
                if shared.LastOrderPrice[shared.Nsymbol]>0:
                    print("%sProfitable operation: We bought at %s and now we sell at %s [PCT = %s]%s" % (rojo,shared.LastOrderPrice[shared.Nsymbol],shared.LimitPrice[shared.Nsymbol],format(float(shared.LimitPrice[shared.Nsymbol]/shared.LastOrderPrice[shared.Nsymbol]-1)*100,'.2f'),neutro))
                shared.CorrectSells[shared.Nsymbol]=shared.CorrectSells[shared.Nsymbol]+1
            else:
                if shared.LastOrderPrice[shared.Nsymbol]>0:
                    print("%sNOT Profitable operation: We bought at %s and now we sell at %s [PCT = %s]%s" % (rojo,shared.LastOrderPrice[shared.Nsymbol],shared.LimitPrice[shared.Nsymbol],format(float(shared.LimitPrice[shared.Nsymbol]/shared.LastOrderPrice[shared.Nsymbol]-1)*100,'.2f'),neutro))
            shared.PointsEarned[shared.Nsymbol]=shared.PointsEarned[shared.Nsymbol]+points()
            
            
        shared.TotalSells=shared.TotalSells+1
        shared.SellsPerAsset[shared.Nsymbol]=shared.SellsPerAsset[shared.Nsymbol]+1
            
        shared.LastOrderPrice[shared.Nsymbol]=shared.LimitPrice[shared.Nsymbol]
        shared.LimitSlippage[shared.Nsymbol]=shared.LimitSlippage[shared.Nsymbol]+(shared.price/shared.LimitPrice[shared.Nsymbol]-1)*100*-1   # no estoy seguro ??
        shared.LastOrderType[shared.Nsymbol]="sell"    
        shared.LimitOrderSince[shared.Nsymbol]=0                    
        shared.AssetPrevSession[shared.Nsymbol]=0
        print("Finished")                             


            
   

def ice_buy():
    
    # If we don't have any asset we want to buy a PARTE, but only that
    
    if shared.assets < 0.0001 : 
        buying=True
        selling=False
    else:
        buying=False
        selling=False
        print("%sWe already have enough %s %s" % (amarillo,shared.symbol,neutro))        
        
    while buying:

        PAIR   = shared.symbol
        RATE   = shared.price*(1+shared.PriceOverlap)
        AMOUNT = float(shared.PARTE/shared.price)
        
        # We buy under the following conditions:
        #          + When we have enough currency to buy a PARTE
        #          + When we don't have any quantity already bought of that asset
        #          + Always that we cover at least the amount required by the exchange
        
        print("Displaying DEBUGGING data for buy order for pair: %s   RATE: %s  AMOUNT:  %s   [curr: %s | price: %s | assets: %s]" % ( PAIR , RATE , AMOUNT , shared.curr , shared.price , shared.assets ))            
        if AMOUNT > 0.0001 and shared.assets < 0.0001 and shared.curr > shared.PARTE:
            print("ORDER DATA FOR PAIR: %s   RATE: %s  AMOUNT:  %s   [curr: %s | price: %s | assets: %s]" % ( PAIR , RATE , AMOUNT , shared.curr, shared.price , shared.assets ))            
            print(polo.api('buy', {'currencyPair': 'BTC_' + PAIR, 'rate': RATE , 'amount': AMOUNT }))
            time.sleep(shared.TIMEOUT)
            update_info()            
            
        else:
            
            # Here supossedly we have already bought the assets
            
            # We check the previous order:
            #         + If previous order was also a BUY is because we just didn't finish the buy and some order has been canceled and reissued again. We don't want to count those rebuys multitimes only one per buy.
            #         + If previous order type was a null then it might be the first order. We will account it but not as a WIN or LOSS
            #         + If previous order was a SELL we will check its profitability and record if it was a CorrectBuy.


            if shared.LastOrderType[shared.Nsymbol] != 'buy':
                if shared.LastOrderType[shared.Nsymbol]=='sell':
                    if shared.price < shared.LastOrderPrice[shared.Nsymbol]:
                        print("%sProfitable operation: We sold at %s and now we repurchase at %s [PCT = %s]%s" % (verde,shared.LastOrderPrice[shared.Nsymbol],shared.price,format(float(shared.LastOrderPrice[shared.Nsymbol]/shared.price-1)*100,'.2f'),neutro))
                        shared.CorrectBuys[shared.Nsymbol]=shared.CorrectBuys[shared.Nsymbol]+1
                    else:
                        print("%sNOT Profitable operation: We sold at %s and now we repurchase at %s [PCT = %s]%s" % (rojo,shared.LastOrderPrice[shared.Nsymbol],shared.price,format(float(shared.LastOrderPrice[shared.Nsymbol]/shared.price-1)*100,'.2f'),neutro))
                
                shared.TotalBuys=shared.TotalBuys+1
                shared.BuysPerAsset[shared.Nsymbol]=shared.BuysPerAsset[shared.Nsymbol]+1
                shared.PointsEarned[shared.Nsymbol]=shared.PointsEarned[shared.Nsymbol]+points()
            else:
                print("%sA buy order from previous tick was not completed%s" % (amarillo,neutro))
            shared.LastOrderType[shared.Nsymbol]="buy"
            shared.LastOrderPrice[shared.Nsymbol]=shared.price
            shared.AssetPrevSession[shared.Nsymbol]=0
            print("Finished buying")
            buying=False                

    
def ice_sell():

    # We only want to sell if we have any asset obv

    if shared.assets > 0.0001:
        selling=True
        buying=False
    else:
        selling=False
        buying=False
        print("%sWe don't have any %s to sell %s" % (amarillo, shared.symbol, neutro))
        
   
    while selling:
        if shared.assets > 0.0001:
            
            # The only requisite to sell is just have any ASSET bigger than the amount accepted by the exchange
            
            PAIR   = shared.symbol
            RATE   = shared.price*(1-shared.PriceOverlap)
            AMOUNT = shared.assets
            
            print("SELLING PAIR: %s   RATE: %s  AMOUNT:  %s" % ( PAIR , RATE , AMOUNT ))
            print(polo.api('sell', {'currencyPair':'BTC_'+ PAIR , 'rate': RATE , 'amount': AMOUNT }))
            time.sleep(shared.TIMEOUT)
            update_info()   
            
        else:
            
            # Here supossedly we have already sold the assets 
            
            # We check the previous order:
            #         + If the assets:
            #                   + Didn't came from a previous session
            #                              - We will show and account the sell profitability
            #                   + If it was a previosu buy then we will account the sell like it
            #                   + But if the previous order was a sell then it won't be accounted as it is an order that did not execute previously.
            #         + If previous order was a SELL we will check its profitability and record if it was a CorrectBuy.
            #
            #                   + Did came from a previous session: 
            #                              - We will display some informative messages and try to give some indication regarding how we have managed the received money in this session.
            #                              - Make sure it is not considered as previous session in next executions.  
            
            if shared.AssetPrevSession[shared.Nsymbol]==0:
                if shared.price > shared.LastOrderPrice[shared.Nsymbol]:
                    print("%sProfitable operation: We bought at %s and now we sell at %s [PCT = %s]%s" % (rojo,shared.LastOrderPrice[shared.Nsymbol],shared.price,format(float(shared.price/shared.LastOrderPrice[shared.Nsymbol]-1)*100,'.2f'),neutro))
                    if shared.LastOrderType[shared.Nsymbol]=="buy":
                        shared.CorrectSells[shared.Nsymbol]=shared.CorrectSells[shared.Nsymbol]+1
                else:
                    print("%sNOT Profitable operation: We bought at %s and now we sell at %s [PCT = %s]%s" % (rojo,shared.LastOrderPrice[shared.Nsymbol],shared.price,format(float(shared.price/shared.LastOrderPrice[shared.Nsymbol]-1)*100,'.2f'),neutro))

                
                
                if shared.LastOrderType[shared.Nsymbol]=="buy":
                    shared.TotalSells=shared.TotalSells+1
                    shared.SellsPerAsset[shared.Nsymbol]=shared.SellsPerAsset[shared.Nsymbol]+1
                    shared.PointsEarned[shared.Nsymbol]=shared.PointsEarned[shared.Nsymbol]+points()
                if shared.LastOrderType[shared.Nsymbol]=="sell":
                    print("%sA sell order from previous tick was not completed%s" % (amarillo,neutro))
                    
                shared.LastOrderType[shared.Nsymbol]="sell"
                shared.LastOrderPrice[shared.Nsymbol]=shared.price
            else:
                print("%sSelling some assets from previous session. Real benefit Unknown.%s" % (amarillo,neutro))
                print("%sTHIS SELL WILL NOT BE ACCOUNTED IN THE STATISTICS.%s" % (amarillo,neutro))                
                if shared.price > shared.stprice[shared.Nsymbol]:
                    print("%sProfitable operation: Price when bot started was %s and now we sell at %s [PCT = %s]%s" % (verde,shared.stprice[shared.Nsymbol],shared.price,format(float(shared.price/shared.stprice[shared.Nsymbol]-1)*100,'.2f'),neutro))
                else:
                    print("%sPrice when bot started was %s and now we sell at %s [PCT = %s]%s" % (rojo,shared.stprice[shared.Nsymbol],shared.price,format(float(shared.price/shared.stprice[shared.Nsymbol]-1)*100,'.2f'),neutro))
                print("%sWe will include this asset in the stats from now on%s" % (amarillo,neutro))
                shared.AssetPrevSession[shared.Nsymbol] = 0
            
            selling=False
            print("Finished selling")
            


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
            for allsymbols in parameters.SYMBOLS:
                shared.net=shared.net+float(val2[allsymbols]['btcValue'])
            shared.PARTE=float(shared.net/(len(parameters.SYMBOLS)+0.33))
            if shared.enabled==1:
                print("%sPart now is %s.%s" % (amarillo,format(shared.PARTE,'4f'),neutro))
        except ZeroDivisionError:
            shared.net=0
        shared.total=shared.net
        shared.price=shared.ticker     
        shared.AssetPrevSession[shared.Nsymbol]=0
        if shared.TICK==1 and shared.JUST_STARTED==0:
            if shared.enabled==1:
                print("%sWe are on tick %s so storing starting balance data. Orders won't be executed during this first tick. %s" % (amarillo,shared.TICK,neutro))
            shared.stassets.append(shared.assets)
            shared.stcurr.append(shared.curr)
            shared.stnet.append(shared.net)
            shared.sttotal.append(shared.total)
            shared.stprice.append(shared.price)
            
            if shared.assets>0:
                if shared.enabled==1:
                    print("%sWe have some assets from previous sessions: %s %s %s" %(amarillo,shared.assets,shared.symbol,neutro))
                shared.AssetPrevSession[shared.Nsymbol]=1
            
    except:
        if shared.TICK==1:
            print("CRITICAL: there was a problem getting the ticker or the balance information.")
            print("Please restart and make sure that at least the first tick works properly.")
            shared.running=False
        else:
            print("ERROR: there was a problem getting the ticker or the balance information.")
        if shared.DEBUG  or shared.DEBUG_UPDATER:
            raise

    return 1

def points():
    if shared.LastOrderPrice[shared.Nsymbol]==0:
        BenefLastTrade=0
    else:
        BenefLastTrade=0
        if shared.LastOrderType[shared.Nsymbol]=="buy":
            BenefLastTrade=float((shared.price/shared.LastOrderPrice[shared.Nsymbol]-1)*100)
        if shared.LastOrderType[shared.Nsymbol]=="sell":
            BenefLastTrade=float((shared.price/shared.LastOrderPrice[shared.Nsymbol]-1)*100*-1)        
    return BenefLastTrade


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
        print("ERROR: There was an unexpected problem when downloading the historical bars from the exchange")
        if shared.DEBUG or shared.DEBUG_BROKER:
            raise
        
            
            
    
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
        print("ERROR: error cancelling open orders in market %s. We can do it in next tick" % shared.symbol)                
        if shared.DEBUG or shared.DEBUG_BROKER:
            raise

    
    
            
    
    
    shared.ck=calculate_close(shared.NUMVELAS)
    
    update_info()
    
    try:
        if shared.CheckCode==False:
            ActualBalanceBTC=shared.net
            StartBalanceBTC=shared.stnet[shared.Nsymbol]
            ProfitBalanceBTC=(ActualBalanceBTC/StartBalanceBTC-1)*100            

            ActualBalanceAST=shared.net/shared.price
            StartBalanceAST=shared.stnet[shared.Nsymbol]/shared.stprice[shared.Nsymbol]
            ProfitBalanceAST=(ActualBalanceAST/StartBalanceAST-1)*100
            
            ProfitBH=(shared.price/shared.stprice[shared.Nsymbol]-1)*100
            col=""
            if shared.assets>0.0001:
                col=purpura
            
            print("Balance now consists in %s BTC and %s %s %s [%s BTC]%s " % (format(shared.curr,'.4f'),col,format(shared.assets,'.4f'),shared.symbol,format(shared.assets*shared.price,'.4f'),neutro))
            col=""
            if ProfitBalanceBTC<0:
                col=rojo
            if ProfitBalanceBTC>0:
                col=verde
            print("Actual Balance in BTC: %s | Start Balance in BTC: %s | PCT Profit: %s %s %s" % (format(ActualBalanceBTC,'.4f'), format(StartBalanceBTC,'.4f') , col,format(ProfitBalanceBTC,'.4f'),neutro ))
            col=""
            if ProfitBalanceAST<0:
                col=rojo
            if ProfitBalanceAST>0:
                col=verde
            print("Actual Balance in %s: %s | Start Balance in %s: %s | PCT Profit: %s %s %s" % (shared.symbol,format(ActualBalanceAST,'.4f'),shared.symbol,format(StartBalanceAST,'.4f'),col,format(ProfitBalanceAST,'.4f'),neutro ))
            col=""
            if ProfitBH<0:
                col=rojo
            if ProfitBH>0:
                col=verde
            print("Buy & Hold Profit: %s %s%s [start: %s / now: %s]" % (col,format(ProfitBH,'.4f'),neutro,shared.stprice[shared.Nsymbol],shared.price ))

            print("Actual %sBTC value: %s | ck value: %s" % (shared.symbol,format(shared.ticker,'.8f'),format(shared.ck[-1],'.8f')))
            col=""
            BenefLastTrade=points()
            if BenefLastTrade<0:
                col=rojo
            if BenefLastTrade>0:
                col=verde
                
            AcumulatedPoints = shared.PointsEarned[shared.Nsymbol] + BenefLastTrade
            
            col2=gris
            if AcumulatedPoints > 0:
                col2=verde
            if AcumulatedPoints < 0:
                col2=rojo
            print("Last Order: %s at %s [PCT Profit: %s %s %s (Acumul: %s %s %s) ]" % (shared.LastOrderType[shared.Nsymbol],shared.LastOrderPrice[shared.Nsymbol],col,format(BenefLastTrade,'.4f'), neutro, col2, format(AcumulatedPoints,'.4f'),neutro))


    except:
        print("ERROR: Something failed when tried to get the user ticker/balance")
        if shared.DEBUG or shared.DEBUG_BROKER:
            raise
        
    try:
        if shared.CheckCode==False:
            if os.name=='nt':
                f=csv.writer(open("c:/Amibroker/Formulas/CSV_Tickers/stats_PO_MultiZLDEMA_"+shared.symbol+"BTC_15m.csv","a+"),delimiter=';')
                f.writerow([time.strftime("%Y-%m-%d %H:%M") , shared.ticker, shared.net, shared.net/shared.ticker, shared.total])
            else:
                f=csv.writer(open("/home/CSV_Tickers/stats_PO_MultiZLDEMA_"+shared.symbol+"BTC_5m.csv","a+"),delimiter=';')
                f.writerow([time.strftime("%Y-%m-%d %H:%M") , shared.ticker, shared.net, shared.net/shared.ticker, shared.total])
    except:
        print("ERROR: Could not export performance stats to file. Have you got the CSV file opened?")
        if shared.DEBUG or shared.DEBUG_EXPORT_CSV:
            raise
        


    
def main_algo():
    try:
        
        if shared.ALGO=="MultiZLDEMA":
            


            
            
    
            z1=common.ZLDEMA(shared.ck,shared.P1)
            z2=common.ZLDEMA(shared.ck,shared.P2)
            z3=common.ZLDEMA(shared.ck,shared.P3)
            z4=common.ZLDEMA(shared.ck,shared.P4)
            
            
            vZLD_B =  z1 > z2
            vZLD_S =  z3 < z4
            
            
            buy  = common.MUX2(vZLD_B,vZLD_S,shared.sel1)
            sell = common.MUX2(vZLD_B,vZLD_S,shared.sel2)
            
            shared.sig=0
            if buy :
                shared.sig =  1
                print("%sThe signal is %s (ZLD1[%s]=%s > ZLD2[%s]=%s ; ZLSD3[%s]=%s < ZLD4[%s]=%s ) %s" % (verde,shared.sig,shared.P1,format(z1,'.6f'),shared.P2,format(z2,'.6f'),shared.P3,format(z3,'.6f'),shared.P4,format(z4,'.6f'),neutro))
            if sell :
                shared.sig = -1
                print("%sThe signal is %s (ZLD1[%s]=%s > ZLD2[%s]=%s ; ZLSD3[%s]=%s < ZLD4[%s]=%s ) %s" % (rojo,shared.sig,shared.P1,format(z1,'.6f'),shared.P2,format(z2,'.6f'),shared.P3,format(z3,'.6f'),shared.P4,format(z4,'.6f'),neutro))
            if shared.sig == 0:
                print("The signal is %s (ZLD1[%s]=%s > ZLD2[%s]=%s ; ZLSD3[%s]=%s < ZLD4[%s]=%s)" % (shared.sig,shared.P1,format(z1,'.6f'),shared.P2,format(z2,'.6f'),shared.P3,format(z3,'.6f'),shared.P4,format(z4,'.6f')))
    except:
        print("ERROR: Problem during Main Algo execution")
        if shared.DEBUG or shared.DEBUG_MAIN_ALGO:
            raise

        
    if shared.sig== 1 and shared.TICK>1: 
        try:
            if parameters.LIMITORDERS==1:
                limit_buy()
            else:
                ice_buy()
        except:
            print("ERROR: There was a problem executing the BUY ORDER")
            if shared.DEBUG or shared.DEBUG_ORDERS:
                raise
                
            
        
    if shared.sig==-1 and shared.TICK>1: 
        try:
            if parameters.LIMITORDERS==1:
                limit_sell()
            else:
                ice_sell()
        except:
            print("ERROR: There was a problem executing the SELL ORDER")
            if shared.DEBUG or shared.DEBUG_ORDERS:
                raise


            



  


def main_thread():
    if shared.SHOWTABLE==False:
        print(".")
        print(".")
        print(".")
        print(".")
        print(".")
        print(".")
        
        print("Initializing main daemon at %s ...." % (time.strftime("%Y-%m-%d %H:%M:%S") ) )
        
        # Initializing all counters per asset
        
        for recorrido in parameters.SYMBOLS:
            shared.BuysPerAsset.append(0)
            shared.SellsPerAsset.append(0)
            shared.LastOrderType.append("NONE YET")
            shared.LastOrderPrice.append(0)
            shared.CorrectBuys.append(0)
            shared.CorrectSells.append(0)
            shared.AssetPrevSession.append(0)
            shared.PointsEarned.append(0)
            shared.LimitPrice.append(0)
            shared.LimitOrderSince.append(0)
            shared.LimitSlippage.append(0)

        while shared.running == True:
            shared.TICK=shared.TICK+1
            if shared.CheckCode==False:
                print("   ")
                
                print("%s********************************************************************************************************************%s" % (blanco,neutro))
                print("%sT I C K = %s  [%s H] [Model:%s] [POLONIEX 5m - %s] DEBUG: %s %s"  % (blanco,shared.TICK, format(shared.TICK/12,'.2f'), shared.ALGO,shared.ACCOUNT,shared.DEBUG,neutro))
                print("%s********************************************************************************************************************%s" % (blanco,neutro))
                
                
                
                print("Total Buys  in this session %s" % shared.TotalBuys)
                print("Total Sells in this session %s" % shared.TotalSells)
                print(" ")
            sumapoints=0
            for shared.Ksymbol in parameters.SYMBOLS:   
                col=gris
                valor=shared.PointsEarned[parameters.SYMBOLS.index(shared.Ksymbol)]
                if valor>0:
                    col=verde
                if valor<0:
                    col=rojo
                print("Total %s points = %s%s%s" % (shared.Ksymbol, col,format(valor,'.4f'),neutro))
                sumapoints=sumapoints+shared.PointsEarned[parameters.SYMBOLS.index(shared.Ksymbol)]
            col=gris
            if sumapoints>0:
                col=verde
            if sumapoints<0:
                col=rojo
            print("%sTOTAL PCT POINTS SUM = %s %s %s %s " % (blanco,neutro,col,format(sumapoints,'.4f'),neutro))
            print("")

            sumaslippage=0
            for shared.Jsymbol in parameters.SYMBOLS:   
                col=gris
                valor=shared.LimitSlippage[parameters.SYMBOLS.index(shared.Jsymbol)]
                print("Total %s slippage = %s%s%s" % (shared.Jsymbol, rojo,format(valor,'.4f'),neutro))
                sumaslippage=sumaslippage+shared.LimitSlippage[parameters.SYMBOLS.index(shared.Jsymbol)]
            print("%sTOTAL PCT SLIPPAGE SUM = %s %s %s %s " % (blanco,neutro,rojo,format(sumaslippage,'.4f'),neutro))
            print("")
            
            
            for shared.symbol in parameters.SYMBOLS:
                
#PUNTO A                
                
                shared.Nsymbol=parameters.SYMBOLS.index(shared.symbol) 
                WinBuys=0
                WinSells=0
                RestaBuy=0 
                RestaSell=0                
                #  Why not 0? Because i don't want to include the first buy in the percent of Wins or Buys, but only after there has really been a loss or a win
                #  The rationale is that when we start buying the first time we have ONE buy but it has not been sold yet so the stat is not real
                #  Possibilities:
                #       - we ar on tick 2 and we have a buy signal so we buy. 
                #       - so we only count "transactions" buy

                if shared.BuysPerAsset[shared.Nsymbol] > 1:
                    if shared.LastOrderType=="buy":    # we have the actual order open so we don't count it.
                        RestaBuy=1
                    WinBuys=float(shared.CorrectBuys[shared.Nsymbol]/(shared.BuysPerAsset[shared.Nsymbol]-RestaBuy))*100
                else:
                    WinBuys=0
                
    
                if shared.SellsPerAsset[shared.Nsymbol] > 1:  
                    if shared.LastOrderType=="sell":    #we have the actual order open so we don't count it.
                        RestaSell=1
                    WinSells=float(shared.CorrectSells[shared.Nsymbol]/(shared.SellsPerAsset[shared.Nsymbol]-RestaSell))*100
                else:
                    WinSells=0
                

                importlib.reload(parameters)   
            
                shared.P1=parameters.carga_vars(shared.symbol,'P1')
                shared.P2=parameters.carga_vars(shared.symbol,'P2')
                shared.P3=parameters.carga_vars(shared.symbol,'P3')
                shared.P4=parameters.carga_vars(shared.symbol,'P4')
                shared.sel1=parameters.carga_vars(shared.symbol,'sel1')
                shared.sel2=parameters.carga_vars(shared.symbol,'sel2')
                shared.enabled=parameters.carga_vars(shared.symbol,'enabled')

                if shared.enabled==1:
                    print("%sACTUAL MARKET BTC_%s  Idx: %s [%s] %s" % (blanco,shared.symbol, shared.Nsymbol,time.strftime("%Y-%m-%d %H:%M"),neutro) )
                    print("--------------------------------------------------------------------------------------------------------------------")
                    
                    print("%s Closed BUYS : ( Winners = %s / Total = %s ) = Profitable %s pct" % (shared.symbol,shared.CorrectBuys[shared.Nsymbol],shared.BuysPerAsset[shared.Nsymbol]-RestaBuy,format(WinBuys,'.2f')))
                    print("%s Closed SELLS: ( Winners = %s / Total = %s ) = Profitable %s pct" % (shared.symbol,shared.CorrectSells[shared.Nsymbol],shared.SellsPerAsset[shared.Nsymbol]-RestaSell,format(WinSells,'.2f')))
                    print("%s[%s PARAMETERS] %s %s %s %s %s %s %s" %(blanco,shared.symbol,shared.P1,shared.P2,shared.P3,shared.P4,shared.sel1,shared.sel2,neutro))
                    
                    try:
                        broker_update()
                        main_algo()
                        print(" ")
                    except:
                        print("ERROR: There was an unexpected error this tick. Retrying in next tick")
                        if shared.DEBUG or shared.DEBUG_BROKER or shared.DEBUG_MAIN_ALGO or shared.DEBUG_ORDERS or shared.DEBUG_UPDATER or shared.DEBUG_EXPORT_CSV:
                            raise
                    time.sleep(20)
                else:
                    print("%s...%s" % (blanco,neutro))
                    print(" ")
                    if shared.TICK==1:
                        update_info()
                 
            
            if shared.CheckCode==False:
                print("")
                print("")
                print("%sTick processing ended at %s. Waiting %s Minutes for next tick%s" % (amarillo,time.strftime("%Y-%m-%d %H:%M:%S"),shared.FRECUENCIA_MINUTOS,neutro))

            if shared.JUST_STARTED==0:
                shared.JUST_STARTED=1
                
            
            time.sleep(300-time.time()%300)


        
if __name__ == "__main__":
    main_thread()        