rm(list = ls(all.names = TRUE)) #will clear all objects includes hidden objects.
gc() 


########################
## COVARIATE CREATION ##
########################

library(kernlab)
data(spam)
spam$capitalAveSq <- spam$capitalAve^2


# Level 1. Raw data -> covariates

       # for example, pages to word frquency, frequency of phrases. Google n-gram etc, frequency capital letters
       # Images, edges, corners ,...
       # ...

# Level 2. Tidy covariates -> new covariates

       # ONLY ON THE TRAINING SET
       # BEST TO DO IT WITH EXPLORATORY ANALYSIS


###########
# Example #
###########

library(ISLR); library(caret) ; data(Wage)
inTrain <- createDataPartition(y=Wage$wage,p=0.7,list=FALSE)

training <- Wage[ inTrain,]
testing  <- Wage[-inTrain,]


# Common covariates to add, dummy variables

table(training$jobclass)


dummies <- dummyVars(wage ~jobclass, data=training)

# Removing Zero Covariates

nsv <- nearZeroVar(training, saveMetrics=TRUE)
nsv

library(splines)
bsBasis <-bs(training$age,df=3)


# Fitting cuves with splines

lml <- lm(wage ~ bsBasis,data=training)
plot(training$age,training$wage,pch=19,cex=0.5)
points(training$age,predict(lml,newdata=training),col="red",pch=19,cex=0.5)

predict(bsBasis,age=testing$age)
    
    
    
    