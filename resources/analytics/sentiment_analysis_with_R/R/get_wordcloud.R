source("configuration.R")

get_wordcloud <-function(qqq,maxw,minw)
{
  #par(bg="black")
  wc <- wordcloud(qqq$WORD,qqq$FREQ, min.freq=minw,max.words=maxw,colors=brewer.pal(8,"Dark2"),random.order=FALSE,scale=c(6,0.5),random.color=FALSE,use.r.layout = FALSE,rot.per=0,font=2,family="serif")
  filename=paste(path,"Temp/",as.character(get_code()),".png",sep="")
  dev.copy(png,filename,width=800,height=800)
  dev.off()  
  print(paste("get_wordcloud::",filename,sep=""))
return(filename)
}


