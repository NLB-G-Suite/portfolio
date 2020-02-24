
FRECUENCIA_MINUTOS=15
MAIN_SLEEP_TIME= 60 * FRECUENCIA_MINUTOS

SPLIT=10
TIMEOUT=10
PriceOverlap=0.0015

JUST_STARTED=1

MinOrderAsset=0.1
MinOrderCurr=0.0001


apikey='011eaa4f-4a14-4ba3-93df-36f86e3e7ee9'
secretkey='725F9EDBCE71326C3A230732F0C24C95'

# ////////////////////////////////////
# CONSTANTES SIDEWAYS PUCK
# ////////////////////////////////////

MAX_OPEN_POSITITIONS=SPLIT

ALGO="SIDEWAYS PUCK"

PAIR='BTC_ETH'
PairAsset='ETH'
PairCurr='BTC'

P1 = 505
P2 = 981
Th1 = 1.2777
Th2 = 50
KH = 1.00164
KL = 0.997758
hb = 1
hs = 3



#VELAS

NUMVELAS=2000
DELAY=0

HISTVELAS=8760

TICK=0


OrderList=[]
TimeoutList1=[]
TimeoutList2=[]
TimeoutList3=[]

# start gui
gui = False

# candles chart time
BARS_TIME = "60"

# broker data refresh thread sleep time 
BROKER_SLEEP_TIME =9 


# assets on which this script trades
SYMBOLS = ["EURUSD"]
# all symbols:
#BTCUSD, EURCHF, USDCAD, GBPUSD, EURGBP, EURJPY, EURNOK, EURSEK, EURUSD, NZDUSD, USDCNH, AUDNZD, AUDUSD, USDRUB, USDJPY, USDCHF, SILVER, GOLD, OILWTI, NFLX, MSFT, PEP, WU, TSLA, TWTR, BAC, V, VOW, KO, AAPL, BMW, BABA, F, FB, GOOG, GPRO, AMZN, INTC, CSCO, AU200, CH30, DAX, UK100, DOW, EU50, SP500, HK50, JP225

# margin used for single position, and leverage
MARGIN = "0.20"
LEVERAGE = "10"

# stop loss&take profit; in market change, multiply by leverage to get profit or loss %
# divided by leverage to get pure %
STOP_LOSS_PERCENT = 0
# round(0.75/float(LEVERAGE), 2)
TAKE_PROFIT_PERCENT = 0 
#round(1.5/float(LEVERAGE), 2)

# your 1broker API token
#API_KEY = "8f42c96ed285f57fb608a4885c17ef05"

# old, trailing stop setting
FOLLOWING_STOP_MARGIN = 2000

running = True

STARTING_HIGHEST_PL = -FOLLOWING_STOP_MARGIN
current_position_highest_profitloss = STARTING_HIGHEST_PL


vZF4=0
TrendingUp=False
TrendingDn=False
sig=0
ticker=0
price=0




# some stats
broker_fetch_count = 0
startup_balance = 0

# init
#for symbol in SYMBOLS:
#	sma5[symbol] = 0
#	sma20[symbol] = 0
#	prev_sma5[symbol] = 0
#	prev_sma20[symbol] = 0
#	position[symbol] = (False, False)

# logging
import logging
import logging.config
log_level = "DEBUG"
logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': log_level,
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'level': "DEBUG",
            'filename': 'debug.log',
            'maxBytes': 2097152, # 2 MiB
            'backupCount': 10,
        },
        'file_info': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'default',
            'level': "INFO",
            'filename': 'info.log',
            'maxBytes': 2097152, # 2 MiB
            'backupCount': 10,
        }
    },
    'loggers': {
        'console_only': {
            'handlers': ['console'],
            'propagate' : 0
        },
        'file_only': {
            'handlers': ['file'],
            'propagate' : 0
        },
        'both': {
            'handlers': ['console', 'file'],
            'propagate' : 0
        },
    },
    'root': {
        'level': log_level,
        'handlers': ['console', 'file', 'file_info'],
    },
})
