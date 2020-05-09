# In sample versus out of sample errors

library(kernlab);data(spam);set.seed(333)
smallSpam <- spam[sample(dim(spam)[1],size=10),]
spamLabel <- (smallSpam$type=="spam")*1 + 1
plot(smallSpam$capitalAve,col=spamLabel)

rule1 <- function(x){
    prediction <- rep(NA,length(x))
    prediction[x>0] <- "nonspam"
    prediction[x<1.7 | (x>1.78 & x<2.6) | x>17.75 ] <- "spam"
    return(prediction)
}

rule2 <- function(x){
    prediction <- rep(NA,length(x))
    prediction[ x>2.4 ] <- "nonspam"
    prediction[ x<2.4 ] <- "spam"
    return(prediction)
}



table(rule1(smallSpam$capitalAve),smallSpam$type)
table(rule1(spam$capitalAve),spam$type)

table(rule2(smallSpam$capitalAve),smallSpam$type)
table(rule2(spam$capitalAve),spam$type)

table(smallSpam$capitalAve,spamLabel)

