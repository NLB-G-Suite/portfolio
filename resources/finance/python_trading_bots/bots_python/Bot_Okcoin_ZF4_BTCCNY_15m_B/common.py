import math
import numpy as np
import talib

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


def dx(a,b):
    k=(a-b)/((a+b)/2)
    return k





def st(arr,period):
    sum1=0
    sum2=0
    for i in range(1,period):
        select=len(arr)-1-period+i
        sum1=sum1

    
def zs(arr,LRp,FL,STDp):
    valor=(arr[-1]-talib.LINEARREG(arr,LRp)[-1]+FL*talib.LINEARREG_SLOPE(arr,LRp)[-1])/talib.STDDEV(arr,STDp)[-1]
    return valor
        
def zf4(CK,A1,LRp1,FL1,STDp1,B1,LRp2,FL2,STDp2,C1,LRp3,FL3,STDp3,D1,LRp4,FL4,STDp4):
    valor=A1*zs(CK, LRp1, FL1, STDp1)+B1*zs(CK, LRp2, FL2, STDp2)+C1*zs(CK, LRp3, FL3, STDp3) +D1*zs(CK, LRp4, FL4, STDp4)
    return valor

def zf3(CK,A1,LRp1,FL1,STDp1,B1,LRp2,FL2,STDp2,C1,LRp3,FL3,STDp3):
    valor= A1*zs(CK, LRp1, FL1, STDp1) + B1 * zs(CK, LRp2, FL2, STDp2) + C1*zs(CK, LRp3, FL3, STDp3)
    return valor


def zscore(arr,p):
    valor=(arr[-1]-talib.LINEARREG(arr,p))/talib.STDDEV(arr,p)
    return valor


def ZSROC(arr,p):
    return zscore(talib.ROC(arr,p),p)

def MUX2(a,b,sel):
    res=False
    if sel==1:
        res=a and b
    if sel==2:
        res=a and not b
    if sel==3:
        res=not a and b
    if sel==4:
        res=a or b
    if sel==5:
        res=a or not b
    if sel==6:
        res=not a or b
    if sel==7:
        res=not a and not b
    if sel==8:
        res=not a or not b
    return res    

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

def ZLDEMA(arr,p):
    zld=2*talib.DEMA(arr,p)[-1]-talib.DEMA(arr,(2*p)-1)[-1]
    return zld

def ZLEMA(arr,p):
    zle=2*talib.EMA(arr,p)[-1]-talib.EMA(arr,(2*p)-1)[-1]
    return zle


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


def MuliCR(arr,period,crtype):
    valor=0
    if crtype==1:
        valor=ZLDEMA(arr,period)
    if crtype==2:
        valor=ZLEMA(arr,period)
    if crtype==3:
        valor=talib.LINEARREG(arr,period)[-1]
    return valor

def MultiCorrel(arr,x1,x2,x3,x4,tb,ts):
    sig=0
    ratio=talib.LINEARREG(arr,x1)/talib.LINEARREG(arr,x2)
    print("====================")
    aa=talib.LINEARREG_INTERCEPT(ratio,x4)
    bb=talib.LINEARREG_SLOPE(ratio,x4)
    res=ratio-(aa+bb*ratio)
    corx=talib.CORREL(ratio,ratio-res,x3)
    std=talib.STDDEV(corx,x4)
    Z=(corx-talib.LINEARREG(corx,x4))/talib.STDDEV(corx,x4)
    CI=Z*10
    if CI[-1] < tb:
        sig=1
    if CI[-1] > ts:    
        sig=-1
#    if parameters.DEBUG_MAIN_ALGO==True:
    period=len(arr)
    for x in reversed(range(1,period+1)):
        print("%s[%s] arr: %s | ratio: %s | aa: %s | bb: %s | res: %s | corx: %s | std: %s | Z: %s | CI: %s" %(bcolors.WARNING, globales.SYMBOL, format(arr[-x],'.8f'),format(ratio[-x],'.8f'),format(aa[-x],'.8f'),format(bb[-x],'.8f'),format(res[-x],'.8f'),format(corx[-x],'.8f'),format(std[-x],'.8f'),format(Z[-x],'.8f'),format(CI[-x],'.8f'), neutro))
    return sig
