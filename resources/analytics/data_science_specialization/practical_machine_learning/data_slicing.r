# We can use DAta Slicing to build training and testing sets at the beginning of the prediction 
# or to perform cross validation / boot strapping within training set to evaluate models.


library(caret)
library(kernlab)
data(spam)

# SLICING 75%, 25%

inTrain <- createDataPartition(y=spam$type, p=0.75,list=FALSE)

training <- spam[ inTrain,]
testing  <- spam[-inTrain,]

dim(training)

# CREATING FOLDS

set.seed(32323)
folds <- createFolds(y=spam$type,k=10,list=TRUE,returnTrain=TRUE)
sapply(folds,length)



folds[[1]][1:10]

# RESAMPLING

set.seed(32323)
folds <- createResample(y=spam$type,times=10,list=TRUE)
sapply(folds,length)

folds[[1]][1:10]

# CREATING TIME SLICES

set.seed(32323)
# time vector of 1 to 1000
tme <- 1:1000
# windows 20, predicting next 10
folds <- createTimeSlices(y=tme,initialWindow=20,horizon=10)
names(folds)

folds$train[[1]]

