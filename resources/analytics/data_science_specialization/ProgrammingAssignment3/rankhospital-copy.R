filter <- function(data, code, num)
{
  data[,code] <- as.numeric(data[,code])  
  len=length(data[,code])
  if (num=="best") 
  {
    fil <- data[data[,code]==min(data[,code],na.rm=T),2]
    fil <- fil[!is.na(fil)]
  } 
  else if (num=="worst")
  {
    fil <- data[data[,code]==max(data[,code],na.rm=T),2]
    fil <- fil[!is.na(fil)]
  } 
  else if (num>length(data[,code])) 
  { 
    fil <-NA 
  }
  else 
  {
    fil <- data[data[,code]==order(data[,code])[num],2]
    fil <- fil[!is.na(fil)]
  }
  return(fil)
}



rankhospital <- function(state, outcome, num = "best") 
{
  ## Reading outcome data csv
  data <- read.csv("outcome-of-care-measures.csv",colClasses = "character")
  ## Checking if the state and the outcome are both valid
  if (!state %in% data$State ) {stop("invalid state")}
  else { data<-data[data$State==state,]}
  if (! outcome %in% c("heart attack","heart failure","pneumonia")) {stop("invalid outcome")}
  else 
  {
    ## filtering by outcome
    if (outcome == "heart attack")  ret <- filter(data,11,num)
    if (outcome == "heart failure") ret <- filter(data,17,num)    
    if (outcome == "pneumonia")     ret <- filter(data,23,num)    
  }
  ## Return the hospital name in that state with lowest 30-day death rate
  return(ret)
}  