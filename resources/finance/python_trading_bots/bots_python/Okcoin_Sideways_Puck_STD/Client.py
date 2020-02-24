#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8

import websocket

from OkcoinSpotAPI import OKCoinSpot
from OkcoinFutureAPI import OKCoinFuture

apikey='011eaa4f-4a14-4ba3-93df-36f86e3e7ee9'
secretkey='725F9EDBCE71326C3A230732F0C24C95'

okcoinRESTURL = 'www.okcoin.cn'   #请求注意：国内账号需要 修改为 www.okcoin.cn  

okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)

okcoinFuture = OKCoinFuture(okcoinRESTURL,apikey,secretkey)


print (okcoinSpot.ticker('btc_cny'))


#print (okcoinSpot.depth('btc_usd')) 


#j=websocket.create_connection(url, timeout=None, class_=WebSocket)
#k=websocket.send("{'event':'addChannel','channel':'ok_sub_spotcny_btc_kline_15min'}")

#K=okcoinSpot.trades()
#print(K)


#print (okcoinSpot.userinfo())
#balance=okcoinSpot.userinfo()
#print(balance['info']['funds']['free']['btc'])
#print(balance['info']['funds']['free']['btc'][-1])

#print (okcoinSpot.trade('ltc_usd','buy','0.1','0.2'))


#print (okcoinSpot.batchTrade('ltc_usd','buy','[{price:0.1,amount:0.2},{price:0.1,amount:0.2}]'))


#print (okcoinSpot.cancelOrder('ltc_usd','18243073'))


#print (okcoinSpot.orderinfo('ltc_usd','18243644'))


#print (okcoinSpot.ordersinfo('ltc_usd','18243800,18243801,18243644','0'))


print (okcoinSpot.orderHistory('btc_cny','0','1','2'))
























#print (okcoinFuture.future_ticker('ltc_usd','this_week'))


#print (okcoinFuture.future_depth('btc_usd','this_week','6'))


#print (okcoinFuture.future_trades('ltc_usd','this_week'))


#print (okcoinFuture.future_index('ltc_usd'))


#print (okcoinFuture.exchange_rate())


#print (okcoinFuture.future_estimated_price('ltc_usd'))


#print (okcoinFuture.future_userinfo())


#print (okcoinFuture.future_position('ltc_usd','this_week'))


#print (okcoinFuture.future_trade('ltc_usd','this_week','0.1','1','1','0','20'))


#print (okcoinFuture.future_batchTrade('ltc_usd','this_week','[{price:0.1,amount:1,type:1,match_price:0},{price:0.1,amount:3,type:1,match_price:0}]','20'))


#print (okcoinFuture.future_cancel('ltc_usd','this_week','47231499'))


#print (okcoinFuture.future_orderinfo('ltc_usd','this_week','47231812','0','1','2'))


#print (okcoinFuture.future_userinfo_4fix())


#print (okcoinFuture.future_position_4fix('ltc_usd','this_week',1))



   
