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

polo=poloniex.Poloniex('L59Q7PUP-1SN6IGH6-AIK6GUNP-KYDO3AZF','3e921956e80717e12ac5b7f6222f04ff873961760fa73e08cd7fa3b6e57de59005a9e88a4b4a5d106c74f85e2e1f69669f48746b51850c38490cca4665083e0a')




def broker_update():
    for symbol in shared.SYMBOLS:
        try:
            print("------------------------------------------")
            balance=polo.api('returnBalances')
            print("Balance ETH: %s " % balance['ETH'])
            print("Balance BTC: %s " % balance['BTC'])
            print("------------------------------------------")
        except:
            print("ERROR: There was an unexpected problem when getting the balances data from the exchange")
    
        try:
            bars=polo.directpublic('https://poloniex.com/public?command=returnChartData&currencyPair=BTC_ETH&start=1405699200&end=9999999999&period=900')
        except:
            print("ERROR: There was an unexpected problem when downloading the historical bars from the exchange")
    
        def calculate_close(period):
            valor=[]
            for x in reversed(range(1,period+1)):
                valor.append(bars[-x]['close'])
            valor2=np.array(valor,dtype='float')
            
            return valor2
        
        
        
        try:
            ticker=polo.api('returnTicker')
            shared.price=float(ticker[shared.PAIR]['last'])
            print("Actual ETHBTC Value: %s - %s" % (time.strftime("%Y-%m-%d %H:%M:%S") , shared.price))
        except:
            print("ERROR: There was an unexpected problem when downloading the ticker data from the exchange")
        
        shared.ck=calculate_close(shared.NUMVELAS)
    
        shared.vSidewaysPuck=common.SidewaysPuck(shared.ck,shared.P1,shared.P2,shared.Th1, shared.Th2, 2)
    
    
    

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
        
        
       
        OpenOrders=polo.api('returnOpenOrders',{'currencyPair':'BTC_ETH'})
        print("Displaying list of opened orders at this moment")
        print(OpenOrders)
        numOrders= len(OpenOrders)        
        print("There are %s opened orders" % (numOrders))
        
        if numOrders>0 and shared.TICK==1:  # HERE WE CLOSE ALL ORDERS FROM PREVIOUS EXECUTIONS OF THE BOT
            print("We have some orders BUT Algorithm Just started. Closing all open orders from previous sessions")
            try:
                for x in reversed(range(1,numOrders+1)):
                    actual=str(OpenOrders[-x]['orderNumber'])
                    print("We select an open order: %s" % (actual))
                    print("Closing order %s" % (actual))
                    print(polo.api('cancelOrder',{'currencyPair':shared.PAIR,'orderNumber':actual}))
                print("Ended closing orders")
            except:
                print("ERROR: At bot start, when cancelling orders from other sessions something failed")
            


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
                        print(polo.api('cancelOrder',{'currencyPair':shared.PAIR,'orderNumber':shared.TimeoutList1[-x]}))
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
                        print(polo.api('cancelOrder',{'currencyPair':shared.PAIR,'orderNumber':shared.TimeoutList1[-x]}))
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
                    balance=polo.api('returnBalances')
                    assets=float(balance[shared.PairAsset])
                    curr=float(balance[shared.PairCurr])    
                except:
                    print("ERROR: Tried to get the balance from the exchange but something failed")
                
                try:
                    ticker=polo.api('returnTicker')
                    shared.price=float(ticker[shared.PAIR]['last'])            
                    maxassets=float(curr/shared.price+assets)
                    orderSize=float(maxassets/shared.SPLIT)
                except:
                    print("ERROR: Tried to get the ticker data from the exchange but something failed")
                
                if (curr/(shared.price*shared.KL)) > 1:
                    print("There is enough money to buy. Placing an order")
                    try:
                        neworder=polo.api('buy', {'currencyPair': shared.PAIR, 'rate': shared.price * shared.KL , 'amount': 1 })
                        print("Adding the order to the timeout list")
                        actual=neworder['orderNumber']
                        shared.TimeoutList1.append(actual)
                        shared.TimeoutList2.append(shared.TICK)
                        shared.TimeoutList3.append('buy')
                        print(shared.TimeoutList1)
                        print(shared.TimeoutList2)
                        print(shared.TimeoutList3)
                    except:
                        print("ERROR: Tried to place a buy order but something failed")
                else:
                    print("Not enough money to buy")
                
                if assets > 1:
                    print("There are enough assets to sell. Placing an order")
                    try:
                        neworder=(polo.api('sell', {'currencyPair': shared.PAIR, 'rate': shared.price * shared.KH , 'amount': 1 }))
                        print("Adding the order to the timeout list")
                        actual=neworder['orderNumber']
                        shared.TimeoutList1.append(actual)
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
        




        try:
            balance=polo.api('returnBalances')
            ticker=polo.api('returnTicker')
            assets1=float(balance[shared.PairAsset])                    
            curr1=float(balance[shared.PairCurr])    
            price1=float(ticker[shared.PAIR]['last'])        
        except:
            print("ERROR: There was a problem when retrieving the balance/ticker data from the exchange")
        

    
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
    if initialcurr==0:
        initialcurr=initialcurr + 0.0000001
        
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
    print("Initializing main daemon.")
    balance=polo.api('returnBalances')
    ticker=polo.api('returnTicker')
    starting_time=time.strftime("%Y-%m-%d %H:%M:%S") 
    starting_assets=float(balance[shared.PairAsset])                    
    starting_curr=float(balance[shared.PairCurr])      
    starting_price=float(ticker[shared.PAIR]['last'])         
    while running == True:
        broker_update()
        main_algo()
        #try:
        #    SessionReport(starting_time,starting_assets,starting_curr,starting_price)
        #except:
        #    print("ERROR: There was a problem when displaying the report")
        print("Tick processing ended. Waiting for next tick. Waiting %s Seconds" % (shared.MAIN_SLEEP_TIME))
        time.sleep(shared.MAIN_SLEEP_TIME)
        

    


    


if __name__ == "__main__":
    main_thread()