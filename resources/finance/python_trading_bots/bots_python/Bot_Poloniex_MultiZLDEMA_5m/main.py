import json
import talib
import math
import random
import numpy as np

import os
import time
import importlib

from random import randint

import globales

import sys
sys.path.append('/home/Comun')
import parameters
import poloniex
import common

import talib    
        
    

# ##################################################
try:
    ACCOUNT=sys.argv[1]
except:
    print("The script needs to receive an argument with the poloniex account or it will fail: guayaba, ariadna, dna48")
print("ACCOUNT: %s" %ACCOUNT)

SYMBOLS = parameters.carga_accountsymbols(ACCOUNT)
# ##################################################



polo=poloniex.Poloniex(parameters.carga_APIKey(ACCOUNT,"API_KEY"),parameters.carga_APIKey(ACCOUNT,"API_SECRET"))


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
    PricePctDiff=0
    update_info() 
    RATE   = globales.PRICE * (1-parameters.DentInOrderBook)
    AMOUNT = float(parameters.PARTE/RATE)
    if parameters.VERBOSE==True:
        print ("%sLast limit order pending for %s ticks %s" % (amarillo,globales.LIMIT_ORDER_SINCE[globales.NSYMBOL],neutro))
    if AMOUNT > parameters.MIN_ALLOWED_ASSETS and globales.ASSETS < parameters.MIN_ALLOWED_ASSETS and globales.CURR > parameters.PARTE:
        if globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]==0:
            globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]=1
            globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]=RATE
            if parameters.VERBOSE==True:
                print ("%sBuy order initiated in this tick, storing LimitOrderSince=1 and LimitPrice %s" % (purpura,neutro))
        else:
            globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]=globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]+1                    
            print("%s- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - %s" % (amarillo,neutro))
            print("%sThis BUY order could not be executed in %s ticks. RETRYING%s" %(amarillo,globales.LIMIT_ORDER_SINCE[globales.NSYMBOL],neutro) )
            if globales.LIMIT_ORDER_PRICE[globales.NSYMBOL] > 0:
                PricePctDiff=(globales.PRICE/globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]-1)*100
                print("%sThe original price was %s . Now it is %s . Diff is %s %% %s" % (amarillo,format(globales.LIMIT_ORDER_PRICE[globales.NSYMBOL],'.8f'),format(globales.PRICE,'.8f'),format(PricePctDiff,'.4f'),neutro) )                
            print("%s- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - %s" % (amarillo,neutro))        
        if PricePctDiff < parameters.CancelBuyWhenSlippageOver:
            print("BUYING PAIR: %s   RATE: %s  AMOUNT:  %s   [curr: %s | price: %s | assets: %s]" % ( globales.SYMBOL , RATE , AMOUNT , globales.CURR, globales.PRICE , globales.ASSETS ))            
            print(polo.api('buy', {'currencyPair': globales.PAIR_CURR+'_' + globales.SYMBOL, 'rate': RATE , 'amount': AMOUNT, 'postOnly': parameters.POST_ONLY }))
        else:
            print("%s[WARNING] I am not sending the BUY order with an actual %s slippage over the configured limit of %s . Waiting for a better price. %s" % (purpura, format(PricePctDiff,'.4f'), format(parameters.CancelBuyWhenSlippageOver,'.4f'),neutro))
    else:
        if globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]>0:
            if globales.LAST_ORDER_PRICE[globales.NSYMBOL] > globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]:
                if globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]>0:
                    print("%sProfitable operation: We sold at %s and now we repurchase at %s [ %s %% ]%s" % (verde,globales.LAST_ORDER_PRICE[globales.NSYMBOL],globales.LIMIT_ORDER_PRICE[globales.NSYMBOL],format(float(globales.LAST_ORDER_PRICE[globales.NSYMBOL]/globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]-1)*100,'.4f'),neutro))
                    if globales.LAST_ORDER_PRICE[globales.NSYMBOL] > 0:
                        globales.POINTS_EARNED[globales.NSYMBOL]=globales.POINTS_EARNED[globales.NSYMBOL]+float(globales.LAST_ORDER_PRICE[globales.NSYMBOL]/globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]-1)*100
            else:
                if globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]>0:
                    print("%sNOT Profitable operation: We sold at %s and now we repurchase at %s [ %s %% ]%s" % (rojo,globales.LAST_ORDER_PRICE[globales.NSYMBOL],globales.LIMIT_ORDER_PRICE[globales.NSYMBOL],format(float(globales.LAST_ORDER_PRICE[globales.NSYMBOL]/globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]-1)*100,'.4f'),neutro))
                    if globales.LAST_ORDER_PRICE[globales.NSYMBOL] > 0:
                        globales.POINTS_EARNED[globales.NSYMBOL]=globales.POINTS_EARNED[globales.NSYMBOL]+float(globales.LAST_ORDER_PRICE[globales.NSYMBOL]/globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]-1)*100
            globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]=0
            globales.LAST_ORDER_PRICE[globales.NSYMBOL]=globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]
            globales.LAST_ORDER_TYPE[globales.NSYMBOL]=="buy"


