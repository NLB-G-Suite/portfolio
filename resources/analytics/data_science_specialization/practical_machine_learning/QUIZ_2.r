##############
#            #
#   QUIZ 2   #
#            #
##############

# QUESTION 1.- Load the Alzheimer's disease data using the commands:'

    install.packages("AppliedPredictiveModeling")
    library(AppliedPredictiveModeling)
    data(AlzheimerDisease)

#   Which of the following commands will create non-overlapping training and 
#   test sets with about 50% of the observations assigned to each

    
# OPTION A
    
    adData = data.frame(diagnosis,predictors)
    trainIndex = createDataPartition(diagnosis, p = 0.50,list=FALSE)
    training = adData[trainIndex,]
    testing = adData[-trainIndex,]

    # Comment: CANNOT BECAUSE IT IS MISSING LIST = FALSE
    
# OPTION B
    
    adData = data.frame(predictors)
    trainIndex = createDataPartition(diagnosis,p=0.5,list=FALSE)
    training_B = adData[trainIndex,]
    testing_B = adData[-trainIndex,]

    # Comment: DUDANDO
    
# OPTION C

    adData = data.frame(diagnosis,predictors)
    train = createDataPartition(diagnosis, p = 0.50,list=FALSE)
    test = createDataPartition(diagnosis, p = 0.50,list=FALSE)
    
    dim(train)
    dim(test)

    # Comment: NO TIENE SENTIDO, SON IGUALES

# OPTION D

    adData = data.frame(diagnosis,predictors)
    trainIndex = createDataPartition(diagnosis, p = 0.50,list=FALSE)
    training_D = adData[trainIndex,]
    testing_D = adData[-trainIndex,]    
    
    # Comment: DUDANDO
    


# DUDANDO ENTRE LA B Y LA D    
    
    #The difference is that option D includes diagnosis
    
        #names(training_D)[!(names(training_D) %in% (names(training_B)))]

    # But if we are preparing both training and test, it shouldn't 
    # as I understand that test should include the solution.
    
    # I AM GOING TO CHOOSE B
    
# ----------------------------------------------
# ----------------------------------------------    
# ----------------------------------------------        

    
    
    
# QUESTION 2 -. Load the cement data using the commands:
    
    
    library(AppliedPredictiveModeling)
    data(concrete)
    library(caret)
    set.seed(1000)
    inTrain = createDataPartition(mixtures$CompressiveStrength, p = 3/4)[[1]]
    training = mixtures[ inTrain,]
    testing = mixtures[-inTrain,]   
    
#  Make a plot of the outcome (CompressiveStrength) versus the index 
#  of the samples. Color by each of the variables in the data set 
#  (you may find the cut2() function in the Hmisc package useful for 
#  turning continuous covariates into factors). 
    
    library(Hmisc)
    plot(mixtures$CompressiveStrength)    
    cut_FlyAsh<- cut2(mixtures$FlyAsh,g=10)
    names(mixtures)
    
    
    #[1] "Cement"              "BlastFurnaceSlag"    "FlyAsh"              "Water"               "Superplasticizer"    "CoarseAggregate"     "FineAggregate"      
    #[8] "Age"                 "CompressiveStrength"    
    
    #qq <- 
    qplot(FlyAsh,CompressiveStrength,data=mixtures,colour=cut_FlyAsh)
    
        El flyash no parece tener ninguna relación con la dureza. Incluso a cero la fuerza de compresión se mantiene
    
    qq<-qplot(Age, CompressiveStrength,data=mixtures,colour=Age)        
    qq + geom_smooth(method="lm",formula=y~x)
    
    
    
    
    library(PerformanceAnalytics)
    chart.Correlation(mixtures)

    
    
#  What do you notice in these plots?    
    
    # observaciones: The highest (negative) correlation is between Superplastizer AGAINST water 
    
    
    
        # a/ There is a non-random pattern in the plot of the outcome versus index that does not appear 
        #    to be perfectly explained by any predictor suggesting a variable may be missing.
            
                chart.Correlation(mixtures)
                
                ESO ES LO QUE PARECE, NO HAY NADA INTERESANTE PARA USAR
            
        # b/ There is a non-random pattern in the plot of the outcome versus index that is perfectly explained by the FlyAsh variable.
                par(mfrow=c(2,1))
                plot(mixtures$CompressiveStrength)            
                plot(mixtures$FlyAsh)
                
                cor(mixtures$CompressiveStrength,mixtures$FlyAsh)
                
                YO CREO QUE NO
    
            
        # c/ The outcome variable is highly correlated with FlyAsh.
            
                DEFINITIVAMENTE NO
            
        # d/ There is a non-random pattern in the plot of the outcome versus index that is perfectly 
        #    explained by the Age variable so there may be a variable missing.

                par(mfrow=c(2,1))
                plot(mixtures$CompressiveStrength)            
                plot(mixtures$Age)
                
                cor(mixtures$CompressiveStrength,mixtures$Age)
                
                PSE
    
    

        
