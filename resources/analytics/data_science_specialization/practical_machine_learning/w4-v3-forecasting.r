# forecasting

library(quantmod)

from.dat <- as.Date("01/01/08",format="%m/%d/%y")
  to.dat <- as.Date("12/31/13",format="%m/%d/%y")
  
getSymbols("GOOG",srv="google",from=from.dat,to=to.dat)


head(GOOG)


mGoog <- to.monthly(GOOG)
googOpen <- Op(mGoog)

ts1 <- ts(googOpen,frequency = 12)
plot(ts1,xlab="Years+1",ylab="GOOG")


wGoog <- to.weekly(GOOG)
googOpen <- Op(wGoog)

ts1 <- ts(googOpen,frequency = 12*4)
plot(ts1,xlab="Years+1",ylab="GOOG")



plot(decompose(ts1),xlab="Years+1")


ts1Train <- window(ts1,start=1,end=5)
ts1Test  <- window(ts1,start=5,end=(7-0.01))

library(forecast)


ets1 <- ets(ts1Train,model="MMM")
fcast<-forecast(ets1)
plot(fcast)
lines(ts1Test,col="red")


accuracy(fcast,ts1Test)