
######################################################
### PREDICTING WITH REGRESSION MULTIPLE COVARIATES ###
######################################################


# EXAMPLE: WAGE DATA
#--------------------


library(ISLR)
library(ggplot2)
library(caret)

data(Wage)
Wage <- subset(Wage,select = -c(logwage)) # log wage is what we are going to predict, so we remove it
summary(Wage)

    # We can see that we have all males, and from Middle Atlantic. 
    # We should probably remove those covariates as they don't provide anything


# Get training /test sets

    inTrain <- createDataPartition(y=Wage$wage,p=0.7,list=FALSE)
    
    training <- Wage[ inTrain,]
    testing  <- Wage[-inTrain,]
    
    dim(training)
    dim(testing)

# EXPLORATORY ANALYSIS TO IDENTIFY BEST COVARIATES    
        
    # Feature Plot. (Exploring covariates probably)
        
        featurePlot(x=training[,c("age","education","jobclass")],y=training$wage,plot="pairs")
    
    # Plot Age versus wage
        
        qplot(age,wage,data=training)
    
        qplot(age,wage,data=training, colour=jobclass)
        
        qplot(age,wage,data=training, colour=education)
        
# Fitting a linear model
    
        modFit <- train(wage ~ age + jobclass + education, method="lm", data=training)
        finMod <- modFit$finalModel
        print(modFit)

        
        
# DIAGNOSTICS
    
    # we plot the relation between the values the model has fitted and those that were not
            
    plot(finMod,1,pch=19,cex=0.5,col="#00000010")
    
    
# Coloring by variables not used in the model
    
    qplot(finMod$fitted, finMod$residuals,colour=race,data=training)
    
    qplot(finMod$fitted, finMod$residuals,colour=education,data=training)
    
    qplot(finMod$fitted, finMod$residuals,colour=jobclass,data=training)
    
    
# Another useful tool is PLOTTING BY INDEX. The index is the datarow
    
    plot(finMod$residuals,pch=19)
    
    # It could happen that all the residuals occur at a specif time (or depending on how the data is ordered)
    
# Another tool is Predicting versus truth in test set
    
    pred <- predict(modFit,testing)
    qplot(wage,pred,colour=year,data=testing)
    
    # This is like a postmortem to determine if your analysis works or not
    

# IF YOU WANT TO USE ALL COVARIATES
    
    modFitAll <- train(wage ~ . , data=training, method="lm")
    pred <-predict(modFitAll,testing)
    qplot(wage,pred,data=testing)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    