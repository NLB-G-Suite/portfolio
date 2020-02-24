#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
import poloniex
import json
import csv
import datetime
import time
import os
import shared


from collections import deque


def get_last_row(csv_filename):
    with open(csv_filename, 'r') as f:
        try:
            lastrow = deque(csv.reader(f), 1)[0]
        except IndexError:  # empty file
            lastrow = None
        return lastrow
    
def write_line_to_csv(csv_filename,row):
    f=csv.writer(open(csv_filename,'a+',newline=''),delimiter=';')
    f.writerow(row)
    return 1

polo=poloniex.Poloniex(shared.API_Key,shared.API_SECRET)



TimePeriodInSeconds=300
running=True


for symbol in shared.SYMBOLS:    

    start=int(time.time()-TimePeriodInSeconds*2) 
    ChartData=polo.api('returnChartData',{'currencyPair':str(symbol),'period':str(TimePeriodInSeconds), 'start': str(start), 'end':'9999999999'})[-1]
    print("%s -> %s" % (symbol,ChartData) )
    str1=str(datetime.datetime.fromtimestamp(float(ChartData['date'])).strftime('%d/%m/%Y %H:%M'))
    str2=(ChartData['open'])
    str3=(ChartData['close'])
    str4=(ChartData['high'])
    str5=(ChartData['low'])
    str6=(ChartData['quoteVolume'])
    k=[str1,str2,str3,str4,str5,str6]

    # D OCHLV 
    if (str2 >0 and str3 >0 and str4>0 and str5>0):
        if os.name=='nt':
            write_line_to_csv("C:/AmiBroker/Formulas/CSV_Tickers/PO-"+symbol+"-5m.csv", k)
        else:
            write_line_to_csv("/home/CSV_Tickers/PO-"+symbol+"-5m.csv",k)
    #else:
        #print("No Data. Copying last line")
        #if os.name=='nt':
            #h=get_last_row("C:/AmiBroker/Formulas/CSV_Tickers/PO-"+symbol+"-5m.csv")
        #else:
            #h=get_last_row("/home/CSV_Tickers/PO-"+symbol+"-5m.csv")
        #print("Last Line was:")
        #print(h)
        #print("Saving last line as actual")
        #if os.name=='nt':
            #write_line_to_csv("C:/AmiBroker/Formulas/CSV_Tickers/PO-"+symbol+"-5m.csv", h)
        #else:
            #write_line_to_csv("/home/CSV_Tickers/PO-"+symbol+"-5m.csv",h)
        #print("%s -> %s" % (symbol,h) )


        
