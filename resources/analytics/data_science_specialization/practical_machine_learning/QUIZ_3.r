# QUIZ 3

# For this quiz we will be using several R packages. R package versions 
# change over time, the right answers have been checked using the following 
# versions of the packages.
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
# If you aren't using these versions of the packages, your answers may not 
# exactly match the right answer, but hopefully should be close.
# 
# Load the cell segmentation data from the AppliedPredictiveModeling package 
# using the commands:


library(AppliedPredictiveModeling)
data("segmentationOriginal")
library(caret)

require(devtools)
install_version("AppliedPredictiveModeling")
install_version("caret",version="6.0.47")
install_version("ElemStatLearn",version="201.04-0")
install_version("pgmm",version="1.1")
install_version("rpart",version="4.1.8")


----------------------------------------------------------
Q1- Subset the data to a training set and testing set based on the Case 
variable in the data set


#inTrain <- createDataPartition(y=segmentationOriginal$Case,p=0.7,list=F)
training <- segmentationOriginal[ segmentationOriginal$Case=="Train",]
testing <- segmentationOriginal[ segmentationOriginal$Case=="Test",]


2.- Set the seed to 125 and fit a CART model to predict Class with rpart
method using all predictor variables and default caret settings

set.seed(125)
modFit <- train(Class ~. , method="rpart",data=training)


3.- In the final model what would be the final model prediction for cases
with the following variable values:
    
plot(modFit$finalModel,uniform=TRUE,main="Classification Tree")
text(modFit$finalModel,use.n=TRUE,all=TRUE,cex=.8)


Con librerias diferentes y posibles datos cambiantes no estoy seguro


    
    
a. TotalIntench2 = 23,000; FiberWidthCh1 = 10; PerimStatusCh1=2

    PS porque 2)

b. TotalIntench2 = 50,000; FiberWidthCh1 = 10; VarIntenCh4 = 100

    WS porque 7)

c. TotalIntench2 = 57,000; FiberWidthCh1 = 8 ; VarIntenCh4 = 100

    PS

d. FiberWidthCh1 = 8     ; VarIntenCh4 = 100 ; PerimStatusCh1=2



DUDANDO ENTRE el 2 y el 3. No sé si se puede predecir el último sin datos
sobre TotalIntenCh2.
Veamos. Debería ser PS porque FiberWidthCh1 =8 pero no tengo esa
opción debe ser por las librerias actualizadas ....

Voy a probar con Not Possible to Predict


TIP: Plot the resulting tree and to use the plot to answer this question.

----------------------------------------------------------
Q2 - If K is small in a K-fold cross validation is the bias in the 
estimate of out-of-sample (test set) accuracy smaller or bigger? 
If K is small is the variance in the estimate of out-of-sample 
(test set) accuracy smaller or bigger. Is K large or small in 
leave one out cross validation?
    
    
The bias is smaller and the variance is bigger. Under leave one out cross validation K is equal to one.


The bias is smaller and the variance is smaller. Under leave one out cross validation K is equal to the sample size.


The bias is larger and the variance is smaller. Under leave one out cross validation K is equal to the sample size.


The bias is larger and the variance is smaller. Under leave one out cross validation K is equal to one.



----------------------------------------------------------
Q3 - 
    
    
library(pgmm)
data(olive)
olive=olive[,-1]

inTrain <- createDataPartition(y=olive$Area,p=0.7,list=F)

training <- olive[ inTrain,]
testing <- olive[ -inTrain,]


newdata = as.data.frame(t(colMeans(olive)))
modFit <- train(Area ~. , method="rpart",data=olive)
predict(modFit,newdata)


Respuesta 4.59965


----------------------------------------------------------
Q4 -
    
library(ElemStatLearn)
data(SAheart)
set.seed(8484)
train = sample(1:dim(SAheart)[1],size=dim(SAheart)[1]/2,replace=F)
trainSA = SAheart[train,]
testSA = SAheart[-train,]    
set.seed(13234)
#modFit <- train(Area ~. , method="glm",data=training)
modFit <- glm(chd ~ age + alcohol + obesity + tobacco + typea + ldl,binomial,data=trainSA)

summary(modFit)

qplot(predict(modFit,testSA),data=testSA)

modFit$

coef(modFit)

missClass()

lapply(list(testSA, trainSA), function(set) {missClass(set$chd, predict(modFit, set))} )

    0.33
    0.31
    
----------------------------------------------------------
Q5 -
   
        
    library(ElemStatLearn)
    data(vowel.train)
    data(vowel.test)             
        
set.seed(33833)

modFit <- randomForest(y ~.,data=vowel.train)
1,2,3
modFit <- train(y ~.,data=vowel.train,method="rf")

2,1,5,6,8

varImp(modFit)