def market_buy():

    PricePctDiff=0
    
    if globales.ASSETS < parameters.MIN_ALLOWED_ASSETS:
        buying=True
        selling=False
    else:
        buying=False
        selling=False
        print("%sWe already have enough %s %s" % (amarillo,globales.SYMBOL,neutro))        
        
    while buying:    
    
        update_info() 
        RATE   = globales.PRICE * (1-parameters.DentInOrderBook)
        AMOUNT = float(parameters.PARTE/RATE)
        if AMOUNT > parameters.MIN_ALLOWED_ASSETS and globales.ASSETS < parameters.MIN_ALLOWED_ASSETS and globales.CURR > parameters.PARTE:
            if globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]==0:
                globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]=1
                globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]=RATE
                if parameters.VERBOSE==True:
                    print ("%sBuy order initiated in this tick, storing LimitOrderSince=1 and LimitPrice %s" % (purpura,neutro))
            else:
                globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]=globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]+1                    
                print("%s- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - %s" % (amarillo,neutro))
                print("%sThis BUY order could not be executed in %s market buy retries. RETRYING%s" %(amarillo,globales.LIMIT_ORDER_SINCE[globales.NSYMBOL],neutro) )
                if globales.LIMIT_ORDER_PRICE[globales.NSYMBOL] > 0:
                    PricePctDiff=(globales.PRICE/globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]-1)*100
                    print("%sThe original price was %s . Now it is %s . Diff is %s %% %s" % (amarillo,format(globales.LIMIT_ORDER_PRICE[globales.NSYMBOL],'.8f'),format(globales.PRICE,'.8f'),format(PricePctDiff,'.4f'),neutro) )                
                print("%s- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - %s" % (amarillo,neutro))        
            if PricePctDiff < parameters.CancelBuyWhenSlippageOver:
                print("BUYING PAIR: %s   RATE: %s  AMOUNT:  %s   [curr: %s | price: %s | assets: %s]" % ( globales.SYMBOL , RATE , AMOUNT , globales.CURR, globales.PRICE , globales.ASSETS ))            
                print(polo.api('buy', {'currencyPair': globales.PAIR_CURR+'_' + globales.SYMBOL, 'rate': RATE , 'amount': AMOUNT}))
            else:
                print("%s[WARNING] I am not sending the BUY order with an actual %s slippage over the configured limit of %s . Waiting for a better price. %s" % (purpura, format(PricePctDiff,'.4f'), format(parameters.CancelBuyWhenSlippageOver,'.4f'),neutro))
        else:
            if globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]>0:
                if globales.LAST_ORDER_PRICE[globales.NSYMBOL] > globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]:
                    if globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]>0:
                        print("%sProfitable operation: We sold at %s and now we repurchase at %s [ %s %% ]%s" % (verde,globales.LAST_ORDER_PRICE[globales.NSYMBOL],globales.LIMIT_ORDER_PRICE[globales.NSYMBOL],format(float(globales.LAST_ORDER_PRICE[globales.NSYMBOL]/globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]-1)*100,'.4f'),neutro))
                        if globales.LAST_ORDER_PRICE[globales.NSYMBOL] > 0:
                            globales.POINTS_EARNED[globales.NSYMBOL]=globales.POINTS_EARNED[globales.NSYMBOL]+float(globales.LAST_ORDER_PRICE[globales.NSYMBOL]/globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]-1)*100
                else:
                    if globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]>0:
                        print("%sNOT Profitable operation: We sold at %s and now we repurchase at %s [ %s %% ]%s" % (rojo,globales.LAST_ORDER_PRICE[globales.NSYMBOL],globales.LIMIT_ORDER_PRICE[globales.NSYMBOL],format(float(globales.LAST_ORDER_PRICE[globales.NSYMBOL]/globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]-1)*100,'.4f'),neutro))
                        if globales.LAST_ORDER_PRICE[globales.NSYMBOL] > 0:
                            globales.POINTS_EARNED[globales.NSYMBOL]=globales.POINTS_EARNED[globales.NSYMBOL]+float(globales.LAST_ORDER_PRICE[globales.NSYMBOL]/globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]-1)*100
                globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]=0
                globales.LAST_ORDER_PRICE[globales.NSYMBOL]=globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]
                globales.LAST_ORDER_TYPE[globales.NSYMBOL]=="buy"    
        buying=False
        print("Market Buy finished")
    



