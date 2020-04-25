install.packages("caret")
install.packages("kernlab")
library(caret)
library(kernlab)

# Spam E-mail Database 
# 4601 observations and 58 variables
dim(spam)
library(sqldf)
sqldf("select type, count(type) as count_type from spam group by type")

#                                             75%
inTrain <- createDataPartition(y=spam$type,p=0.75,list=FALSE)
training <- spam[inTrain,]
testing <- spam[-inTrain,]
dim(training)
dim(testing)
dim(inTrain)
head(spam)
names(training)

set.seed(32343)
# PREDICTING TYPE                    ~. USE ALL THE OTHER VARIABLES
modelFit <- train(type ~. , data=training , method="glm")
modelFit

names(modelFit)

modelFit$finalModel

# Now we try the testing data

predictions <- predict(modelFit,newdata=testing)

confusionMatrix(predictions,testing$type)