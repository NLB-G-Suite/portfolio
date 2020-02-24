emocion_comparativa <- function(Num,RetryLimit=10,NoRetweet=FALSE,FechaInicial,FechaFinal,Busqueda1,Busqueda2,Busqueda3,Busqueda4,Busqueda5,Busqueda6,outputfile)
{  

  require(plyr)
  require(ggplot2)
  require(SnowballC)
  require(RColorBrewer)
  require(wordcloud)
  require(stringr)
  require(tm)
  require(magrittr)
  require(multipanelfigure)
  require(imager)
  require(qdap)

source("configuration.R")
source("classify_polarity.R")
source("classify_emotion.R")
source("create_matrix.R")
source("prepare_tweet_search.R")
source("emotion_columns.R")
source("polarity_columns.R")
source("get_wordcloud.R")


  
get_max_single_prepare <- function(prep_tw)  
{
  class_emo = classify_emotion(prep_tw, algorithm="bayes", prior=1.0)
  emotion = class_emo[,7]
  emotion[is.na(emotion)] = "unknown"
  class_pol = classify_polarity(prep_tw, algorithm="bayes")
  polarity = class_pol[,4]  
  Scale=max(max(table(emotion)),max(table(polarity)))
  return(Scale)
}

#as.character(CODE), <----------------





try(prep_tw1 <- prepare_tweet_search(Busqueda1,Num,FechaInicial,FechaFinal,RetryLimit,NoRetweet,get_code()))
prep_tw2 <- prepare_tweet_search(Busqueda2,Num,FechaInicial,FechaFinal,RetryLimit,NoRetweet,get_code())
prep_tw3 <- prepare_tweet_search(Busqueda3,Num,FechaInicial,FechaFinal,RetryLimit,NoRetweet,get_code())
prep_tw4 <- prepare_tweet_search(Busqueda4,Num,FechaInicial,FechaFinal,RetryLimit,NoRetweet,get_code())
prep_tw5 <- prepare_tweet_search(Busqueda5,Num,FechaInicial,FechaFinal,RetryLimit,NoRetweet,get_code())
prep_tw6 <- prepare_tweet_search(Busqueda6,Num,FechaInicial,FechaFinal,RetryLimit,NoRetweet,get_code())

maxYScale<-max(get_max_single_prepare(prep_tw1),get_max_single_prepare(prep_tw2),get_max_single_prepare(prep_tw3),get_max_single_prepare(prep_tw4),get_max_single_prepare(prep_tw5),get_max_single_prepare(prep_tw6))
print(paste("emocion_comparativa::La escala más alta es ",maxYScale,sep=""))




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

print("Emocion y polaridad calculadas.")

rm(figure1)
#???1380*2,height=1035*2
#figure1 <- multi_panel_figure(columns=4,rows=6,panel_label_type="lower-alpha",width=460*2,height=345*2,panel_clip="false",figure_name=outputfile,unit="px")
figure1 <- multi_panel_figure(columns=4,rows=6,panel_label_type="lower-alpha",width=1380*2,height=1035*2,panel_clip="false",figure_name=outputfile,unit="points")

maxw=200
minw=3

#//////////////////
fil_prep_tw1<-freq_terms(prep_tw1,maxw,at.least=minw,stopwords=tm::stopwords("spanish"))
fil_prep_tw2<-freq_terms(prep_tw2,maxw,at.least=minw,stopwords=tm::stopwords("spanish"))
fil_prep_tw3<-freq_terms(prep_tw3,maxw,at.least=minw,stopwords=tm::stopwords("spanish"))
fil_prep_tw4<-freq_terms(prep_tw4,maxw,at.least=minw,stopwords=tm::stopwords("spanish"))
fil_prep_tw5<-freq_terms(prep_tw5,maxw,at.least=minw,stopwords=tm::stopwords("spanish"))
fil_prep_tw6<-freq_terms(prep_tw6,maxw,at.least=minw,stopwords=tm::stopwords("spanish"))

print("Frecuencias calculadas.")

#wordcloud(fil_prep_tw1$WORD,fil_prep_tw1$FREQ, min.freq=3,max.words=100,colors=brewer.pal(8,"Dark2"),random.order=FALSE)
p1c<-get_wordcloud(fil_prep_tw1,maxw,minw)
p2c<-get_wordcloud(fil_prep_tw2,maxw,minw)
p3c<-get_wordcloud(fil_prep_tw3,maxw,minw)
p4c<-get_wordcloud(fil_prep_tw4,maxw,minw)
p5c<-get_wordcloud(fil_prep_tw5,maxw,minw)
p6c<-get_wordcloud(fil_prep_tw6,maxw,minw)

print("Wordclouds calculadas.")

titleX="Frecuencia de palabras"
p1d<-get_barplot(fil_prep_tw1,20,titleX)
p2d<-get_barplot(fil_prep_tw2,20,titleX)
p3d<-get_barplot(fil_prep_tw3,20,titleX)
p4d<-get_barplot(fil_prep_tw4,20,titleX)
p5d<-get_barplot(fil_prep_tw5,20,titleX)
p6d<-get_barplot(fil_prep_tw6,20,titleX)


print("Barplots calculados.")

figure1 %<>%
  fill_panel(p1a, column = 1, row = 1) %<>%
  fill_panel(p1c, column = 3, row = 1,scaling="fit") %<>%
  fill_panel(p1d, column = 4, row = 1,scaling="fit") %<>%
  fill_panel(p1b, column = 2, row = 1) %<>%
  fill_panel(p2a, column = 1, row = 2) %<>%
  fill_panel(p2c, column = 3, row = 2,scaling="fit") %<>%
  fill_panel(p2d, column = 4, row = 2,scaling="fit") %<>%
  fill_panel(p2b, column = 2, row = 2) %<>%
  fill_panel(p3a, column = 1, row = 3) %<>%
  fill_panel(p3c, column = 3, row = 3,scaling="fit") %<>%
  fill_panel(p3d, column = 4, row = 3,scaling="fit") %<>%
  fill_panel(p3b, column = 2, row = 3) %<>%
  fill_panel(p4a, column = 1, row = 4) %<>%
  fill_panel(p4c, column = 3, row = 4,scaling="fit") %<>%
  fill_panel(p4d, column = 4, row = 4,scaling="fit") %<>%
  fill_panel(p4b, column = 2, row = 4) %<>%
  fill_panel(p5a, column = 1, row = 5) %<>%
  fill_panel(p5c, column = 3, row = 5,scaling="fit") %<>%
  fill_panel(p5d, column = 4, row = 5,scaling="fit") %<>%
  fill_panel(p5b, column = 2, row = 5) %<>%
  fill_panel(p6a, column = 1, row = 6) %<>%
  fill_panel(p6c, column = 3, row = 6,scaling="fit") %<>%
  fill_panel(p6d, column = 4, row = 6,scaling="fit") %<>%
  fill_panel(p6b, column = 2, row = 6) 
print(figure1)


filename=paste(path,"Analisis/",outputfile,".png",sep="")
#dev.copy(png,filename,width=1380*2,height=1035*2)
dev.copy(png,filename,width=1380*2,height=1035*2)
dev.off()
print(paste("emocion_comparativa::Nuevo fichero de salida en ",filename,sep=""))

}