def limit_sell():
    PricePctDiff=0
    update_info() 
    RATE   = globales.PRICE * (1+parameters.DentInOrderBook)
    AMOUNT = globales.ASSETS
    if parameters.VERBOSE==True:
        print ("%sLast limit order pending for %s ticks %s" % (amarillo,globales.LIMIT_ORDER_SINCE[globales.NSYMBOL],neutro))
    if globales.ASSETS > parameters.MIN_ALLOWED_ASSETS:
        if globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]==0:
            globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]=1
            globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]=RATE
            if parameters.VERBOSE==True:
                print ("%sSell order initiated in this tick, storing LimitOrderSince=1 and LimitPrice %s" % (purpura,neutro))
        else:
            globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]=globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]+1                                    
            print("%s- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - %s" % (amarillo,neutro))
            print("%sThis SELL order could not be executed in %s ticks. RETRYING%s" %(amarillo, globales.LIMIT_ORDER_SINCE[globales.NSYMBOL] ,neutro) )
            if globales.PRICE > 0:
                PricePctDiff=(globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]/globales.PRICE-1)*100
                print("%sThe original price was %s . Now it is %s . Diff is %s %% %s" % (amarillo,format(globales.LIMIT_ORDER_PRICE[globales.NSYMBOL],'.8f'),format(globales.PRICE,'.8f'),format(PricePctDiff,'.4f'),neutro) )                
            print("%s- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - %s" % (amarillo,neutro))
        if PricePctDiff < parameters.CancelSellWhenSlippageOver:            
            print("SELLING PAIR: %s   RATE: %s  AMOUNT:  %s    [curr: %s | price: %s | assets: %s]" % ( globales.SYMBOL , RATE , AMOUNT , globales.CURR, globales.PRICE , globales.ASSETS ))
            print(polo.api('sell', {'currencyPair': globales.PAIR_CURR+'_'+ globales.SYMBOL , 'rate': RATE , 'amount': AMOUNT, 'postOnly': parameters.POST_ONLY }))   
        else:
            print("%s[WARNING] I am not sending the SELL order with an actual %s slippage over the configured limit of %s . Waiting for a better price. %s" % (purpura, format(PricePctDiff,'.4f'), format(parameters.CancelSellWhenSlippageOver,'.4f'),neutro))
        
        
    else:
        if globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]>0:
            if globales.LIMIT_ORDER_PRICE[globales.NSYMBOL] > globales.LAST_ORDER_PRICE[globales.NSYMBOL]:
                if globales.LAST_ORDER_PRICE[globales.NSYMBOL]>0:
                    print("%sProfitable operation: We bought at %s and now we sell at %s [ %s %% ]%s" % (verde,globales.LAST_ORDER_PRICE[globales.NSYMBOL],globales.LIMIT_ORDER_PRICE[globales.NSYMBOL],format(float(globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]/globales.LAST_ORDER_PRICE[globales.NSYMBOL]-1)*100,'.4f'),neutro))
                    globales.POINTS_EARNED[globales.NSYMBOL]=globales.POINTS_EARNED[globales.NSYMBOL]+float(globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]/globales.LAST_ORDER_PRICE[globales.NSYMBOL]-1)*100
            else:
                if globales.LAST_ORDER_PRICE[globales.NSYMBOL]>0:
                    print("%sNOT Profitable operation: We bought at %s and now we sell at %s [ %s %% ]%s" % (rojo,globales.LAST_ORDER_PRICE[globales.NSYMBOL],globales.LIMIT_ORDER_PRICE[globales.NSYMBOL],format(float(globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]/globales.LAST_ORDER_PRICE[globales.NSYMBOL]-1)*100,'.4f'),neutro))
                    globales.POINTS_EARNED[globales.NSYMBOL]=globales.POINTS_EARNED[globales.NSYMBOL]+float(globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]/globales.LAST_ORDER_PRICE[globales.NSYMBOL]-1)*100
            globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]=0
            globales.LAST_ORDER_PRICE[globales.NSYMBOL]=globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]
            globales.LAST_ORDER_TYPE[globales.NSYMBOL]=="sell"


