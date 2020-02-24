####################################################
#Chunk -7- Classification by emotions and polarity                
####################################################

library(twitteR)
#library(sentiment) not suported under R ver 3.0 Used as funcion
library(plyr)
library(ggplot2)
library(wordcloud)
library(RColorBrewer)
library(stringr)
library(tm)

source("configuration.R")
source("multiplot.R")

source("classify_polarity.R")
source("classify_emotion.R")
source("create_matrix.R")

BusquedaEmotion="@podemos"


ListaEmotion.list <- searchTwitter(BusquedaEmotion, n=150,since="2018-12-28",until="2019-01-01")
#ListaEmotion.list <- searchTwitter(BusquedaEmotion, n=150)  
ListaEmotion.df = twListToDF(ListaEmotion.list)  
write.csv(ListaEmotion.df, file=paste(path,'ListaEmotionTweets.csv',sep=""), row.names=F)



# Get the text
ListaEmotion_txt = sapply(ListaEmotion.list, function(x) x$getText())

# Prepare text for the analysis
ListaEmotion_txt = gsub("(RT|via)((?:\\b\\W*@\\w+)+)", "", ListaEmotion_txt)
ListaEmotion_txt = gsub("@\\w+", "", ListaEmotion_txt)
ListaEmotion_txt = gsub("[[:punct:]]", "", ListaEmotion_txt)
ListaEmotion_txt = gsub("[[:digit:]]", "", ListaEmotion_txt)
ListaEmotion_txt = gsub("http\\w+", "", ListaEmotion_txt)
ListaEmotion_txt = gsub("[ \t]{2,}", "", ListaEmotion_txt)
ListaEmotion_txt = gsub("^\\s+|\\s+$", "", ListaEmotion_txt)


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
ListaEmotion_txt = sapply(ListaEmotion_txt, try.error)


# remove NAs in ListaEmotion_txt
ListaEmotion_txt = ListaEmotion_txt[!is.na(ListaEmotion_txt)]
names(ListaEmotion_txt) = NULL





#classify emotion
class_emo = classify_emotion(ListaEmotion_txt, algorithm="bayes", prior=1.0)

#get emotion best fit
emotion = class_emo[,7]

# substitute NA's by "unknown"
emotion[is.na(emotion)] = "unknown"


# classify polarity
class_pol = classify_polarity(ListaEmotion_txt, algorithm="bayes")


# get polarity best fit
polarity = class_pol[,4]


# data frame with results
sent_df = data.frame(text=ListaEmotion_txt, emotion=emotion, 
                     polarity=polarity, stringsAsFactors=FALSE)



# sort data frame
sent_df = within(sent_df,
                 emotion <- factor(emotion, levels=names(sort(table(emotion), decreasing=TRUE))))


# plot distribution of emotions
p1<-ggplot(sent_df, aes(x=emotion)) +
  geom_bar(aes(y=..count.., fill=emotion)) +
  scale_fill_brewer(palette="Dark2") +
  labs(x="emotion categories", y="number of tweets", 
       title = paste("Analisis de sentimiento sobre : " , BusquedaEmotion ,"\n(clasificados por emocion)",sep=""),
       plot.title = element_text(size=12))


# plot distribution of emotions
p2<-ggplot(sent_df, aes(x=polarity)) +
  geom_bar(aes(y=..count.., fill=polarity)) +
  scale_fill_brewer(palette="RdGy") +
  labs(x="polarity categories", y="number of tweets",
       title = paste("Analisis de sentimiento sobre : ",BusquedaEmotion , "\n(classificados por emocion)",sep=""),
       plot.title = element_text(size=12))


multiplot(p1,p2)

