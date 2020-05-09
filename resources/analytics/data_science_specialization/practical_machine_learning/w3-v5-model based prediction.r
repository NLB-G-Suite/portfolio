# Model Based Prediction

# Basic Idea:

# 1.- Assume the data follow a probabilistic model
# 2.- Use Bayer' theorem to identify optimal classifiers

# PROs:

# + Can take advantage of structure of the data
# + May be computational convenient
# + Are reasonably accurate on real problems

# CONs:

# + Make additional assumptions about the data:
# + When the model is incorrect you may get reduced accuracy



# LINEAR DISCRIMINANT ANALYSIS




# QUADRATIC DISCRIMINANT ANALYSIS


# MODEL BASED PREDICTION

# taking the log of the ratio of probabilitie 1 /  probabilities 2
# we fit a line between each gaussian distributions equivalence
# line betw G1 & G2, line betw G2 % G3 etc


# NAIVES BAYES 

# good for categorical classifications


data(iris); library(ggplot2)
names(iris)

table(iris$Species)

inTrain <- createDataPartition(y=iris$Sepal.Length,p=0.7,list=F)
training <- iris[ inTrain,]
testing <- iris[ -inTrain,]

dim(training);dim(testing)

# Building the predictions:

modlda <- train(Species ~., data =training, methods="lda")
modnb <- train(Species ~., data =training, methods="nb")
plda <- predict(modlda,testing);pnb =predict(modnb,testing)

table (plda, pnb)

# Comparison of results


equalPredictions = (plda == pnb)

qplot(Petal.Width,Sepal.Width, colour=equalPredictions,data=testing)



















