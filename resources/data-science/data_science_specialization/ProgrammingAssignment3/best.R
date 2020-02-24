best <- function(state, outcome) 
{
  ## Reading outcome data csv
  data <- read.csv("outcome-of-care-measures.csv",colClasses = "character")
  ## Checking if the state and the outcome are both valid
  if (!state %in% data$State )
  {
    stop("invalid state") 
  }
  else
  {
    data<-data[data$State==state,]
  }
  if (! outcome %in% c("heart attack","heart failure","pneumonia"))
  {
    stop("invalid outcome")
  }
  else
  {
    ## filtering by outcome
    if (outcome == "heart attack")
    {
      data[,11]<-as.numeric(data[,11])
      filter <-data[data[,11]==min(data[,11],na.rm=T),2]
    }
    if (outcome == "heart failure")
    {
      data[,17]<-as.numeric(data[,17])
      filter <-data[data[,17]==min(data[,17],na.rm=T),2]
    }
    if (outcome == "pneumonia")
    {
      data[,23]<-as.numeric(data[,23])
      filter <-data[data[,23]==min(data[,23],na.rm=T),2]
    }
  }
  ## return the filtered value after removing na
  ret <- filter[! is.na(filter)]

  ## Return the hospital name in that state with lowest 30-day death rate
  return(ret)
}
