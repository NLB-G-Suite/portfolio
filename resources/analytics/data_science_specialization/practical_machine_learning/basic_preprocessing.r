####################
# WHY PREPROCESS ??
####################

    library(caret); library(kernlab) ; data(spam)
    library(Hmisc); library(ggplot2)
    library(gridExtra)
    
    inTrain <- createDataPartition(y=spam$type, p=0.75, list=FALSE)
    
    training <- spam[inTrain,]
    testing <- spam[-inTrain,]
    
    head(training)
    
    p1 <- qplot(capitalAve,colour=type,data=training,geom="density")
    cut_capitalAve<- cut2(training$capitalAve,g=10)
    p2 <- qplot(cut_capitalAve,data=training,colour=type, geom=c("boxplot"))
    
    hist(training$capitalTotal,main="",xlab="ave, capital run length")
    
    mean(training$capitalAve)
    
    sd(training$capitalAve)

# STANDARIZING

    trainCapAve <- training$capitalAve
    trainCapAveS <- (trainCapAve - mean(trainCapAve))/sd(trainCapAve)
    
    mean(trainCapAveS)
    
    sd(trainCapAveS)

# STANDARIZING - preProcess function

    preObj <- preProcess(training[,-58],method=c("center","scale"))
    trainCapAveS <- predict(preObj, training[,-58])$capitalAve
    mean(trainCapAveS)
    sd(trainCapAveS)
    
    testCapAveS <- predict(preObj,testing[,-58])$capitalAve
    mean(testCapAveS)

# STANDARIZING - preProcess argument

    set.seed(32343)
    modelFit <- train(type ~. , data = training, preProcess = c("center","scale"),method="glm")
    modelFit

# STANDARIZING - BOX-COX TRANSFORMS

    preObj <- preProcess(training[,-58],method=c("BoxCox"))
    trainCapAveS <- predict(preObj,training[,-58])$capitalAve
    par(mfrow=c(1,2)) 
        hist(trainCapAveS)
        qqnorm(trainCapAveS)
    
    
# STANDARIZING - INPUTTING DATA
    
        set.seed(14343)    
    
    # Make some value NA
    
        training$capAve <- training$capitalAve
        selectNA <- rbinom(dim(training)[1],size=1,prob=0.05)==1
        training$capAve[selectNA] <- NA
    
    # Impute and Standarize ( removing the column 58 with the result) -> "type" )
    
        # Pre-processing transformation (centering, scaling etc.) can be estimated 
        # from the training data and applied to any data set with the same variables.
        
        # Similar to scale() 
        # install.packages("RANN")
        
        
    
        preObj <- preProcess(training[,-58],method="knnImpute")
        require(RANN)
        capAve <- predict(preObj,training[,-58])$capAve
        
    # Standarizing the values

        capAveTruth <- training$capitalAve
        capAveTruth <- (capAveTruth-mean(capAveTruth))/sd(capAveTruth)
        
        # A Z-Score ...
        


    
    
    
    



