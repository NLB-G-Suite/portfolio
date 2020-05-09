# Unsupervised Prediction

# To build a predictor:

#   - Create clusters
#   - Name Clusters
#   - Build predictor for clusters

# In a new data set

#   - Predict clusters



data(iris); library(ggplot2)

inTrain <- createDataPartition(y=iris$Species,p=0.7,list=F)

training <- iris[ inTrain,]
testing  <- iris[-inTrain,]

dim(training);dim(testing)



KMeans1 <- kmeans(subset(training,select=-c(Species)),centers=3)
training$clusters <- as.factor(KMeans1$cluster)
qplot(Petal.Width,Petal.Length,colour=clusters,data=training)


table(KMeans1$cluster,training$Species)