prepare_tweet_search <- function (Busqueda,Num,FechaInicial=NULL,FechaFinal=NULL,RetryLimit=120,NoRetweet=FALSE,CODE) {
  
  require(plyr)
  require(ggplot2)
  require(SnowballC)
  require(RColorBrewer)
  require(wordcloud)
  
  require(stringr)
  require(tm)
  require(magrittr)
  require(multipanelfigure)
  
  
  #source("configuration.R")
  #source("multiplot.R")
  
  source("classify_polarity.R")
  source("classify_emotion.R")
  source("create_matrix.R")

  # DEBUGGING=FALSE
  # if (DEBUGGING) {
  # Busqueda='"yo votare a vox"'
  # Origen1=""
  # Origen2=""
   #FechaInicial = "2018-12-08"
   #FechaFinal = "2019-01-07"
   #Num=2000
   #NoRetweet=FALSE
   #RetryLimit=5
   #MaxYScale=600

  print(paste("Iniciando Búsqueda: ",Busqueda,sep=""))
  
  try(ListaEmotion1.list <- searchTwitter(Busqueda, n=Num,lang="es",since=FechaInicial,until=FechaFinal,retryOnRateLimit=RetryLimit)  )
  head(ListaEmotion1.list)
  nrow(ListaEmotion1.list)
  if (NoRetweet)
  {
    ListaEmotion1.df = twListToDF(strip_retweets(ListaEmotion1.list))  
  } else  {
    #if (nrow(ListaEmotion1.list)>0) {
    ListaEmotion1.df = twListToDF(ListaEmotion1.list)  
    #} else
    #{
    #  ListaEmotion1.df=""
    #}
  }
  write.csv(ListaEmotion1.df, file=paste(path,'Temp/',"Tweets_",CODE,'.csv',sep=""), row.names=F)  
  
  # Get the text
  ListaEmotion1_txt = sapply(ListaEmotion1.list, function(x) x$getText())
  #}
  
  # Prepare text for the analysis
  ListaEmotion1_txt = gsub("(RT|via)((?:\\b\\W*@\\w+)+)", "", ListaEmotion1_txt)
  ListaEmotion1_txt = gsub("@\\w+", "", ListaEmotion1_txt)
  ListaEmotion1_txt = gsub("[[:punct:]]", "", ListaEmotion1_txt)
  ListaEmotion1_txt = gsub("[[:digit:]]", "", ListaEmotion1_txt)
  ListaEmotion1_txt = gsub("http\\w+", "", ListaEmotion1_txt)
  ListaEmotion1_txt = gsub("[ \t]{2,}", "", ListaEmotion1_txt)
  ListaEmotion1_txt = gsub("^\\s+|\\s+$", "", ListaEmotion1_txt)
  
  
  try.error = function(x)
    
  {  
    # create missing value
    y = NA
    # tryCatch error
    try_error = tryCatch(tolower(x), error=function(e) e)
    # if not an error
    if (!inherits(try_error, "error"))
      y = tolower(x)
    # result
    return(y)
  }
  
  # lower case using try.error with sapply 
  ListaEmotion1_txt = sapply(ListaEmotion1_txt, try.error)
  
  # remove NAs in ListaEmotion1_txt
  ListaEmotion1_txt = ListaEmotion1_txt[!is.na(ListaEmotion1_txt)]
  names(ListaEmotion1_txt) = NULL  
  return(ListaEmotion1_txt)
}