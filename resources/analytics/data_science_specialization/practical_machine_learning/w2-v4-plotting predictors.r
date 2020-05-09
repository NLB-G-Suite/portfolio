# plotting predictors


install.packages("ISLR")
library(ISLR) ; library(ggplot2) ; library(caret)
data("Wage")

summary(Wage)

inTrain <- createDataPartition(y=Wage$wage,p=0.7,list=FALSE)
training <- Wage[inTrain,]
testing <- Wage[-inTrain,]
dim(training);dim(testing)


featurePlot(x=training[,c("age","education","jobclass")],y=training$wage,plot="pairs")



qplot(age,wage,data=training)
qplot(age,education,data=training)
qplot(age,jobclass,data=training)
qplot(wage,education,data=training)

# qplot(education,jobclass,data=training)



qq<-qplot(age,wage,data=training,colour=education)
qq + geom_smooth(method="lm",formula=y~x)
qq<-qplot(age,wage,data=training,colour=jobclass)
qq + geom_smooth(method="lm",formula=y~x)

# qplot(age,education,data=training,colour=wage)
# qplot(age,education,data=training,colour=jobclass)

# qplot(age,jobclass,data=training,colour=wage)
# qplot(age,jobclass,data=training,colour=education)

# qq<-qplot(wage,education,data=training,colour=jobclass)
# qq + geom_smooth(method="lm",formula=y~x)
# qplot(wage,education,data=training,colour=age)

# qplot(wage,jobclass,data=training,colour=age)
# qq<-qplot(wage,jobclass,data=training,colour=education)
# qq + geom_smooth(method="lm",formula=y~x)

# qplot(education,jobclass,data=training,colour=age)
# qplot(education,jobclass,data=training,colour=wage)



