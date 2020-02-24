import poloniex
import json
import time
import time

import shared
import common
import talib
import math
import random

import numpy as np




running=True

polo=poloniex.Poloniex('BQDLO5T5-3LRJEACQ-E6NF99LR-V4WZXDTY','392d25a3059ecfe0fded3c11e8b92c0eafafc512d241000a960ea96545e7bb55c5cf6d65afafcf0fe7a9c2b9dbb175dad1956029a8b798c6564195d20cdc5008')




def broker_update():
    print("------------------------------------------")
    balance=polo.api('returnBalances')
    print("Balance ETH: %s " % balance['ETH'])
    print("Balance BTC: %s " % balance['BTC'])
    

    bars=polo.directpublic('https://poloniex.com/public?command=returnChartData&currencyPair=BTC_ETH&start=1405699200&end=9999999999&period=900')

    def calculate_close(period):
        valor=[]
        for x in reversed(range(1,period+1)):
            valor.append(bars[-x]['close'])
        valor2=np.array(valor,dtype='float')
        
        return valor2
    
    
    
    
    ticker=polo.api('returnTicker')
    shared.price=float(ticker[shared.PAIR]['last'])
    print("%s - %s" % (time.strftime("%Y-%m-%d %H:%M:%S") , shared.price))
    
    shared.ck=calculate_close(shared.NUMVELAS)

    shared.vZF4=common.zf4(shared.ck,shared.A1,shared.LRp1,shared.FL1,shared.STDp1,shared.B1,shared.LRp2,shared.FL2,shared.STDp2,shared.C1,shared.LRp3,shared.FL3,shared.STDp3,shared.D1,shared.LRp4,shared.FL4,shared.STDp4)
    TrendingUp=common.linregangle(shared.ck,shared.ap)>shared.au
    TrendingDn=common.linregangle(shared.ck,shared.ap)<shared.ad
    print ("ZF4 = %s | TrendingUp = %s | TrendingDn = %s " % (shared.vZF4[-1],shared.TrendingUp,shared.TrendingDn))
    

