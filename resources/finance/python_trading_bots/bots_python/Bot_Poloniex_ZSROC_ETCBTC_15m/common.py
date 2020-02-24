import math
import numpy as np
import talib

def dx(a,b):
    k=(a-b)/((a+b)/2)
    return k
    
def zs(arr,LRp,FL,STDp):
    valor=(arr[-1]-talib.LINEARREG(arr,LRp)+FL*talib.LINEARREG_SLOPE(arr,LRp))/talib.STDDEV(arr,STDp)
    return valor
        
def zf4(CK,A1,LRp1,FL1,STDp1,B1,LRp2,FL2,STDp2,C1,LRp3,FL3,STDp3,D1,LRp4,FL4,STDp4):
    valor=A1*zs(CK, LRp1, FL1, STDp1)+B1*zs(CK, LRp2, FL2, STDp2)+C1*zs(CK, LRp3, FL3, STDp3) +D1*zs(CK, LRp4, FL4, STDp4)
    return valor

def zscore(arr,p):
    valor=(arr[-1]-talib.LINEARREG(arr,p))/talib.STDDEV(arr,p)
    return valor


def ZSROC(arr,p):
    return zscore(talib.ROC(arr,p),p);

    

def puckII(arr,per, pers,k, th,direc):
    retorno=False
    calc=0.000001
    LR1=talib.LINEARREG(arr,per)
    ST1=talib.STDDEV(arr,pers)                    
    calc=LR1[-1]+ST1[-1] * k
    if direc==0 and calc > th:
        retorno= True
    if direc==1 and calc < th:
        retorno= True
    return retorno

def linregangle(arr,period):
    import numpy as np
    return np.arctan(talib.LINEARREG_SLOPE(arr,period))

def marketfomoing(arr,per1,per2,th):
    LR1=talib.LINEARREG(arr,per1)
    LR2=talib.LINEARREG(arr,per2)
    DXResult=dx(LR1[-1],LR2[-1])
    return DXResult>th

def marketcrashing(arr,per1,per2,th):
    LR1=talib.LINEARREG(arr,per1)
    LR2=talib.LINEARREG(arr,per2)
    DXResult=dx(LR1[-1],LR2[-1])
    return DXResult<th
    
def writetoCSV(symbol,bars): #time, h, c, o, l
    import csv
    import datetime
    f=csv.writer(open("F:/Cripto/Cryptotrader/AMIBROKER/"+symbol+"_1broker.csv","wb+"))
    numbars= len(bars['response'])
    print(numbars)
    # H C O L
    for x in reversed(range(1,numbars+1)):
        f.writerow([datetime.datetime.fromtimestamp(float(bars['response'][-x]['time'])).strftime('%Y-%m-%d %H:%M:%S'),bars['response'][-x]['h'],bars['response'][-x]['c'],bars['response'][-x]['o'],bars['response'][-x]['l']])
        
        
def logbasek(valor,basek):
    return math.log(valor)/math.log(basek)


def nplogbasek(valor,basek):
    return np.log(valor)/np.log(basek)


def SidewaysPuck(arr,p1,p2,th1,th2,lag):
    Ang1=abs(linregangle(arr,p1))
    Ang2=abs(linregangle(arr,p1+p2))
    return (Ang1[-lag]<th1 and Ang2[-lag]<th2)


def SidewaysPuckSTD(arr,a,th,lag):
    Ang=abs(linregangle(arr,a)[-lag])
    return Ang<th
      
    
def CrossLinReg(arr,P1,P2,lag):
    return talib.LINEARREG(arr,P1)[-lag] > talib.LINEARREG(arr,P2)[-lag] and talib.LINEARREG(arr,P1)[-lag-1] < talib.LINEARREG(arr,P2)[-lag-1]
    

def ROC(arr,P1,P2,T1,T2):
    resp = 0
    if talib.ROC(arr,P1)[-1]<T1:
        resp =  1
    if talib.ROC(arr,P2)[-1]>T2:
        resp = -1
    return resp

      

def CR2LinRegSTD(arr,P1,P2,Q1,Q2,lag):
    val=dx(talib.LINEARREG(arr,P1)[-lag],talib.LINEARREG(arr,P2)[-lag])
    
    c1=val>0
    c2=val<0
    c3=CrossLinReg(arr,Q1,Q2,lag)
    c4=CrossLinReg(arr,Q2,Q1,lag)
    
    sig=0
    if c3 or c1:
        sig= 1
    if c4 or c2:
        sig=-1
    return sig

