

cat("\014")
print("HOW TO DISPLAY TRADITIONAL CANDLESTICK CHART IN R FROM A CSV FILE")
print("-----------------------------------------------------------------")

library(plotly)
library(quantmod)
print("    - Loading libraries plotly and quantmod")

source_dir<-"e:/dev/bitcoin-OHLC-generator/"
source_data<-"btcusd.csv"
print(paste("    - Using file located at ",source_dir,source_data,sep=""))
print("    - We load the .csv file obtained from aggregating 5 different exchanges with 5 minute OHCL Open, High, low, close, volume candles. From 2012 to jan 2020")


dat <- read.csv(paste(source_dir,source_data,sep=""),header=TRUE)
print("")
print("    - We get it into a dataframe")
lastcandles <- 2000
df <- as.data.frame(dat)
print(paste("    - We will be using the last ",lastcandles," candles",sep=""))
df <- tail(df,lastcandles)

names(df) <- c("date","open","high","low","close","volume")

print("    - We redirect the output of plot_ly with the dataframe configuration for each column, title, etc")
p <- df %>%
  plot_ly(x= ~date, type="candlestick",
          open= ~open, close= ~close,
          high= ~high, low  = ~low,name="BTCUSD") %>%
  layout(yaxis=list(title="Price"))


# plot volume bar chart
pp <- df %>%
  plot_ly(x=~date, y=~volume, type='bar', name = "Volume"
        ) %>%
  layout(yaxis = list(title = "Volume"))

# create rangeselector buttons
rs <- list(visible = TRUE, x = 0.5, y = -0.055,
           xanchor = 'center', yref = 'paper',
           font = list(size = 9),
           buttons = list(
             list(count=1,
                  label='RESET',
                  step='all'),
             list(count=1,
                  label='1 YR',
                  step='year',
                  stepmode='backward'),
             list(count=3,
                  label='3 MO',
                  step='month',
                  stepmode='backward'),
             list(count=1,
                  label='1 MO',
                  step='month',
                  stepmode='backward')
             
           ))

# subplot with shared x axis
p <- subplot(p, pp, heights = c(0.7,0.2), nrows=2,
             shareX = TRUE, titleY = TRUE) %>%
  layout(title = paste("BTCUSD ",Sys.Date()),
         xaxis = list(rangeselector = rs),
         legend = list(orientation = 'h', x = 0.5, y = 1,
                       xanchor = 'center', yref = 'paper',
                       font = list(size = 10),
                       bgcolor = 'transparent'))

p

