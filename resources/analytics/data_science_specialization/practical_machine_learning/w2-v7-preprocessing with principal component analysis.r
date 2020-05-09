#############################################################
### PREPROCESSING WITH PRINCIPAL COMPONENT ANALYSIS (PCA) ###
#############################################################


# Correlated predictors

library(caret)
library(kernlab)
data(spam)

inTrain <- createDataPartition(y=spam$type,p=0.75,list=FALSE)

training <- spam[ inTrain,]
testing  <- spam[-inTrain,]

# Which 

M <- abs(cor(training[,-58]))

diag(M) <- 0
which(M > 0.8, arr.ind=T)

big_corr <- as.data.frame(which(M > 0.8, arr.ind=T))
names(big_corr)

for (k in 1:nrow(big_corr))  print(paste(toString(names(spam)[c(big_corr$row[k],big_corr$col[k])])," , ",toString(big_corr[k,]),sep=""))



plot(spam[,34],spam[,32])


# BASIC Principal Component Analysis Idea

    # We might not need every covariant/predictor
    # A weighted combination of predictors might be better
    # We should pick this combination to capture the "most information" possible
    # Benefits : 
        # Reduced numbers of predictors
        # Reduced noise (due to averaging)



# WE CAN ROTATE THE PLOT

    # i.e :  X = 0.81 x num415 + 0.71 x num857
    #        Y = 0.81 x num415 - 0.71 x num857

x <- 0.71*training$num415 + 0.71*training$num857    
y <- 0.71*training$num415 - 0.71*training$num857
plot(x,y)

# What do we get from this ? That the most of the variability is happening in the x-axis. A lot of points spread in the X-axis but 0 on y-axis
# The idea is that we might want to use the sum of both variables as a predictor

# If we get this into a matrix we would get the lower matrix
# This is good at statistical and data compression levels



###################################
### Related Solutions - PCA/SVD ###
###################################


# SVD 'Matrix Decomposition'
############################


# PCA Substrace mean and divide by SD 
#####################################

# Principal Components in R - prcomp

smallSpam <- spam[,c(34,32)]
prComp <- prcomp(smallSpam)
plot(prComp$x[,1],prComp$x[,2])


prComp$rotation

# PCA on SPAM data

typeColor <- ((spam$type=="spam")*1 + 1)
prComp <- prcomp(log10(spam[,-58]+1))
plot(prComp$x[,1],prComp$x[,2],col=typeColor,xlab="PCI",ylab="PC2")


# Doing PCA with caret package

preProc <- preProcess(log10(spam[,-58]+1),method="pca",pcaComp=2)
spamPC <- predict(preProc,log10(spam[,-58]+1))
plot(spamPC[,1],spamPC[,2],col=typeColor)

## VERY IMPORTANT TO PAY ATTENTION TO OUTLIERS ON PCA AS THEY CAN BREAK THE ANALYSIS. 
## BOX-COX might be needed. Plot to avoid problems !. Might increase difficulty to interpret.



### Preprocessing with PCA





preProc <- preProcess(log10(training[,-58]+1),method="pca",pcaComp=2)
trainPC <- predict(preProc,log10(training[,-58]+1))


            # CUIDADO con sintaxis NO añadir el dataset$type, solo type. Versión???
modelFit <- train(type ~. , method="glm", data = trainPC)    


testPC <- predict(preProc,log10(testing[,-58]+1))

confusionMatrix(testing$type,predict(modelfit,testPC))


### Alternative (sets # of PCs)


            # CUIDADO con sintaxis NO añadir el dataset$type, solo type. Versión???

modelFit <- train(type ~. , method ="glm", preProcess = "pca", data = training)

confusionMatrix(testing$type,predict(modelFit,testing))









