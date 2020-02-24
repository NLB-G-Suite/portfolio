library(plyr)
library(ggplot2)
library(SnowballC)
library(RColorBrewer)
library(wordcloud)
library(stringr)
library(tm)
library(magrittr)
library(multipanelfigure)

source("configuration.R")
source("multiplot.R")
source("classify_polarity.R")
source("classify_emotion.R")
source("create_matrix.R")
source("prepare_tweet_search.R")
source("emotion_columns.R")
source("polarity_columns.R")


Origen1=""
Origen2=""
FechaInicial = "2018-12-01"
FechaFinal = "2019-01-01"    
Num=645
NoRetweet=FALSE
RetryLimit=10

Busqueda1="Sanchez+independencia OR independentistas"
Busqueda2="Sanchez+desempleo OR paro"
Busqueda3="Sanchez+terrorismo OR terroristas"
Busqueda4="Sanchez+inmigracion OR inmigrante OR inmigrantes"
Busqueda5="Sanchez+feminismo OR feminista"
Busqueda6="Sanchez+corrupcion OR corrupto"


prep_tw1 <- prepare_tweet_search(Busqueda1,Num,FechaInicial,FechaFinal,RetryLimit,NoRetweet)
prep_tw2 <- prepare_tweet_search(Busqueda2,Num,FechaInicial,FechaFinal,RetryLimit,NoRetweet)
prep_tw3 <- prepare_tweet_search(Busqueda3,Num,FechaInicial,FechaFinal,RetryLimit,NoRetweet)
prep_tw4 <- prepare_tweet_search(Busqueda4,Num,FechaInicial,FechaFinal,RetryLimit,NoRetweet)
prep_tw5 <- prepare_tweet_search(Busqueda4,Num,FechaInicial,FechaFinal,RetryLimit,NoRetweet)
prep_tw6 <- prepare_tweet_search(Busqueda4,Num,FechaInicial,FechaFinal,RetryLimit,NoRetweet)



maxYScale=1000

Coment1a=""
Coment1b=""
Coment2a=""
Coment2b=""
Coment3a=""
Coment3b=""
Coment4a=""
Coment4b=""
Coment5a=""
Coment5b=""
Coment6a=""
Coment6b=""
p1a<-emotion_columns(prep_tw1,FechaInicial,FechaFinal,Coment1a,maxYScale,Busqueda1)
print(p1a)
p1b<-polarity_columns(prep_tw1,FechaInicial,FechaFinal,Coment1b,maxYScale,Busqueda1)
print(p1b)
p2a<-emotion_columns(prep_tw2,FechaInicial,FechaFinal,Coment2a,maxYScale,Busqueda2)
print(p2a)
p2b<-polarity_columns(prep_tw2,FechaInicial,FechaFinal,Coment2b,maxYScale,Busqueda2)
print(p2b)
p3a<-emotion_columns(prep_tw3,FechaInicial,FechaFinal,Coment3a,maxYScale,Busqueda3)
print(p3a)
p3b<-polarity_columns(prep_tw3,FechaInicial,FechaFinal,Coment3b,maxYScale,Busqueda3)
print(p3b)
p4a<-emotion_columns(prep_tw4,FechaInicial,FechaFinal,Coment4a,maxYScale,Busqueda4)
print(p4a)
p4b<-polarity_columns(prep_tw4,FechaInicial,FechaFinal,Coment4b,maxYScale,Busqueda4)
print(p4b)
p5a<-emotion_columns(prep_tw5,FechaInicial,FechaFinal,Coment5a,maxYScale,Busqueda5)
print(p5a)
p5b<-polarity_columns(prep_tw5,FechaInicial,FechaFinal,Coment5b,maxYScale,Busqueda5)
print(p5b)
p6a<-emotion_columns(prep_tw6,FechaInicial,FechaFinal,Coment6a,maxYScale,Busqueda6)
print(p6a)
p6b<-polarity_columns(prep_tw6,FechaInicial,FechaFinal,Coment6b,maxYScale,Busqueda6)
print(p6b)



rm(figure1)
figure1 <- multi_panel_figure(columns=2,rows=6,panel_label_type="lower-alpha",width=460,height=345,panel_clip="false")

figure1 %<>%
  fill_panel(p1a, column = 1, row = 1) %<>%
  fill_panel(p1b, column = 2, row = 1) %<>%
  fill_panel(p2a, column = 1, row = 2) %<>%
  fill_panel(p2b, column = 2, row = 2) %<>%
  fill_panel(p3a, column = 1, row = 3) %<>%
  fill_panel(p3b, column = 2, row = 3) %<>%
  fill_panel(p4a, column = 1, row = 4) %<>%
  fill_panel(p4b, column = 2, row = 4) %<>%
  fill_panel(p5a, column = 1, row = 5) %<>%
  fill_panel(p5b, column = 2, row = 5) %<>%
  fill_panel(p6a, column = 1, row = 6) %<>%
  fill_panel(p6b, column = 2, row = 6) 
print(figure1)

#bmp(filename="figure1.bmp",width=1000,height=900,pointsize=12,units="px",bg="white",type="cairo")
#rect(1,1,1000,900,col="white")
#plot(figure1)
dev.copy(jpeg,filename="plot2.jpg",width=1380,height=1035)
dev.off()

