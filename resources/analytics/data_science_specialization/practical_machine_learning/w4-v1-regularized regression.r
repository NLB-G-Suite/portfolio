# Regularized regression

Basic Idea

Fit a regression model
Penalize (or shrink) larger coefficients

Pros:
    
    Can help with bias/variance ratio
    Can help model selection
    

Cons:
    
    May be computationally intensive on large data sets
    Works worse than random forests / boosting
    
    
Example:
    
    Y = a + bx1 + cx2 + e
    
    Y = a + (b+c)x1 + e
    
    (when b & c are highly correlated)
    
    Results:
        
        Model will work fine
        Increased bias
        reduced variance
    

Practical example:
    
    Prostate cancer
    
    library(ElemStatLearn)
    data("prostate")
    str(prostate)
    
    inTrain <- createDataPartition(y=prostate$lcavol,p=0.7,list = F)
    training <- prostate[ inTrain,]
    testing  <- prostate[-inTrain,]
    dim(training);dim(testing)
    
    modFit <- train(lcavol ~. , data=training,method="rf")
    
    # getTree(modFit$finalModel)
    # names(training)
    # featurePlot(x=training[,2:10],y=training$lcavol,plot="pairs")
    # library(PerformanceAnalytics)
    # chart.Correlation(training)
    
small = prostate[1:5,]
lm(lpsa ~., data=small)
    
    
    