# ----------------------------------------------
# ----------------------------------------------    
# ----------------------------------------------        
                
                

                
    # QUESTION 3 -. Load the cement data using the commands:
                
                library(AppliedPredictiveModeling)
                data(concrete)
                library(caret)
                set.seed(1000)
                inTrain = createDataPartition(mixtures$CompressiveStrength, p = 3/4)[[1]]
                training = mixtures[ inTrain,]
                testing = mixtures[-inTrain,]   
                

#        Make a histogram and confirm the SuperPlasticizer variable is skewed. Normally you might use the log transform 
#           to try to make the data more symmetric. Why would that be a poor choice for this variable?

            hist(mixtures$Superplasticizer)                    
            summary(mixtures$Superplasticizer)
            head(mixtures$Superplasticizer)
            
            ¿porqué tiene muchos valores 0 que serían inválidos ??
                    
#           a/ The SuperPlasticizer data include negative values so the log transform can not be performed.
            
                min(mixtures$Superplasticizer)
            
                NOT THE CASE
                
#           b/ There are a large number of values that are the same and even if you took the log(SuperPlasticizer + 1) they
#               would still all be identical so the distribution would not be symmetric.
                
                b.1/ Is there really a large number of equal values ?
                    
                        Lets see using an histogram without graph
                
                         hh<-hist(mixtures$Superplasticizer,plot=F)
                         par(mfrow=c(2,1))
                         plot(hh$breaks[1:14],hh$counts)
                         plot(hh$breaks[1:14],hh$density)
                    
                    
                    
 
                b.2/ COULD BE. Let s compare.               

                    Superplasticizer_A <- mixtures$Superplasticizer
                    Superplasticizer_log_A_plus_1 <- log(Superplasticizer_A+1)
                    
                    par(mfrow=c(2,1))
                    hist(Superplasticizer_A)            
                    hist(Superplasticizer_log_A_plus_1)
                    
                    THIS IS TRUE
                    
                I SAY THIS IS THE CORRECT ONE
                
                
#           c/ The log transform is not a monotone transformation of the data.
                
                I have never heard of monotone transformation??? Wikipedia neither
                
#           d/ The log transform does not reduce the skewness of the non-zero values of SuperPlasticizer
                
                COULD BE? . If we ignore all the 0 values the skewness would be similar probably
                
                mixtures$Superplasticizer_B <- mixtures$Superplasticizer
                
                for (k in 1:length(mixtures$Superplasticizer_B))
                {
                    if (mixtures$Superplasticizer_B[k] !=0 ) mixtures$Superplasticizer_B[k] = log10(mixtures$Superplasticizer_B[k])
                }
                    
                par(mfrow=c(2,1))
                hist(mixtures$Superplasticizer)            
                hist(mixtures$Superplasticizer_B)
                
                Well it changes, it shifts values from positive to negative, but ignoring the zeros ??        
                
                let's see if we can create a copy of Superplasticizer and calculate quantitatively the skewness & kurtosis
                
                NZ_Superplasticizer_A <- mixtures$Superplasticizer[mixtures$Superplasticizer!=0]
                NZ_Superplasticizer_B <- mixtures$Superplasticizer_B[mixtures$Superplasticizer_B!=0]
                
                Let's replot

                par(mfrow=c(2,1))
                hist(NZ_Superplasticizer_A)            
                hist(NZ_Superplasticizer_B)
                
                
                install.packages("moments")
                library(moments)
                
                kurtosis(NZ_Superplasticizer_A)
                kurtosis(NZ_Superplasticizer_B)
                
                skewness(NZ_Superplasticizer_A)
                skewness(NZ_Superplasticizer_B)
                
                Well, it certainly changes, although it is because the data is not centered.                
                
                
                
                
                
# ----------------------------------------------
# ----------------------------------------------    
# ----------------------------------------------        
                
                
                
                
    # QUESTION 4 -. Load the Alzheimer's disease data using the commands:
                
                library(caret)
                library(AppliedPredictiveModeling)
                set.seed(3433)
                data(AlzheimerDisease)
                adData = data.frame(diagnosis,predictors)
                inTrain = createDataPartition(adData$diagnosis, p = 3/4)[[1]]
                training = adData[ inTrain,]
                testing = adData[-inTrain,]   
                
                
#                Find all the predictor variables in the training set that begin with IL. Perform principal components on these variables 
#                    with the preProcess() function from the caret package. Calculate the number of principal components needed to 
#                    capture 90% of the variance. How many are there?
                

                library(base)
                require(caret)
                
                names_with_IL <- names(predictors)[substr(names(predictors),1,2)=="IL"]
                predictors_IL <- predictors[,names(predictors) %in% names_with_IL]


                pca <- prcomp(predictors_IL,scale=TRUE)
                summary(pca)

                > pca <- prcomp(predictors_IL,scale=TRUE)
                > summary(pca)
                Importance of components:
                                         PC1    PC2     PC3     PC4     PC5     PC6     PC7     PC8     PC9    PC10    PC11   PC12
                Standard deviation     2.0661 1.1730 1.05178 1.01226 0.88322 0.85748 0.80706 0.76961 0.71490 0.64823 0.56518 0.4634
                Proportion of Variance 0.3557 0.1147 0.09219 0.08539 0.06501 0.06127 0.05428 0.04936 0.04259 0.03502 0.02662 0.0179
                Cumulative Proportion  0.3557 0.4704 0.56257 0.64796 0.71297 0.77424 0.82852 0.87788 [0.92047] 0.95549 0.98210 1.0000                
                
                
                #Parece que era muchisimo mas facil de lo que yo estaba haciendo                
                
                Entiendo que con 9 componentes vale para explicar una varianza de 0.90 (90%)
                

                
                
    
