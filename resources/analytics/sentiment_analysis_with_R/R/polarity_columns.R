


polarity_columns <- function(BusquedaPreparada,FechaInicial,FechaFinal,Coment,Scale,Busqueda) {


  
  
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
source("classify_polarity.R")
source("classify_emotion.R")
source("create_matrix.R")
  
  
  #TEST
  #////////////////////////////////////////
  #Busqueda = "Susana+2018"    ## <------------------
  #FechaInicial = "2018-12-28"              ## <------------------
  #FechaFinal = "2019-01-02"              ## <------------------
  #Origen = ""                          ## <------------------
  #Busqueda = "Susana Diaz"             ## <------------------  
  #BusquedaPreparada<-prepare_tweet_search(Busqueda,FechaIni,FechaFin)

  #classify emotion
  class_emo = classify_emotion(BusquedaPreparada, algorithm="bayes", prior=1.0)
  
  #get emotion best fit
  emotion = class_emo[,7]
  
  # substitute NA's by "unknown"
  emotion[is.na(emotion)] = "unknown"
  
  
  # classify polarity
  class_pol = classify_polarity(BusquedaPreparada, algorithm="bayes")
  
  
  # get polarity best fit
  polarity = class_pol[,4]
  
  
  # data frame with results
  sent_df = data.frame(text=BusquedaPreparada, emotion=emotion, 
                       polarity=polarity, stringsAsFactors=FALSE)
  
  
  

rm(title1)
#title1 = paste(Origen,"-> Sentimiento : " , Busqueda , "\n[ Emocion Tweets desde ",FechaInicial," hasta ",FechaFinal," ] ",sep="")
title1=paste("Análisis Polaridad tweets de ",FechaInicial," >> ",FechaFinal,"\nBúsqueda:[" , Busqueda , "] ",sep="")


#TEST
#/////////////////////////////////
#Scale=max(table(emotion))  ## <------------------


g1<-ggplot(sent_df, aes(x=polarity)) +
  geom_bar(aes(y=..count.., fill=polarity),width=0.7) +
  scale_fill_brewer(palette="Greens") +
  coord_cartesian(ylim=c(0,Scale)) +
  labs(x=Coment, y="número de tweets",
       subtitle = title1,
       plot.title = element_text(size=1))+
  theme(axis.title.x=element_text(size=rel(0.85)),panel.background=element_rect(fill="white"),panel.grid.major.y=element_line(size=0.15,linetype='solid',colour="#eeeeee"))
return(g1)
}