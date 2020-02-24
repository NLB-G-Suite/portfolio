



    

def main_algo():

    
    
   
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
        #print("This is the list of buy orders to check:")
        numTimeouts=len(shared.TimeoutList1)
        for x in reversed(range(1,numTimeouts+1)):
            #print(shared.TimeoutList1[-x])
            if (shared.TimeoutList3[-x]=='buy' and ( shared.TICK - shared.TimeoutList2[-x] > shared.hb)):
                try:
                    print(polo.api('cancelOrder',{'currencyPair':shared.PAIR,'orderNumber':shared.TimeoutList1[-x]}))
                    #print("AFTER DEL (Buy) NumTimeoutList1=%s | NumTimeoutList2=%s | NumTimeoutList3=%s" % (len(shared.TimeoutList1),len(shared.TimeoutList2),len(shared.TimeoutList3)))
                    del shared.TimeoutList1[-x]
                    del shared.TimeoutList2[-x]
                    del shared.TimeoutList3[-x]
                    #print("AFTER DEL (Buy) NumTimeoutList1=%s | NumTimeoutList2=%s | NumTimeoutList3=%s" % (len(shared.TimeoutList1),len(shared.TimeoutList2),len(shared.TimeoutList3)))
                except:
                    print("ERROR: Tried to cancel a buy order that reached the timeout but something failed")
        #print("This is the list of sell orders to check:")
        numTimeouts=len(shared.TimeoutList1)
        for x in reversed(range(1,numTimeouts+1)):
            #print(shared.TimeoutList1[-x])
            if (shared.TimeoutList3[-x]=='sell' and ( shared.TICK - shared.TimeoutList2[-x] > shared.hs)):
                try:
                    print(polo.api('cancelOrder',{'currencyPair':shared.PAIR,'orderNumber':shared.TimeoutList1[-x]}))
                    #print("BEFORE DEL (Sell) NumTimeoutList1=%s | NumTimeoutList2=%s | NumTimeoutList3=%s" % (len(shared.TimeoutList1),len(shared.TimeoutList2),len(shared.TimeoutList3)))
                    del shared.TimeoutList1[-x]
                    del shared.TimeoutList2[-x]
                    del shared.TimeoutList3[-x]
                    #print("AFTER DEL (Sell) NumTimeoutList1=%s | NumTimeoutList2=%s | NumTimeoutList3=%s" % (len(shared.TimeoutList1),len(shared.TimeoutList2),len(shared.TimeoutList3)))
                except:
                    print("ERROR: Tried to cancel a sell order that reached the timeout but something failed")
                
        

    print("=================== ALGO: MAIN LOGIC ===================")
    print("Checking buy/sell algorithm to see if we can create new orders")
    print("Model vSidewaysPuckSTD wants to operate now? %s [Why? Ang=%s < Th=%s ]" % (shared.vSidewaysPuckSTD, abs(common.linregangle(shared.ck,shared.A)[-1]), shared.Th))
    if shared.ALGO=="SIDEWAYS PUCK STD":
        if shared.vSidewaysPuckSTD:
            
            
            print("----------------------------------------------------------------------------")
            


            if float(shared.amountpct)*float(curr)/float(buyprice) > shared.amountmin:
                print("There is enough money to buy. Placing an order")
                try:

                    neworder=polo.api('buy', {'currencyPair': shared.PAIR, 'rate': buyprice , 'amount': buyamount })
                    #print("Adding the order to the timeout list")
                    actual=neworder['orderNumber']
                    shared.TimeoutList1.append(actual)
                    shared.TimeoutList2.append(shared.TICK)
                    shared.TimeoutList3.append('buy')
                    #print(shared.TimeoutList1)
                    #print(shared.TimeoutList2)
                    #print(shared.TimeoutList3)
                except:
                    print("ERROR: Tried to place a buy order but something failed")
            else:
                print("Not enough money to buy")
            
            sellamount = shared.amountpct * assets
            if float(shared.amountpct)*assets > shared.amountmin:
                print("There are enough assets to sell. Placing an order")
                try:

                    neworder=(polo.api('sell', {'currencyPair': shared.PAIR, 'rate': sellprice , 'amount': sellamount }))
                    #print("Adding the order to the timeout list")
                    actual=neworder['orderNumber']
                    shared.TimeoutList1.append(actual)
                    shared.TimeoutList2.append(shared.TICK)
                    shared.TimeoutList3.append('sell')
                    #print(shared.TimeoutList1)
                    #print(shared.TimeoutList2)
                    #print(shared.TimeoutList3)
                except:
                    print("ERROR: Tried to place a sell order but something failed")
            else:
                print("Not enough assets to sell")
                
            # #####################################
            if correctbuy==1 and correctsell==1:
                x1=sellprice-buyprice
                x2=float(sellprice)*(1-float(shared.FEEPCT/200)) - float(buyprice)*(1+float(shared.FEEPCT/200))
                x3=x1-x2
                x4=float(sellprice)*float(sellamount)-float(buyprice)*float(buyamount)   # benefit from difference selling buying
                x5=float(shared.FEEPCT/200)*float(sellprice)*float(sellamount) + float(shared.FEEPCT/200)*float(buyprice)*float(buyamount)   #paid in fees when selling + paid in fees when buying
                x6=x4-x5  # Net benefit after Fees
                print("----------------------------------------------------------------------------")
                print("SPREAD in Price buy/sell = %s [Fee=%2] [NET=%s]" %(x1, x2, x3)) 
                print("AMOUNT in Value buy/sell = %s [Fee=%2] [NET=%s]" %(x4, x5, x6))
                print("----------------------------------------------------------------------------")
            # #####################################                    
        else:
            print("Model does not want to operate at this moment:")


        

    


def main_thread():
    print("Initializing main daemon.")
    running=True
    while running == True:
        try:
            broker_update()
            main_algo()
            print("Tick processing ended. Waiting for next tick. Waiting %s Minutes" % (shared.FRECUENCIA_MINUTOS))
            time.sleep(shared.MAIN_SLEEP_TIME)
        except:
            print("ERROR: There was an unexpected error this tick. Retrying")
        

    


    


if __name__ == "__main__":
    main_thread()