def market_sell():

    PricePctDiff=0



    if globales.ASSETS > parameters.MIN_ALLOWED_ASSETS:
        selling=True
        buying=False
        print("Market Sell initiated")
    else:
        selling=False
        buying=False
        print("%sWe don't have any %s to sell %s" % (amarillo, globales.SYMBOL, neutro))
        
   
    while selling:
        update_info() 
        RATE   = globales.PRICE * (1+parameters.DentInOrderBook)
        AMOUNT = globales.ASSETS        
        if globales.ASSETS > parameters.MIN_ALLOWED_ASSETS:
            if globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]==0:
                globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]=1
                globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]=RATE
            else:
                globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]=globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]+1                                    
                print("%s- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - %s" % (amarillo,neutro))
                print("%sThis SELL order could not be executed in %s market sell retries. RETRYING%s" %(amarillo, globales.LIMIT_ORDER_SINCE[globales.NSYMBOL] ,neutro) )
                if globales.PRICE > 0:
                    PricePctDiff=(globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]/globales.PRICE-1)*100
                    print("%sThe original price was %s . Now it is %s . Diff is %s %% %s" % (amarillo,format(globales.LIMIT_ORDER_PRICE[globales.NSYMBOL],'.8f'),format(globales.PRICE,'.8f'),format(PricePctDiff,'.4f'),neutro) )                
                print("%s- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - %s" % (amarillo,neutro))
            print("SELLING PAIR: %s   RATE: %s  AMOUNT:  %s    [curr: %s | price: %s | assets: %s]" % ( globales.SYMBOL , RATE , AMOUNT , globales.CURR, globales.PRICE , globales.ASSETS ))
            print(polo.api('sell', {'currencyPair': globales.PAIR_CURR+'_'+ globales.SYMBOL , 'rate': RATE , 'amount': AMOUNT }))  
            time.sleep(parameters.TIMEOUT)
        else:
            if globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]>0:
                if globales.LIMIT_ORDER_PRICE[globales.NSYMBOL] > globales.LAST_ORDER_PRICE[globales.NSYMBOL]:
                    if globales.LAST_ORDER_PRICE[globales.NSYMBOL]>0:
                        print("%sProfitable operation: We bought at %s and now we sell at %s [ %s %% ]%s" % (verde,globales.LAST_ORDER_PRICE[globales.NSYMBOL],globales.LIMIT_ORDER_PRICE[globales.NSYMBOL],format(float(globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]/globales.LAST_ORDER_PRICE[globales.NSYMBOL]-1)*100,'.4f'),neutro))
                        globales.POINTS_EARNED[globales.NSYMBOL]=globales.POINTS_EARNED[globales.NSYMBOL]+float(globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]/globales.LAST_ORDER_PRICE[globales.NSYMBOL]-1)*100
                else:
                    if globales.LAST_ORDER_PRICE[globales.NSYMBOL]>0:
                        print("%sNOT Profitable operation: We bought at %s and now we sell at %s [ %s %% ]%s" % (rojo,globales.LAST_ORDER_PRICE[globales.NSYMBOL],globales.LIMIT_ORDER_PRICE[globales.NSYMBOL],format(float(globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]/globales.LAST_ORDER_PRICE[globales.NSYMBOL]-1)*100,'.4f'),neutro))
                        globales.POINTS_EARNED[globales.NSYMBOL]=globales.POINTS_EARNED[globales.NSYMBOL]+float(globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]/globales.LAST_ORDER_PRICE[globales.NSYMBOL]-1)*100
                globales.LIMIT_ORDER_SINCE[globales.NSYMBOL]=0
                globales.LAST_ORDER_PRICE[globales.NSYMBOL]=globales.LIMIT_ORDER_PRICE[globales.NSYMBOL]
                globales.LAST_ORDER_TYPE[globales.NSYMBOL]=="sell"
        selling=False
        print("Market Sell finished")
       
   



