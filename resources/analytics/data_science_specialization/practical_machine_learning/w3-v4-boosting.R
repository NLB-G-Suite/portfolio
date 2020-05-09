# Boosting

# ADAPTIVE BOOST.

# Gives power to those predictors failing, reducing outliers and noise and
# making them work together with the rest.

# If they are just better than random, they have something to say.


# Multiple types of boostings

# gbm - boosting with trees
# mboost - model based boosting
# ada - statistical boosting based on additive logistic regression
# gamBoost - for boosting generalized additive models

# (most in caret)


library(ISLR);
data(Wage)
library(ggplot2)
library(caret)
Wage <- subset(Wage,select = -c(logwage))

inTrain <- createDataPartition(y=Wage$wage,p=0.7,list=F)

training <- Wage[inTrain,] ; testing <- Wage[-inTrain,]

dim(training);dim(testing)


# Fitting the model using trees

modFit <- train(wage ~. , method ="gbm", data=training, verbose=FALSE)

qplot(predict(modFit,testing),wage,data=testing)