# ----------------------------------------------
# ----------------------------------------------    
# ----------------------------------------------        
                
                
                
                
    # QUESTION 5 -. Load the Alzheimer's disease data using the commands:
    
    
    
                library(caret)
                library(AppliedPredictiveModeling)
                set.seed(3433)data(AlzheimerDisease)
                adData = data.frame(diagnosis,predictors)
                inTrain = createDataPartition(adData$diagnosis, p = 3/4)[[1]]training = adData[ inTrain,]
                testing = adData[-inTrain,]    
    
    
    
                # Create a training data set consisting of only the predictors with variable names beginning with IL and the diagnosis. 
                
                    names_with_IL <- names(predictors)[substr(names(predictors),1,2)=="IL"]
                    predictors_IL <- predictors[,names(predictors) %in% names_with_IL]
                    df <- data.frame(predictors_IL,diagnosis)
                
                
                # Build two predictive models, one using the predictors as they are and one using PCA with principal components 
                # explaining 80% of the variance in the predictors. Use method="glm" in the train function.
                # 
                
                
                trainIndex = createDataPartition(diagnosis, p = 0.75,list=FALSE)
                training = df[trainIndex,]
                testing = df[-trainIndex,]
                
                pca <- prcomp(df,scale=TRUE)
                summary(pca)
                
                # Importance of components:
                #                          PC1    PC2     PC3     PC4     PC5     PC6     PC7     PC8     PC9    PC10    PC11   PC12
                # Standard deviation     2.0661 1.1730 1.05178 1.01226 0.88322 0.85748 0.80706 0.76961 0.71490 0.64823 0.56518 0.4634
                # Proportion of Variance 0.3557 0.1147 0.09219 0.08539 0.06501 0.06127 0.05428 0.04936 0.04259 0.03502 0.02662 0.0179
                # Cumulative Proportion  0.3557 0.4704 0.56257 0.64796 0.71297 0.77424 0.82852 0.87788 0.92047 0.95549 0.98210 1.0000
                
                # Necesitamos un PCA con 7 columnas para obtener una varianza de 80%
                
                preProc <- preProcess(training[,-13],method="pca",pcaComp=7)
                trainPC <- predict(preProc,training[,-13])
                modelFit <- train(diagnosis ~ . , method = "glm", data=trainPC)

                
                
                # What is the accuracy of each method in the test set? Which is more accurate?
                #     
                # A/    
                # Non-PCA Accuracy: 0.74
                # 
                # PCA Accuracy: 0.74
                # 
                # B/
                # Non-PCA Accuracy: 0.65
                # 
                # PCA Accuracy: 0.72
                # 
                # C/
                # Non-PCA Accuracy: 0.72
                # 
                # PCA Accuracy: 0.71
                # 
                # D/
                # Non-PCA Accuracy: 0.72
                # 
                # PCA Accuracy: 0.65
                
                
    
                library(caret)
                library(AppliedPredictiveModeling)
                
                set.seed(3433)
                data(AlzheimerDisease)
                adData = data.frame(diagnosis,predictors)
                inTrain = createDataPartition(adData$diagnosis, p = 3/4)[[1]]
                training = adData[ inTrain,]
                testing = adData[-inTrain,]
                # get the data with column names started with IL
                New_training <- data.frame(training[,grep('^IL',names(training))],training$diagnosis)
                New_testing <- data.frame(testing[,grep('^IL',names(testing))],testing$diagnosis)
                
                # non-PCA
                NotPCFit <- train(training.diagnosis ~.,data = New_training, method="glm")
                NotPCTestPredict <- predict(NotPCFit, New_testing[, -13])
                confusionMatrix(New_testing$testing.diagnosis, NotPCTestPredict)
                
                # PCA
                preProc <- preProcess(New_training[, -13],method="pca",thresh=.8)
                trainPC <- predict(preProc, New_training[, -13])
                testPC <- predict(preProc, New_testing[, -13])
                # add the diagnosis into the trainPC data
                trainPC <- data.frame(trainPC, training$diagnosis)
                
                PCFit <- train(training.diagnosis ~.,data= trainPC, method="glm")
                PCTestPredict <- predict(PCFit, testPC)
                confusionMatrix(New_testing$testing.diagnosis, PCTestPredict)
    
    
    
    IMPORTANT NOTE: 
        
        THE QUIZ IS WRONG -> Course Forum Correction
        
        https://www.coursera.org/learn/practical-machine-learning/discussions/weeks/2/threads/IUK7h6a6EemQZwoo6Wjp0A
    
    
    
    
        
    
    
    
    
    
    
    
    
    
    