install.packages("twitteR")
install.packages("ROAuth")
install.packages("plyr")
install.packages("ggplot2")
install.packages("wordcloud2")
install.packages("SnowballC")
install.packages("RColorBrewer")
install.packages("stringr")
install.packages("tm")
install.packages("magrittr")
install.packages("multipanelfigure")
install.packages("openNLPdata")
install.packages("qdap")  #<------ NOTA, CONFIGURAR EL JAVA_HOME !!!


library(twitteR)
library(ROAuth)

source("configuration.R")

download.file(url="http://curl.haxx.se/ca/cacert.pem",destfile="cacert.pem")

setup_twitter_oauth(consumer_key,consumer_secret,access_token,access_secret)
cred <- OAuthFactory$new(consumerKey=consumer_key,
                         consumerSecret=consumer_secret,
                         requestURL="https://api.twitter.com/oauth/request_token",
                         accessURL="https://api.twitter.com/oauth/access_token",
                         authURL="https://api.twitter.com/oauth/authorize")

cred$handshake(cainfo="cacert.pem")