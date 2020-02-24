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
import sys

from OkcoinSpotAPI import OKCoinSpot
from OkcoinFutureAPI import OKCoinFuture
from random import randint


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
cyan = bcolors.CYAN
neutro=bcolors.ENDC
azulclaro=bcolors.CYAN
warning = bcolors.WARNING

okcoinSpot = OKCoinSpot("www.okcoin.cn",shared.apikey,shared.secretkey)

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
            print(okcoinSpot.trade('btc_cny', 'buy' , shared.price*(1+shared.PriceOverlap) , amount ))
            n=n+1
            print("Waiting %s seconds until next order (TIMEOUT)" %shared.TIMEOUT)
            time.sleep(shared.TIMEOUT)
        else:
            time.sleep(shared.TIMEOUT)
            update_info()
            if shared.curr/shared.price > 0.01:
                print("Iceberg last order. Trying to spend the last %s %s buying %s at price %s" % (shared.curr, shared.PairCurr, shared.curr/shared.price*0.95, shared.price*(1+ 1.5*shared.PriceOverlap)))
                print(okcoinSpot.trade('btc_cny', 'buy' , shared.price*(1+ 1.5*shared.PriceOverlap) , shared.curr/shared.price*0.95 ))
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
            print(okcoinSpot.trade('btc_cny', 'sell' , shared.price*(1-shared.PriceOverlap) , amount ))
            n=n+1
            print("Waiting %s seconds until next order (TIMEOUT)" %shared.TIMEOUT)
            time.sleep(shared.TIMEOUT)
        else:
            update_info()
            if shared.assets>0.01:
                print("Iceberg last order. Trying to sell the last %s %s for %s at price %s" % (shared.assets, shared.PairAsset,shared.price*(1-20*shared.PriceOverlap),shared.price*(1- 1.5 *shared.PriceOverlap) ))
                print(okcoinSpot.trade('btc_cny', 'sell' , shared.price*(1- 1.5 *shared.PriceOverlap)  , shared.assets*0.99 ))
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
            if shared.TICK==1 and JUST_STARTED==0:
                print("CRITICAL: there was a problem getting the ticker or the balance information.")
                print("Please restart and make sure that at least the first tick works properly.")
                shared.running=False
            else:
                print("ERROR: there was a problem getting the ticker or the balance information.")
    JUST_STARTED=1
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

    shared.TICK=shared.TICK+1
    if shared.CheckCode==False:
        print("   ")
        print("********************************************************************************************************************")
        print(" T I C K = %s  [%s D] [BOT: %s] %s" % (shared.TICK, format(shared.TICK/48,'.2f'), shared.BOT_NAME, shared.Cuenta))
        print("********************************************************************************************************************")
    
    
    try:
        update_info()
        
        if shared.CheckCode==False:
            ActualBalanceCNY=shared.curr + shared.assets * shared.price
            StartBalanceCNY=shared.stcurr + shared.stassets * shared.stprice
            ProfitBalanceCNY=(ActualBalanceCNY/StartBalanceCNY-1)*100
            
            ActualBalanceBTC=shared.curr/shared.price+shared.assets
            StartBalanceBTC=shared.stcurr/shared.stprice+shared.stassets
            ProfitBalanceBTC=(ActualBalanceBTC/StartBalanceBTC-1)*100
            
            ProfitBH=(shared.price/shared.stprice-1)*100
            print("Balance now consists in %s CNY and %s BTC" % (format(shared.curr,'.4f'),format(shared.assets,'.4f')))
            col = "neutro"
            if ProfitBalanceCNY > 0:
                col = "verde"
            if ProfitBalanceCNY < 0:
                col = "rojo"
            if ProfitBalanceCNY == 0:
                col = "neutro"
            print("Actual Balance in CNY: %s | Start Belance in CNY: %s | CNY Profit: %s %s %s %%" % (format(ActualBalanceCNY,'.4f'), format(StartBalanceCNY,'.4f') , col, format(ProfitBalanceCNY,'.4f'), neutro ))
            
            col2 = "neutro"
            if ProfitBalanceBTC > 0:
                col2 = "verde"
            if ProfitBalanceBTC < 0:
                col2 = "rojo"
            if ProfitBalanceBTC == 0:
                col2 = "neutro"
            print("Actual Balance in BTC: %s | Start Balance in BTC: %s | BTC Profit: %s %s %s %%" % (format(ActualBalanceBTC,'.4f'),format(StartBalanceBTC,'.4f'), col, format(ProfitBalanceBTC,'.4f') , neutro))
            
            print("Buy & Hold Profit: %s" % (format(ProfitBH,'.4f') ))
            print("Actual BTCCNY value: %s | ck value: %s" % (format(shared.ticker,'.4f'),format(shared.ck[-1],'.4f')))

    except:
        print("ERROR: Something failed when tried to get the user ticker/balance")
        if shared.DEBUG:
            raise
        
    try:
        if shared.CheckCode==False:
            if os.name=='nt':
                f=csv.writer(open("c:/Amibroker/Formulas/CSV_Tickers/stats_ZF4_OK_BTCCNY_15m.csv","a+"),delimiter=';')
                f.writerow([time.strftime("%Y-%m-%d %H:%M") , shared.ticker, shared.net, shared.net/shared.ticker, shared.total])
            else:
                f=csv.writer(open("/home/CSV_Tickers/stats_ZF4_OK_BTCCNY_15m.csv","a+"),delimiter=';')
                f.writerow([time.strftime("%Y-%m-%d %H:%M") , shared.ticker, shared.net, shared.net/shared.ticker, shared.total])
    except:
        print("ERROR: Could not export performance stats to file. Have you got the CSV file opened?")
        if shared.DEBUG:
            raise
        

    shared.vZF4=common.zf4(shared.ck,shared.A1,shared.LRp1,shared.FL1,shared.STDp1,shared.B1,shared.LRp2,shared.FL2,shared.STDp2,shared.C1,shared.LRp3,shared.FL3,shared.STDp3,shared.D1,shared.LRp4,shared.FL4,shared.STDp4)
    print("%svZF4=%s %s" % (amarillo, shared.vZF4, neutro))
    

    
    