def update_info():

    try:
        val=polo.api('returnTicker')
        globales.BALANCE=polo.api('returnBalances')
        globales.ASSETS=float(globales.BALANCE[globales.SYMBOL])
        globales.CURR=float(globales.BALANCE[globales.PAIR_CURR])
        try:
            val2=polo.api('returnCompleteBalances')
            globales.NET=0+float(val2[globales.PAIR_CURR]['btcValue'])
            for allsymbols in SYMBOLS:
                globales.NET=globales.NET+float(val2[allsymbols]['btcValue'])
            parameters.PARTE=float(globales.NET/(len(SYMBOLS)+0.20))
            if globales.enabled==1 and parameters.DEBUG_UPDATER==True:
                print("%sPart now is %s.%s" % (amarillo,format(parameters.PARTE,'4f'),neutro))
        except ZeroDivisionError:
            globales.NET=0
        globales.TOTAL=globales.NET


        globales.PRICE=float(val[globales.PAIR_CURR+'_'+globales.SYMBOL]['last'])
        if globales.TICK==1 and globales.JUST_STARTED==0:
            if globales.enabled==1:
                print("%sWe are on tick %s so storing starting balance data. Orders won't be executed during this first tick. %s" % (amarillo,globales.TICK,neutro))
            globales.STNET.append(globales.NET)
            globales.STPRICE.append(globales.PRICE)
            #globales.LAST_ORDER_PRICE[globales.NSYMBOL]=globales.PRICE           # nuevo !
            if globales.ASSETS > parameters.MIN_ALLOWED_ASSETS:                  # nuevo !
                globales.LAST_ORDER_TYPE[globales.NSYMBOL]="buy"                 # mievp !
            if globales.ASSETS < parameters.MIN_ALLOWED_ASSETS:                  # nuevo !
                globales.LAST_ORDER_TYPE[globales.NSYMBOL]="sell"                # mievp !                
            
    except:
        if globales.TICK==1:
            print("CRITICAL: there was a problem getting the ticker or the balance information.")
            print("Please restart and make sure that at least the first tick works properly.")
            parameters.RUNNING=False
        else:
            print("ERROR: there was a problem getting the ticker or the balance information.")
        if parameters.DEBUG  or parameters.DEBUG_UPDATER:
            raise

    return 1




