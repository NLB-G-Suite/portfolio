
##################################
### Predicting with Regression ###
##################################


    # Key Ideas
            
        # Fit a simple regression model
        # Plug in new covariates and multiply by the coefficients
        # Useful when the linear model is (nearly) correct

    # PROs:

        # Easy to implement
        # Easy to interpret

    # CONs:

        # Often poor performance in nonlinear settings




# EXAMPLE: Old Faithful Eruptions
#--------------------------------


library(caret);data(faithful);set.seed(333)

inTrain <- createDataPartition(y = faithful$waiting, p=0.5, list=FALSE)


trainFaith <- faithful[ inTrain,] 
testFaith  <- faithful[-inTrain,]

head(trainFaith)


# Plotting duration versus waiting time

plot(trainFaith$waiting,trainFaith$eruptions,pch=19,col="blue",xlab="Waiting time",ylab="Eruption Duration")


# Fitting a linear model

lm1 <- lm(eruptions ~ waiting, data=trainFaith)
summary(lm1)


# Model fit

plot(trainFaith$waiting,trainFaith$eruptions,pch=19,col="blue",xlab="Waiting time",ylab="Eruption Duration")
lines(trainFaith$waiting, lm1$fitted,lwd=3)

# Predictin a new value

coef(lm1)[1]+coef(lm1)[2]*80

newdata <- data.frame(waiting=80)
predict(lm1,newdata)



# Plotting predictions - training and test along each other

par(mfrow=c(1,2))

plot(trainFaith$waiting,trainFaith$eruptions,pch=12,col="blue",xlab="Waiting time",ylab="Eruption Duration",main="TRAIN DATA")
lines(trainFaith$waiting,predict(lm1),lwd=3)

plot(testFaith$waiting,testFaith$eruptions,pch=12,col="blue",xlab="Waiting time",ylab="Eruption Duration",main="TEST DATA")
lines(testFaith$waiting,predict(lm1,newdata=testFaith),lwd=3)

# Get training set/test set errors

    # Calculating RMSE on training
    
    sqrt(sum((lm1$fitted-trainFaith$eruptions)^2))
    
    # Calculating RMSE on test
    
    sqrt(sum((predict(lm1,newdata=testFaith)-testFaith$eruptions)^2))
    
    
# Adding Prediction Intervals
    
    pred1 <- predict(lm1,newdata=testFaith,interval="prediction")
    ord <- order(testFaith$waiting)
    plot(testFaith$waiting,testFaith$eruptions,pch=19,col="blue")
    matlines(testFaith$waiting[ord],pred1[ord,],type="l",,col=c(1,2,2),lty=c(1,1,1),lwd=3)
    
    
    
    
#######################################
### Same process with caret Package ###
#######################################    
    
modFit <-train(eruptions ~ waiting, data = trainFaith , method ="lm")    
summary(modFit$finalModel)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    