def main_algo():
    # for all pairs
    for symbol in shared.SYMBOLS:
        print("Main algorithm started for %s " % shared.PAIR)
        print("Actual Model => %s " % shared.ALGO)
        shared.sig=0
        
        if shared.ALGO=="ZF4":
            if shared.vZF4[-1]>shared.Th1:
                print("BUY SIGNAL")
                shared.sig= 1
            if shared.vZF4[-1]<shared.Th2:
                print("SELL SIGNAL")
                shared.sig=-1
                
        if shared.ALGO=="ZF4 ANG":
            if ((shared.vZF4[-1]>shared.Th1) and not shared.TrendingDn) or shared.TrendingUp :
                print("BUY SIGNAL")
                shared.sig= 1
            if ((shared.vZF4[-1]<shared.Th2) and not shared.TrendingUp) or shared.TrendingDn :
                print("SELL SIGNAL")
                shared.sig=-1
                
        
        if shared.ALGO=="P3F2":
            c1=common.puckII(shared.ck,shared.P1,shared.S1,shared.K1,shared.ThL,1)
            c2=common.marketfomoing(shared.ck,shared.Fo1,shared.Fo2,shared.FT)
            c3=common.puckII(shared.ck,shared.P2,shared.S2,shared.K2,shared.ThS,0)
            c4=common.marketcrashing(shared.ck,shared.Cr1,shared.Cr2,shared.CT)                 
            shared.sig= 0
            if (c1 and not c4) or c2:
                print("BUY SIGNAL")
                shared.sig= 1
            else:
                if (c3 and not c2) or c4:
                    print("SELL SIGNAL")
                    shared.sig=-1
                else:
                    print("NULL SIGNAL")
                    shared.sig= 0


        def ice_buy():
            n = 1
            buying=True
            balance=polo.api('returnBalances')
            assets=float(balance[shared.PairAsset])
            curr=float(balance[shared.PairCurr])    
            ticker=polo.api('returnTicker')
            shared.price=float(ticker[shared.PAIR]['last'])            
            maxassets=float(curr/shared.price+assets)
            orderSize=float(maxassets/shared.SPLIT)
            if curr>shared.MinOrderCurr:
                print("There is enough Curr to buy")
                buying=True
                selling=False
            else:
                buying=False 
                selling=False

            print("MaxAssets = %s | OrderSize = %s | LastPrice = %s" % (maxassets,orderSize,shared.price))
            while buying:
                amount=max(1,(0.8+0.4*random.random())*orderSize)                
                if shared.SPLIT>1 and float(curr/shared.price) > max(1,float(orderSize*1.2)) and curr>shared.MinOrderCurr:
                    print("Iceberg Order ##%s" % n)
                    print(polo.api('buy', {'currencyPair': shared.PAIR, 'rate': shared.price*(1+shared.PriceOverlap) , 'amount': amount, 'immediateOrCancel': 1 }))
                    n=n+1
                    print("Waiting %s seconds until next order (TIMEOUT)" %shared.TIMEOUT)
                    time.sleep(shared.TIMEOUT)
                    ticker=polo.api('returnTicker')
                    shared.price=float(ticker[shared.PAIR]['last'])                        
                    balance=polo.api('returnBalances')
                    curr=float(balance[shared.PairCurr])
                else:
                    balance=polo.api('returnBalances')
                    curr=float(balance[shared.PairCurr])    
                    ticker=polo.api('returnTicker')
                    shared.price=float(ticker[shared.PAIR]['lowestAsk'])                        
                    print("Iceberg last order. Trying to spend the last %s %s" % (curr, shared.PairCurr))
                    print(polo.api('buy', {'currencyPair': shared.PAIR, 'rate': shared.price*(1+20*shared.PriceOverlap) , 'amount': curr*0.997, 'immediateOrCancel': 1  }))
                    buying=False
                    print("Finished buying")
                    OrderReport(assets,curr,shared.price)
            
        def ice_sell():
            n = 1
            
            balance=polo.api('returnBalances')
            assets=float(balance[shared.PairAsset])                    
            curr=float(balance[shared.PairCurr])    
            ticker=polo.api('returnTicker')
            shared.price=float(ticker[shared.PAIR]['last'])
            maxassets=float(curr/shared.price+assets)
            orderSize=float(maxassets/shared.SPLIT)
            if assets>shared.MinOrderAsset:
                print("There are enough assets to sell")
                selling=True
                buying=False
            else:
                selling=False
                buying=False
            
            while selling:
                amount=max(1,(0.8+0.4*random.random())*orderSize)
                if shared.SPLIT>1 and assets > max(1,orderSize*1.2):
                    print("Iceberg Order ##%s" % n)
                    print(polo.api('sell', {'currencyPair': shared.PAIR, 'rate': shared.price*(1-shared.PriceOverlap) , 'amount': amount, 'immediateOrCancel': 1 }))
                    n=n+1
                    print("Waiting %s seconds until next order (TIMEOUT)" %shared.TIMEOUT)
                    time.sleep(shared.TIMEOUT)
                    ticker=polo.api('returnTicker')
                    shared.price=float(ticker[shared.PAIR]['last'])                        
                    balance=polo.api('returnBalances')
                    assets=float(balance[shared.PairAsset])
                else:
                    balance=polo.api('returnBalances')   
                    assets=float(balance[shared.PairAsset])                    
                    ticker=polo.api('returnTicker')
                    shared.price=float(ticker[shared.PAIR]['highestBid'])                             
                    print("Iceberg last order. Trying to sell the last %s %s" % (assets, shared.PairAsset))
                    print(polo.api('sell', {'currencyPair': shared.PAIR, 'rate': shared.price*(1-20*shared.PriceOverlap) , 'amount': assets*0.997, 'immediateOrCancel': 1 }))
                    selling=False
                    print("Finished selling")
                    OrderReport(assets,curr,shared.price)



        def OrderReport(assets1,curr1,price1):
            time.sleep(5)
            print("Final Order Report")
            print("======================")
            balance=polo.api('returnBalances')   
            ticker=polo.api('returnTicker')      
            assets2=float(balance[shared.PairAsset])                    
            curr2=float(balance[shared.PairCurr])    
            price2=float(ticker[shared.PAIR]['last'])                    
            
            initialcurr=float(curr1+assets1*price1)
            finalcurr=float(curr2+assets2*price2)
            print("Start: %s %s and %s %s and the price was %s = %s"% (assets1, shared.PairAsset, curr1, shared.PairCurr, price1, initialcurr ))
            print("End  : %s %s and %s %s and the price was %s = %s"% (assets2, shared.PairAsset, curr2, shared.PairCurr, price2, finalcurr ))
            slippage=float((finalcurr/initialcurr-1)*100)
            print("Percent Lost on Slippage & Expenses : %s " % slippage)            
            return 1
        





        balance=polo.api('returnBalances')
        ticker=polo.api('returnTicker')
        assets1=float(balance[shared.PairAsset])                    
        curr1=float(balance[shared.PairCurr])    
        price1=float(ticker[shared.PAIR]['last'])        
        
        if shared.sig== 1:
            ice_buy()
            
        if shared.sig==-1:
            ice_sell()
            
        #if shared.sig==1 or shared.sig==-1:

        
            
        if shared.sig== 0:
            print("No clear signal - doing nothing.")
    
