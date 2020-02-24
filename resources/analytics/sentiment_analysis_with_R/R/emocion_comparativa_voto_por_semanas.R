library(plyr)
library(ggplot2)
library(SnowballC)
library(RColorBrewer)
library(wordcloud)
library(stringr)
library(tm)
library(magrittr)
library(multipanelfigure)
library(qdap)



source("configuration.R")
source("classify_polarity.R")
source("classify_emotion.R")
source("create_matrix.R")
source("prepare_tweet_search.R")
source("emotion_columns.R")
source("polarity_columns.R")
source("emocion_comparativa.R")
source("get_wordcloud.R")
source("get_barplot.R")


  persona=""
  Origen1=""
  Origen2=""

  Num=1000
  NoRetweet=FALSE
  RetryLimit=5  
  
  
  
  Busqueda1='"votare al pp" OR "voy a votar pp" OR "votare pp" OR "voy a votar al pp" OR "votare al partido popular" OR "yo voto al pp" OR "yo voto al partido popular"'
  Busqueda2='"votare al psoe" OR "voy a votar psoe" OR "votare psoe" OR "voy a votar al psoe" OR "yo voto al psoe"'
  Busqueda3='"votare a vox" OR "voy a votar vox" OR "votare vox" OR "voy a votar a vox" OR "yo voto a vox"'
  Busqueda4='"votare a ciudadanos" OR "voy a votar ciudadanos" OR "voy a votar a ciudadanos" OR "votare Cs" OR "votare a Cs" OR "yo voto a Cs" OR "yo voto a ciudadanos"'
  Busqueda5='"votare a podemos" OR "voy a votar podemos" OR "votare podemos" OR "voy a votar a podemos" OR "yo voto a podemos" OR "yo voto podemos"'
  Busqueda6='"yo no votare" OR "yo no voto" OR "no ire a votar" OR "yo no voy a votar"'
  

  FechaInicial = "2019-04-01"
  FechaFinal = "2019-05-01"    
  emocion_comparativa(Num,RetryLimit,NoRetweet,FechaInicial,FechaFinal,Busqueda1,Busqueda2,Busqueda3,Busqueda4,Busqueda5,Busqueda6,paste("Opinion_Voto_",FechaInicial,"_",FechaFinal,sep=""))
  
  
  