def broker_update():

    
    def calculate_close(period):
        valor=[]
        for x in reversed(range(1,period+1)):
            valor.append(bars[-x]['close'])
        valor2=np.array(valor,dtype='float')
        return valor2    
    

    
    try:
        bars=polo.directpublic('https://poloniex.com/public?command=returnChartData&currencyPair='+globales.PAIR_CURR+'_'+globales.SYMBOL+'&start=1469404801&end=9999999999&period='+str(parameters.MINUTE_FREQUENCY*60))
        if parameters.DEBUG_UPDATER==True:
            print("%sThe number of bars imported from the exchange is %s %s" % (amarillo, len(bars),neutro))
            

    except:
        print("ERROR: There was an unexpected problem when downloading the historical bars from the exchange")
        if parameters.DEBUG or parameters.DEBUG_BROKER:
            raise
        
            
            
    
    try:
        OpenOrders=polo.api('returnOpenOrders',{'currencyPair': globales.PAIR_CURR+'_'+globales.SYMBOL})
        #print(OpenOrders)
        numOrders= len(OpenOrders)  
        if numOrders>0:
            
            print("%sWe have %s orders to close %s" % (amarillo,numOrders,neutro))
            for x in reversed(range(1,numOrders+1)):
                actual=str(OpenOrders[-x]['orderNumber'])
                print("%sClosing order %s %s" % (amarillo,actual,neutro))
                print(polo.api('cancelOrder',{'currencyPair': globales.PAIR_CURR+'_'+globales.SYMBOL,'orderNumber':actual}))
            print("%sEnded closing orders %s" %(amarillo,neutro))
    except:
        print("ERROR: error cancelling open orders in market %s. We can do it in next tick" % globales.SYMBOL)                
        if parameters.DEBUG or parameters.DEBUG_BROKER:
            raise

    
    
            
    
    
    globales.CK=calculate_close(globales.NUMVELAS)
    

    
    update_info()
    
    try:

        ActualBalanceCURR=globales.NET
        StartBalanceCURR=globales.STNET[globales.NSYMBOL]
        ProfitBalanceCURR=(ActualBalanceCURR/StartBalanceCURR-1)*100            

        ActualBalanceAST=globales.NET/globales.PRICE
        StartBalanceAST=globales.STNET[globales.NSYMBOL]/globales.STPRICE[globales.NSYMBOL]
        ProfitBalanceAST=(ActualBalanceAST/StartBalanceAST-1)*100
        
        ProfitBH=(globales.PRICE/globales.STPRICE[globales.NSYMBOL]-1)*100
        col=""
        if globales.ASSETS>parameters.MIN_ALLOWED_ASSETS:
            col=purpura
        
        print("Balance now consists in %s %s and %s %s %s [%s %s]%s " % (format(globales.CURR,'.4f'),globales.PAIR_CURR,col,format(globales.ASSETS,'.4f'),globales.SYMBOL,format(globales.ASSETS * globales.PRICE,'.4f'),globales.PAIR_CURR,neutro))
        col=""
        if ProfitBalanceCURR<0:
            col=rojo
        if ProfitBalanceCURR>0:
            col=verde
        if StartBalanceCURR==0:
            print("%sDid you start the bot without any money in the exchange account?%s" %(purpura,neutro))
        else:
            print("Equivalent Balance in %s: %s | Start Balance in %s: %s | Profit:%s %s %% %s" % (globales.PAIR_CURR,format(ActualBalanceCURR,'.4f'),globales.PAIR_CURR, format(StartBalanceCURR,'.4f') , col,format(ProfitBalanceCURR,'.4f'),neutro ))
        col=""
        if ProfitBalanceAST<0:
            col=rojo
        if ProfitBalanceAST>0:
            col=verde
        print("Equivalent Balance in %s: %s | Start Balance in %s: %s | Profit:%s %s %% %s" % (globales.SYMBOL,format(ActualBalanceAST,'.4f'),globales.SYMBOL,format(StartBalanceAST,'.4f'),col,format(ProfitBalanceAST,'.4f'),neutro ))
        col=""
        if ProfitBH<0:
            col=rojo
        if ProfitBH>0:
            col=verde
        print("Buy & Hold Profit:%s %s %% %s [start: %s / now: %s]" % (col,format(ProfitBH,'.4f'),neutro,globales.STPRICE[globales.NSYMBOL], globales.PRICE ))
        if globales.CK[-1]>0:
            print("Actual %s_%s close value: %s | Previous value was : %s" % (globales.PAIR_CURR,globales.SYMBOL,format(globales.PRICE,'.8f'),format(globales.CK[-1],'.8f')))
        else:
            print("Actual %s_%s close value: %s " % (globales.PAIR_CURR,globales.SYMBOL,format(globales.PRICE,'.8f')))

        col=gris
        PctBenefit=points()
        if PctBenefit > 0:
            col=verde
        if PctBenefit < 0:
            col=rojo

        PctBenefitAcum=globales.POINTS_EARNED[globales.NSYMBOL] + PctBenefit

        col2=gris
        if PctBenefitAcum > 0:
            col2=verde
        if PctBenefitAcum < 0:
            col2=rojo
        print("Profit since last order %s %s %% %s  [Acumulated:%s %s %% %s]" % (col,format(PctBenefit,'.4f'),neutro,col2, format(PctBenefitAcum,'.4f'),neutro))

    except:
        print("ERROR: Something failed when tried to get the user ticker/balance")
        if parameters.DEBUG or parameters.DEBUG_BROKER:
            raise
        
def points():
    BenefLastTrade=0.000
    
    if globales.LAST_ORDER_PRICE[globales.NSYMBOL]==0 and globales.TICK==1:
        globales.LAST_ORDER_PRICE[globales.NSYMBOL]=globales.PRICE
        if globales.ASSETS > parameters.MIN_ALLOWED_ASSETS:
            globales.LAST_ORDER_TYPE[globales.NSYMBOL]="buy"
        else:
            globales.LAST_ORDER_TYPE[globales.NSYMBOL]="sell"


    if parameters.DEBUG_ORDERS==True:
        print("%s[START Points() TICK %s | LAST_ORDER_PRICE %s | ASSETS %s | MIN_ALLOWED_ASSETS %s | LAST_ORDER_TYPE %s | BenefLastTrade %s | PRICE %s ] %s" % (purpura, globales.TICK, globales.LAST_ORDER_PRICE[globales.NSYMBOL], globales.ASSETS, parameters.MIN_ALLOWED_ASSETS, globales.LAST_ORDER_TYPE[globales.NSYMBOL], BenefLastTrade, globales.PRICE,neutro))


    LastOrderPrice = float(globales.LAST_ORDER_PRICE[globales.NSYMBOL])
    
    if globales.LAST_ORDER_TYPE[globales.NSYMBOL]=="buy" and LastOrderPrice > 0:
        BenefLastTrade=float(float(globales.PRICE/LastOrderPrice) -1)*100
    if globales.LAST_ORDER_TYPE[globales.NSYMBOL]=="sell" and globales.PRICE > 0:
        BenefLastTrade=float(float(LastOrderPrice/globales.PRICE)-1)*100
        
    if parameters.DEBUG_ORDERS==True:
        print("%s[END Points() TICK %s | LAST_ORDER_PRICE_ %s | ASSETS %s | MIN_ALLOWED_ASSETS %s | LAST_ORDER_TYPE %s | BenefLastTrade %s | PRICE %s ] %s" % (purpura, globales.TICK, globales.LAST_ORDER_PRICE[globales.NSYMBOL], globales.ASSETS, parameters.MIN_ALLOWED_ASSETS, globales.LAST_ORDER_TYPE[globales.NSYMBOL], BenefLastTrade, globales.PRICE,neutro))
    return BenefLastTrade

    