def SessionReport(starting_time,assets1,curr1,price1):
    print(" ")
    print("==================")
    print("Session Statistics")
    print("==================")
    balance=polo.api('returnBalances')   
    ticker=polo.api('returnTicker')      
    assets2=float(balance[shared.PairAsset])                    
    curr2=float(balance[shared.PairCurr])    
    price2=float(ticker[shared.PAIR]['last'])                    
    
    initialcurr=float(curr1+assets1*price1)
    finalcurr=float(curr2+assets2*price2)
    print("Start: %s | Now: %s" %(starting_time,time.strftime("%Y-%m-%d %H:%M:%S")))
    print("--------------------------------------------------------------")
    print("Start: %s %s and %s %s and the price was %s "% (round(assets1,4), shared.PairAsset, round(curr1,4), shared.PairCurr, price1))
    print("End  : %s %s and %s %s and the price was %s "% (round(assets2,4), shared.PairAsset, round(curr2,4), shared.PairCurr, price2))
    print("--------------------------------------------------------------")
    Benefit_Curr=float((finalcurr/initialcurr-1)*100)
    Benefit_BH=float((price2/price1-1)*100)
    Benefit_Assets=float(((finalcurr/price2)/(initialcurr/price1)-1)*100)
    print("Benefit %s: %s %% [%s]" % (shared.PairCurr,round(Benefit_Curr,4),round(finalcurr-initialcurr,4)))            
    print("Benefit %s: %s %% [%s]" % (shared.PairAsset,round(Benefit_Assets,4),round(finalcurr/price2-initialcurr/price1,4)))            
    print("Benefit B&H: %s %%" % (round(Benefit_BH,4)))
    print("--------------------------------------------------------------")
    print("Total in %s would be %s" % (shared.PairCurr,round(finalcurr,4)))
    print("Total in %s would be %s" % (shared.PairAsset,round(finalcurr/price2,4)))
    print("--------------------------------------------------------------")
    return 1          


def main_thread():
    print"Initializing main daemon."
    balance=polo.api('returnBalances')
    ticker=polo.api('returnTicker')
    starting_time=time.strftime("%Y-%m-%d %H:%M:%S") 
    starting_assets=float(balance[shared.PairAsset])                    
    starting_curr=float(balance[shared.PairCurr])      
    starting_price=float(ticker[shared.PAIR]['last'])         
    while running == True:
        broker_update()
        main_algo()
        SessionReport(starting_time,starting_assets,starting_curr,starting_price)
        print("Tick processing ended. Waiting for next tick")
        time.sleep(900)

    


    


if __name__ == "__main__":
    main_thread()