def main_algo():
    shared.sig=0
    if shared.ALGO=="ZF4":
        

        
        if shared.vZF4>shared.Th1:
            shared.sig= 1
        if shared.vZF4<shared.Th2:
            shared.sig=-1                
        print("--------------------------------------------------------------------------------------------------------------------")
        print("[ %s - %s ] : LAST SIGNAL = %s [Sell %s < ZF4 = %s  > Buy %s ]" %(shared.BOT_NAME,time.strftime("%Y-%m-%d %H:%M:%S"), shared.sig,shared.Th2 , format(shared.vZF4,'.4f') , shared.Th1))
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
    else:
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
        
        print("ZF4 parameters (A1: %s  ,LRp1: %s , FL1: %s, STDp1: %s | B1: %s  ,LRp2 %s , FL2: %s, STDp2: %s | C1: %s  ,LRp3: %s , FL3: %s, STDp3 %s | D1: %s  ,LRp4: %s , FL4: %s, STDp4: %s )" % (shared.A1,shared.LRp1,shared.FL1,shared.STDp1,shared.B1,shared.LRp2,shared.FL2,shared.STDp2,shared.C1,shared.LRp3,shared.FL3,shared.STDp3,shared.D1,shared.LRp4,shared.FL4,shared.STDp4))                
        num=len(shared.bars)        
        for k in reversed(range(1,shared.NUMVELAS+1)):
            w=common.zf4(shared.ck,shared.A1,shared.LRp1,shared.FL1,shared.STDp1,shared.B1,shared.LRp2,shared.FL2,shared.STDp2,shared.C1,shared.LRp3,shared.FL3,shared.STDp3,shared.D1,shared.LRp4,shared.FL4,shared.STDp4)[-k]
            print("X: %s    |    %s    |    Close:    %s    |    vZF4:    %s   [k: %s|num: %s] " % (num-k,shared.bars['d'][-k], format(shared.bars['c'][-k],'.4f'), w ,k,num)       )

        
if __name__ == "__main__":
    main_thread()        