def main_algo():
    try:
        
        if globales.ALGO=="MultiZLDEMA":
            
            z1=common.MuliCR(globales.CK,globales.P1,globales.crtype1)
            z2=common.MuliCR(globales.CK,globales.P2,globales.crtype1)
            z3=common.MuliCR(globales.CK,globales.P3,globales.crtype2)
            z4=common.MuliCR(globales.CK,globales.P4,globales.crtype2)
            vZLD_B =  z1 > z2
            vZLD_S =  z3 < z4
            buy  = common.MUX2(vZLD_B,vZLD_S,globales.sel1)
            sell = common.MUX2(vZLD_B,vZLD_S,globales.sel2)
            globales.MODEL_SIGNAL=0
            if buy :
                globales.MODEL_SIGNAL =  1
                print("%sThe signal is %s (CR1[%s]=%s > CR2[%s]=%s ; CR3[%s]=%s < CR4[%s]=%s ) %s" % (verde,globales.MODEL_SIGNAL,globales.P1,format(z1,'.6f'),globales.P2,format(z2,'.6f'),globales.P3,format(z3,'.6f'),globales.P4,format(z4,'.6f'),neutro))
            if sell :
                globales.MODEL_SIGNAL = -1
                print("%sThe signal is %s (CR1[%s]=%s > CR2[%s]=%s ; CR3[%s]=%s < CR4[%s]=%s ) %s" % (rojo,globales.MODEL_SIGNAL,globales.P1,format(z1,'.6f'),globales.P2,format(z2,'.6f'),globales.P3,format(z3,'.6f'),globales.P4,format(z4,'.6f'),neutro))
            if globales.MODEL_SIGNAL == 0:
                print("The signal is %s (CR1[%s]=%s > CR2[%s]=%s ; CR3[%s]=%s < CR4[%s]=%s)" % (globales.MODEL_SIGNAL,globales.P1,format(z1,'.6f'),globales.P2,format(z2,'.6f'),globales.P3,format(z3,'.6f'),globales.P4,format(z4,'.6f')))
                
                
        if globales.ALGO=="MultiCorrel":
                
    except:
        print("ERROR: Problem during Main Algo execution")
        if parameters.DEBUG or parameters.DEBUG_MAIN_ALGO:
            raise

        
    if globales.MODEL_SIGNAL== 1 and globales.TICK>1: 
        try:
            if parameters.LIMIT_BUY==1:
                limit_buy()
            else:
                market_buy()
        except:
            print("ERROR: There was a problem executing the BUY ORDER")
            if parameters.DEBUG or parameters.DEBUG_ORDERS:
                raise
                
            
        
    if globales.MODEL_SIGNAL==-1 and globales.TICK>1: 
        try:
            if parameters.LIMIT_SELL==1:
                limit_sell()
            else:
                market_sell()
        except:
            print("ERROR: There was a problem executing the SELL ORDER")
            if parameters.DEBUG or parameters.DEBUG_ORDERS:
                raise


            



  


