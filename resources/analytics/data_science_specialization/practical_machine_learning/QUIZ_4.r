# QUIZ 4


#1 .- QUESTION

# For this quiz we will be using several R packages. R package versions change over time, the right answers have been checked using the following versions of the packages.
# 
# AppliedPredictiveModeling: v1.1.6
# 
# caret: v6.0.47
# 
# ElemStatLearn: v2012.04-0
# 
# pgmm: v1.1
# 
# rpart: v4.1.8
# 
# gbm: v2.1
# 
# lubridate: v1.3.3
# 
# forecast: v5.6
# 
# e1071: v1.6.4
# 
# If you aren't using these versions of the packages, your answers may not exactly match the right answer, but hopefully should be close.
# 
# Load the vowel.train and vowel.test data sets:

library(ElemStatLearn)

data(vowel.train)
data(vowel.test)

# Set the variable y to be a factor variable in both the training and 
# test set. Then set the seed to 33833. Fit (1) a random forest 
# predictor relating the factor variable y to the remaining variables 
# and (2) a boosted predictor using the "gbm" method. Fit these both 
# with the train() command in the caret package.
# 
# What are the accuracies for the two approaches on the test data 
# set? What is the accuracy among the test set samples where the two 
# methods agree?

vowel.train$y <- as.factor(vowel.train$y)
vowel.test$y  <- as.factor(vowel.test$y)

set.seed(33833)

ytrain_rf <- train( y ~. , data = vowel.train  ,method ="rf")
ytrain_bst <- train(y~. , data = vowel.train , method ="gbm")

pred_rf <- predict(ytrain_rf,vowel.test)
pred_bst <- predict(ytrain_bst,vowel.test)


pred_agreement <- pred_rf==pred_bst

common_pred <- pred_rf[pred_agreement]


library(caret)

confusionMatrix(as.factor(pred_rf),as.factor(vowel.test$y))
confusionMatrix(as.factor(pred_bst),as.factor(vowel.test$y))
confusionMatrix(as.factor(pred_rf[pred_agreement]),as.factor(vowel.test$y[pred_agreement]))

#----------------------------------------------------------------
#----------------------------------------------------------------

#2 .- QUESTION

# Load the Alzheimer's data using the following commands

library(caret)
library(gbm)
set.seed(3433)
library(AppliedPredictiveModeling)
data(AlzheimerDisease)
adData = data.frame(diagnosis,predictors)
inTrain = createDataPartition(adData$diagnosis, p = 3/4)[[1]]
training = adData[ inTrain,]
testing = adData[-inTrain,]


# Set the seed to 62433 and predict diagnosis with all the other 
# variables using a random forest ("rf"), boosted trees ("gbm") and 
# linear discriminant analysis ("lda") model. Stack the predictions 
# together using random forests ("rf"). What is the resulting 
# accuracy on the test set? Is it better or worse than each of the 
# individual predictions?

set.seed(62433)

train_rf <- train(diagnosis ~. , data=training, method="rf")
train_gbm <- train(diagnosis ~. , data=training, method="gbm")
train_lda <- train(diagnosis ~. , data=training, method="lda")

testing_pred_rf  <- predict(train_rf,testing)
testing_pred_gbm <- predict(train_gbm,testing)
testing_pred_lda <- predict(train_lda,testing)


predDF <- data.frame(testing_pred_rf,
                     testing_pred_gbm,
                     testing_pred_lda,
                     diagnosis=testing$diagnosis)
combModFit <-  train(diagnosis ~. ,method="rf",data=predDF)

combPred <- predict(combModFit,predDF)


confusionMatrix(as.factor(testing_pred_rf),as.factor(testing$diagnosis))$overall
confusionMatrix(as.factor(testing_pred_gbm),as.factor(testing$diagnosis))$overall
confusionMatrix(as.factor(testing_pred_lda),as.factor(testing$diagnosis))$overall
confusionMatrix(as.factor(combPred),as.factor(testing$diagnosis))$overall
# 
# rf  = 0.9146
# gmb = 0.9146
# lda = 0.9146
# mix = 0.9512
# 

# QUESTION 3

set.seed(3523)
library(AppliedPredictiveModeling)
data(concrete)
inTrain = createDataPartition(concrete$CompressiveStrength, p = 3/4)[[1]]
training = concrete[ inTrain,]
testing = concrete[-inTrain,]

set.seed(233)

install.packages("glmnet")
library(glmnet)

training$CompressiveStrength

lambdas <- 10^seq(2,-3,by=-.05)

lasso_reg <- glmnet(x=training$CompressiveStrength,,alpha=1,lambda=lambdas, standarize=TRUE,nfolds=5)



# QUESTION 4

library(lubridate) # For year() function below

dat = read.csv("E:/dev/portfolio/resources/analytics/data_science_specialization/practical_machine_learning/gaData.csv")

training = dat[year(dat$date) < 2012,]
testing = dat[(year(dat$date)) > 2011,]

# OBSOLETE LIBRARY. THEY NEED TO UPDATE THE COURSE

tstrain = ts(training$visitsTumblr)

library(forecast)
fit <- bats(tstrain)
forec <- forecast(fit,level=c(95))


plot(forec)
lines(testing,col="red")

ets1 <- ets(ts1Train,model="MMM")
fcast<-forecast(ets1)
plot(fcast)
lines(ts1Test,col="red")


# QUESTION 5

set.seed(3523)
library(AppliedPredictiveModeling)
data(concrete)
inTrain = createDataPartition(concrete$CompressiveStrength, p = 3/4)[[1]]
training = concrete[ inTrain,]
testing = concrete[-inTrain,]

library(e1071)
set.seed(325)
tr1 <- svm(CompressiveStrength~. ,data=training)
tr2 <- train(CompressiveStrength~.,data=training,method="svmRadial")
# PORQUE USA SVM RADIAL ????
pred <- predict(tr1,testing)
accuracy(pred,testing$CompressiveStrength)

# ME     RMSE      MAE       MPE     MAPE
#Test set 0.3113479 7.962075 5.515605 -6.845664 20.31935

# The course results are all obsolete They should update it.














