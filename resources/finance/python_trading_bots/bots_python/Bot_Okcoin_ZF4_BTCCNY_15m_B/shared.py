
FRECUENCIA_MINUTOS=15
MAIN_SLEEP_TIME= 60 * FRECUENCIA_MINUTOS

SPLIT=10
TIMEOUT= (FRECUENCIA_MINUTOS - 2) * 60 / SPLIT
PriceOverlap=0.0015

JUST_STARTED=0

MinOrderAsset=0.1
MinOrderCurr=0.0001

TICK=0

#Guayaba
apikey= '627eb3e8-0237-4bae-8394-56cfa19256c2'
secretkey= 'E5ED9F5C22E7A2EC0537AD4610B42224'


# ////////////////////////////////////
# CONSTANTES ZF4 ANG
# ////////////////////////////////////

BOT_NAME="OKCOIN ZF4 BTCCNY 15M B"
ALGO="ZF4"

PAIR='btc_cny'
PairAsset='BTC'
PairCurr='CNY'

Cuenta = "badolato"

A1	=  10.27
B1	= -15.05
C1	=  45.15
D1	= -69.4

LRp1	=  380
LRp2	=  433
LRp3	=  131
LRp4	=   98

STDp1	=  402
STDp2	=  476
STDp3	=  104
STDp4	=  383

FL1	=  -9.63
FL2	=  -14
FL3	=  -5.43
FL4	=  -27.54

Th1     =  44.386
Th2     = -32.465


FEEPCT = 0.016

# ###############################

NUMVELAS=5000


running = True

CheckCode=False
DEBUG=False
SHOWTABLE=False


vZF4=[]
TrendingUp=False
TrendingDn=False
sig=0
ticker=0
price=0


balance=0
assets=0
curr=0
net=0
price=0
total=0

stbalance=0
stassets=0
stcurr=0
stnet=0
stprice=0
stotal=0

FirstTickError=0