def main_thread():
    
    print(".")
    print(".")
    print(".")
    print(".")
    print(".")
    print(".")
    
    print("%sInitializing main daemon at %s .... %s" % (amarillo,time.strftime("%Y-%m-%d %H:%M:%S"),neutro ) )
    
    # Initializing all counters per asset
    
    for recorrido in SYMBOLS:
        globales.POINTS_EARNED.append(0)
        globales.LAST_ORDER_PRICE.append(0)
        globales.LIMIT_ORDER_SINCE.append(0)
        globales.LIMIT_ORDER_PRICE.append(0)
        globales.LAST_ORDER_TYPE.append("")
        globales.LIMIT_ORDER_CANCELLED.append(0)

    while parameters.RUNNING == True:
        globales.TICK=globales.TICK+1

        print("   ")
        
        print("%s********************************************************************************************************************%s" % (blanco,neutro))
        print("%sT I C K = %s  [Account %s] [%s H] [POLONIEX 5m - %s] DEBUG: %s %s"  % (blanco,globales.TICK,ACCOUNT, format(globales.TICK/12,'.2f'), ACCOUNT,parameters.DEBUG,neutro))
        print("%s********************************************************************************************************************%s" % (blanco,neutro))
        print(SYMBOLS)
            
        print("")
            
            
        sumapoints=0
        for KSYMBOL in SYMBOLS:   
            col=gris
            valor=globales.POINTS_EARNED[SYMBOLS.index(KSYMBOL)]
            if valor>0:
                col=verde
            if valor<0:
                col=rojo
            if parameters.carga_vars(KSYMBOL,'enabled')==1:
                print("Total %s points = %s%s%s" % (KSYMBOL, col,format(valor,'.4f'),neutro))
            sumapoints=sumapoints+globales.POINTS_EARNED[SYMBOLS.index(KSYMBOL)]
        col=gris
        if sumapoints>0:
            col=verde
        if sumapoints<0:
            col=rojo
        
        print("%sTOTAL %% POINTS SUM = %s %s %s %s " % (blanco,neutro,col,format(sumapoints,'.4f'),neutro))
        print("")

        time.sleep(parameters.TIMEOUT)
        
        
        for globales.SYMBOL in SYMBOLS:
            
            globales.NSYMBOL=SYMBOLS.index(globales.SYMBOL) 
            

            importlib.reload(parameters)   
        
            globales.P1=parameters.carga_vars(globales.SYMBOL,'P1')
            globales.P2=parameters.carga_vars(globales.SYMBOL,'P2')
            globales.P3=parameters.carga_vars(globales.SYMBOL,'P3')
            globales.P4=parameters.carga_vars(globales.SYMBOL,'P4')
            globales.sel1=parameters.carga_vars(globales.SYMBOL,'sel1')
            globales.sel2=parameters.carga_vars(globales.SYMBOL,'sel2')
            globales.crtype1=parameters.carga_vars(globales.SYMBOL,'crtype1')
            globales.crtype2=parameters.carga_vars(globales.SYMBOL,'crtype2')
            
            globales.enabled=parameters.carga_vars(globales.SYMBOL,'enabled')
            if parameters.carga_vars(globales.SYMBOL,'algo')==1:
                globales.ALGO="MultiZLDEMA"
            if parameters.carga_vars(globales.SYMBOL,'algo')==2:
                globales.ALGO="MultiCorrel"
            
            
            #globales.NUMVELAS=3*max(globales.P1,max(globales.P2,max(globales.P3,globales.P4))) + 10
            if parameters.DEBUG_MAIN_ALGO == True:
                print("%sThe Number of ticks used for this asset is %s %s" % (amarillo, globales.NUMVELAS,neutro))
                print("")

            if globales.enabled==1:
                print("%sACTUAL MARKET %s_%s [Model:%s] Idx: %s [%s] Tick: %s %s" % (blanco,globales.PAIR_CURR,globales.SYMBOL, globales.ALGO, globales.NSYMBOL,time.strftime("%Y-%m-%d %H:%M"),globales.TICK,neutro) )
                print("--------------------------------------------------------------------------------------------------------------------")
                if parameters.DEBUG_MAIN_ALGO==True:
                    print("%s[%s PARAMETERS] %s %s %s %s %s %s %s %s %s" %(blanco,globales.SYMBOL,globales.P1,globales.P2,globales.P3,globales.P4,globales.sel1,globales.sel2,globales.crtype1,globales.crtype2,neutro))
                
                try:
                    broker_update()
                    main_algo()
                    print(" ")
                except:
                    print("ERROR: There was an unexpected error this tick. Retrying in next tick")
                    if parameters.DEBUG or parameters.DEBUG_BROKER or parameters.DEBUG_MAIN_ALGO or parameters.DEBUG_ORDERS or parameters.DEBUG_UPDATER:
                        raise
                time.sleep(parameters.TIMEOUT)
            else:
                if globales.TICK==1:
                    update_info()
             
        

        print("")
        print("")
        print("%sTick processing ended at %s. Waiting %s Minutes for next tick%s" % (amarillo,time.strftime("%Y-%m-%d %H:%M:%S"),parameters.MINUTE_FREQUENCY,neutro))

        if globales.JUST_STARTED==0:
            globales.JUST_STARTED=1
            
        
        time.sleep(parameters.MINUTE_FREQUENCY*60-time.time()%(parameters.MINUTE_FREQUENCY*60))


        
if __name__ == "__main__":
    main_thread()        