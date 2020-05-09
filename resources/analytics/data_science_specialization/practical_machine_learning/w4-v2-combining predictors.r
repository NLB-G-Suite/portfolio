# Combining predictors


Combining classifiers avg/vote

combining , ++ accuracy  -- interpretability

i.e : boosting, bagging, random forests



# Not clear difference between blending & ensembling

# Basically is what you did with the trad algorithm.

Vote=k1 * Top(vote(x models),a ) + k2 * Top(vote(x models), b) + k3 *Top(vote(x models), c )


# Empirically, ensembles tend to yield better results when there is a 
# significant diversity among the models.[5][6] Many ensemble methods, 
# therefore, seek to promote diversity among the models they combine.


Types of ensembles:
    
    + Bayes optimal classifier
    + bagging
    + boosting
    + Bayesian model averaging
    + Bayesian model combination
    + Bucket of models
    + Stacking

Stacking / Ensembling




library(ISLR);
data(Wage)
library(ggplot2)
library(caret)
names(Wage)


Wage <- subset(Wage, select = -c("logwage"))
# logwage solo es un cálculo del logaritmo del salario (wage)


inBuild <- createDataPartition(y=Wage$wage,p=0.7,list=F)

validation <- Wage [ -inBuild,]
buildData  <- Wage [  inBuild,]

inTrain <- createDataPartition(y=buildData$wage,p=0.7,list=F)

training <- buildData[ inTrain,]
testing  <- buildData[-inTrain,] 



mod1 <- train(wage ~. ,method="glm",data=training)
mod2 <- train(wage ~. ,method="rf",data=training,
            trControl=trainControl(method="cv"),number=3)

pred1 <- predict(mod1,testing)
pred2 <- predict(mod2,testing)

qplot(pred1,pred2,colour=wage,data=testing)


predDF <- data.frame(pred1,pred2,wage=testing$wage)
combModFit <-  train(wage ~. ,method="gam",data=predDF)
combPred <- predict(combModFit,predDF)

# DISPLAYING TESTING ERRORS
# raiz cuadrada de diferencia de cuadrados


sqrt(sum((pred1-testing$wage)^2))

sqrt(sum((pred2-testing$wage)^2))

sqrt(sum((combPred-testing$wage)^2))



# Predicting on validation data set


pred1V <- predict(mod1,validation)
pred2V <- predict(mod2,validation)
predVDF <- data.frame(pred1=pred1V,pred2=pred2V)
combPredV <- predict(combModFit, predVDF)

# DISPLAYING VALIDATION ERRORS

sqrt(sum((pred1V-validation$wage)^2))

sqrt(sum((pred2V-validation$wage)^2))

sqrt(sum((combPredV-validation$wage)^2))














    
    

