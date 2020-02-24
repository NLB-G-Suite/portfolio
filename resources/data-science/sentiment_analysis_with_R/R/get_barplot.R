source("configuration.R")

get_barplot <-function(fil,maxw,title)
{
  
  wc<-barplot(fil[1:maxw,]$FREQ,names.arg=fil[1:maxw,]$WORD,col=brewer.pal(maxw,"Greens"),border=NA,las=2,ylab="Frecuencia de palabras")
  filename=paste(path,"Temp/",as.character(get_code()),".png",sep="")
  dev.copy(png,filename,width=500,height=400)
  dev.off()  
  print(paste("get_barplot::",filename,sep=""))
return(filename)
}

