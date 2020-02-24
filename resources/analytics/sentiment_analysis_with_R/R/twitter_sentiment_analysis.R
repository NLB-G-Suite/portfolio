
# Guide videos here http://txcdk.unt.edu/iralab/how
#############################################
# Chunk - 1 - Authenticate with twitter API
#############################################

library(twitteR)
library(ROAuth)
library(plyr)
library(stringr)
library(ggplot2)
library(tm)

source("configuration.R")


############################################################
# Chunk  - 2 - Twitter Scrape  #Lista1 #Lista2 #Lista3  
############################################################
Lista1.list <- searchTwitter(Busqueda1, n=150)  
Lista1.df = twListToDF(Lista1.list)  
write.csv(Lista1.df, file=paste(path,'Lista1Tweets.csv',sep=""), row.names=F)

Lista2.list <- searchTwitter(Busqueda2, n=150)  
Lista2.df = twListToDF(Lista2.list)  
write.csv(Lista2.df, file=paste(path,'Lista2Tweets.csv',sep=""), row.names=F)

Lista3.list <- searchTwitter(Busqueda3, n=150)  
Lista3.df = twListToDF(Lista3.list)  
write.csv(Lista3.df, file=paste(path,'Lista3Tweets.csv',sep=""), row.names=F)


###############################
#Chunk -3- Sentiment Function     
###############################

library (plyr)
library (stringr)

score.sentiment = function(sentences, pos.words, neg.words, .progress='none')  
{  
  require(plyr)  
  require(stringr)         
  # we got a vector of sentences. plyr will handle a list  
  # or a vector as an "l" for us  
  # we want a simple array ("a") of scores back, so we use   
  # "l" + "a" + "ply" = "laply":  
  
  scores = laply(sentences, function(sentence, pos.words, neg.words) {     
    # clean up sentences with R's regex-driven global substitute, gsub():     
    sentence = gsub('[[:punct:]]', '', sentence)     
    sentence = gsub('[[:cntrl:]]', '', sentence)     
    sentence = gsub('\\d+', '', sentence)     
    # and convert to lower case:     
    sentence = tolower(sentence)     
    # split into words. str_split is in the stringr package     
    word.list = str_split(sentence, '\\s+')     
    # sometimes a list() is one level of hierarchy too much     
    words = unlist(word.list)     
    # compare our words to the dictionaries of positive & negative terms     
    pos.matches = match(words, pos.words)  
    neg.matches = match(words, neg.words)     
    # match() returns the position of the matched term or NA  
    # we just want a TRUE/FALSE:     
    pos.matches = !is.na(pos.matches)     
    neg.matches = !is.na(neg.matches)      
    # and conveniently enough, TRUE/FALSE will be treated as 1/0 by sum():    
    score = sum(pos.matches) - sum(neg.matches)  
    return(score)  
  }, pos.words, neg.words, .progress=.progress )  
  scores.df = data.frame(score=scores, text=sentences)  
  return(scores.df)  
} 


############################################
#Chunk - 4 - Scoring Tweets & Adding a column      
############################################

# =======================
#   4. Citation Info for lexicon en espaniol
# 
# If you use these lexicons please cite:
#   
#   @InProceedings{Perez12,
#                  author =       {Veronica Perez Rosas , Carmen Banea, Rada Mihalcea},
#                  title =            {Learning Sentiment Lexicons in Spanish},
#                  booktitle =    {Proceedings of the international conference on Language
#                                  Resources and Evaluation (LREC)},
#                  address =      {Istanbul, Turkey},
#                  year =            {2012}
#   }

# load lexicom
sentimentcomb<-read.csv(paste(path,"subjectivity.csv",sep=""),header=FALSE,sep=",")
positive<-t(subset(sentimentcomb,V3=="positive",select=V1))

negative<-t(subset(sentimentcomb,V3=="negative",select=V1))

# Añadir palabras positivas o negativas a gusto
pos.words = c(positive, 'upgrade',"bueno","bien","chereve","amplia","ampliacion")
neg.words = c(negative, 'wtf', 'wait','waiting', 'epicfail', 'mechanical',"mal","malo","mierda",
              "prohÃ?be", "polariza", "irresponsable", "prohibirÃ¡", "cagada",
              "lucha","olvido","polarizÃ³","incertidumbre","inconformes","inconforme",
              "temen","prohibira","faltan","desplazados",
              "desplazado","gentuza")

#Import 3 csv
DatasetLista1 <- read.csv(paste(path,"Lista1Tweets.csv",sep=""))
DatasetLista1$text<-as.factor(DatasetLista1$text)

DatasetLista2 <- read.csv(paste(path,"Lista2Tweets.csv",sep=""))
DatasetLista2$text<-as.factor(DatasetLista2$text)

DatasetLista3 <- read.csv(paste(path,"Lista3Tweets.csv",sep=""))
DatasetLista3$text<-as.factor(DatasetLista3$text)

###########################
#Score all tweets 
#############################
Lista1.scores = score.sentiment(DatasetLista1$text, pos.words,neg.words, .progress='text')
Lista2.scores = score.sentiment(DatasetLista2$text, pos.words,neg.words, .progress='text')
Lista3.scores = score.sentiment(DatasetLista3$text, pos.words,neg.words, .progress='text')


write.csv(Lista1.scores,file=paste(path,"Lista1Scores.csv",sep=""),row.names=TRUE)
write.csv(Lista2.scores,file=paste(path," Lista2Scores.csv",sep=""),row.names=TRUE)
write.csv(Lista3.scores,file=paste(path,"Lista3Scores.csv",sep=""),row.names=TRUE)

Lista1.scores$Team = Busqueda1
Lista2.scores$Team = Busqueda2
Lista3.scores$Team = Busqueda3

############################# 
#Chunk -5.5- loading  sentiment functions       
#############################
# source("sentiment.R")
# t1<-sentiment(text=c("I hate my apple", "I love my apple"))
source("classify_polarity.R")
source("classify_emotion.R")
source("create_matrix.R")


############################# 
#Chunk -5- simple Visualization        
#############################

x<-Lista1.scores$score
y<-Lista2.scores$score
z<-Lista3.scores$score

#hist(x,breaks="FD")
#breaks<-pretty(range(x,n=nclass.FD(x),min.n=0.5))
#bwidth<-breaks[2]-breaks[1]
qplot(x,binwidth=0.5)

#hist(y,breaks="FD")
#breaks<-pretty(range(y,n=nclass.FD(y),min.n=0.5))
#bwidth<-breaks[2]-breaks[1]
qplot(y,binwidth=0.5)


#hist(z,breaks="FD")
#breaks<-pretty(range(z,n=nclass.FD(z),min.n=0.5))
#bwidth<-breaks[2]-breaks[1]
qplot(z,binwidth=0.5)


#################################
#Chunk -6- Comparing 3 data sets	              
#################################




all.scores = rbind(Lista1.scores, Lista2.scores, Lista3.scores)
ggplot(data=all.scores) + # ggplot works on data.frames, always
  geom_bar(mapping=aes(x=score, fill=Team), binwidth=0.5) +
  facet_grid(Team~.) + # make a separate plot for each hashtag
  theme_bw() + scale_fill_brewer() # plain display, nicer colors







