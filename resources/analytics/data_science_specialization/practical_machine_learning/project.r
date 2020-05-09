# PROJECT : Practical Machine Learning
# 
# Background
# 
# Using devices such as Jawbone Up, Nike FuelBand, and Fitbit it is 
# now possible to collect a large amount of data about personal 
# activity relatively inexpensively. These type of devices are part 
# of the quantified self movement – a group of enthusiasts who take 
# measurements about themselves regularly to improve their health, 
# to find patterns in their behavior, or because they are tech geeks. 
# One thing that people regularly do is quantify how much of a 
# particular activity they do, but they rarely quantify how well they 
# do it. In this project, your goal will be to use data from 
# accelerometers on the belt, forearm, arm, and dumbell of 6 
# participants. They were asked to perform barbell lifts correctly 
# and incorrectly in 5 different ways. More information is available 
# from the website here: http://groupware.les.inf.puc-rio.br/har 
# (see the section on the Weight Lifting Exercise Dataset).
# 
# Data
# 
# The training data for this project are available here:
#     
#     https://d396qusza40orc.cloudfront.net/predmachlearn/pml-training.csv
# 
# The test data are available here:
#     
#     https://d396qusza40orc.cloudfront.net/predmachlearn/pml-testing.csv
# 
# The data for this project come from this source: 
#     
#     http://groupware.les.inf.puc-rio.br/har. 
# 
# If you use the document you create for this class for any purpose 
# please cite them as they have been very generous in allowing their 
# data to be used for this kind of assignment.
# 
# What you should submit
#
# The goal of your project is to predict the manner in which they 
# did the exercise. This is the "classe" variable in the training set. 
# You may use any of the other variables to predict with. You should 
# create a report describing how you built your model, how you used 
# cross validation, what you think the expected out of sample error is, 
# and why you made the choices you did. You will also use your 
# prediction model to predict 20 different test cases.
# 
# Peer Review Portion
# 
# Your submission for the Peer Review portion should consist of a 
# link to a Github repo with your R markdown and compiled HTML file 
# describing your analysis. Please constrain the text of the writeup 
# to < 2000 words and the number of figures to be less than 5. It 
# will make it easier for the graders if you submit a repo with a 
# gh-pages branch so the HTML page can be viewed online (and you 
#  always want to make it easy on graders :-).
# 
# Course Project Prediction Quiz Portion
# 
# Apply your machine learning algorithm to the 20 test cases available 
# in the test data above and submit your predictions in appropriate 
# format to the Course Project Prediction Quiz for automated grading.
# 
# Reproducibility
# 
# Due to security concerns with the exchange of R code, your code 
# will not be run during the evaluation by your classmates. Please 
# be sure that if they download the repo, they will be able to view 
# the compiled HTML version of your analysis.

# ------------------------------------------------------

# Introduction

# The general idea seems to be able to predict the manner in which they 
# did the exercise.

# My approach will be to run 10 different models with different methodologies
# over the classe result column and lately create an hypermodel that optimizes
# those 10 models combining their predictions

# Data loading. 

# Getting the training & testing csv data

require(scales)
require(sqldf)
require(mice)
require(VIM)
require(caret)

clean_df <- function(df, max_pct_rate_NAs_to_keep_column = 100,verbose = 0, max_imputation_iterations=10)
{
    base_log <- paste("clean_df > ",sep="")
    df2 <- data.frame(stringsAsFactors = FALSE)
    ini_cols = dim(df)[2]
    max_numNA = 0
    str0="[Step 1] "
    for (q in 1:dim(df)[2])
    {
        column = names(df)[q]
        if (verbose>1) str1=paste("Col ",q," of ",dim(df)[2]," : ",column,sep="") else str1=""
        col <- df[,which(colnames(df) == column)]
        if (is.factor(col)) 
        {
            if (verbose>1) print(paste(base_log,str0,str1," - Converting column to numeric",sep=""))
            col <- as.numeric(df[,which(colnames(df) == column)])
        }
        count_pre_DIV0=length(col[col=="#DIV/0!"])
        if (count_pre_DIV0 > 0) 
        {
            if (verbose>1) print(paste(base_log,str0,str1," - Converting ",count_pre_DIV0," rows with #DIV/0! to ",NA,sep=""))
            col[col=="#DIV/0!"] <- NA
        }
        if (dim(df2)[2]>0)
        {
            df2 <- as.data.frame(cbind(df2, col))
        } else {
            df2 <- as.data.frame(col)
        }
        names(df2)[dim(df2)[2]] <- names(df)[q] 
    }
    num_NAs <- nrow(check_NA(df2))
    if (num_NAs > 0)
    {
        str0="[Step 2] "
        if (verbose>1) print(paste(base_log,str0,"Trying to impute data on ",num_NAs," columns with NA values",sep=""))
        mice_df <- mice(df2,m=50,maxit=max_imputation_iterations,method="cart",seed=500,printFlag=FALSE)
        df2 <- complete(mice_df,1)
    }
    if (nrow(check_NA(df2)) > 0)
    {
        str0="[Step 3] "
        pct_rate_NAs_by_column <- round(colSums(is.na(df2))/dim(df2)[1]*100,0)
        cols_With_Excessive_Percent_Of_NAs <- names(df3[, pct_rate_NAs_by_column > max_pct_rate_NAs_to_keep_column])
        if (length(cols_With_Excessive_Percent_Of_NAs) > 0 )
        {
            print(paste(base_log,str0,"We have ",length(cols_With_Excessive_Percent_Of_NAs)," columns with an Excessive Percent of rows as NAs (max % defined:",max_pct_rate_NAs_to_keep_column,") ",sep=""))
            print(paste(base_log,str0,"Removing following columns ",toString(cols_With_Excessive_Percent_Of_NAs),sep=""))
        }
        df2 <- df2[, !(names(df2) %in% cols_With_Excessive_Percent_Of_NAs)]
    }
    str0="[Step 4] "
    end_cols = dim(df2)[2]
    print(paste(base_log,str0,"Discarded ",max(0,ini_cols-end_cols)," columns from the initial ",ini_cols," in the cleaning process.",sep=""))
    return(df2)
}

list_Highly_Correlated <- function(df,max_correlation_preserved=0.90)
{
    ex_cor_df <- data.frame(col1=character(),col2=character(),corr=numeric(),other=character(),stringsAsFactors = FALSE)
    cont=0
    for (j in 1:(dim(df)[2]-1))
    {
        col1_name = names(df)[j]
        col1_data = df[,j]
        for (k in 1:(dim(df)[2]-1))
        {
            col2_name = names(df)[k]
            if (j!=k & !col2_name %in% ex_cor_df[,1])
            {
                col2_data = df[,k]
                corr=cor(col1_data,col2_data,use="complete.obs")            
                if (is.na(corr))
                {   cont=cont+1
                print(paste(cont," > Correlation of ",col1_name," [",j,"] with ",col2_name," [",k,"] is NA. Needs Review.",sep=""))
                ex_cor_df[cont,1]=col1_name
                ex_cor_df[cont,2]=col2_name
                ex_cor_df[cont,4]="NOT OK"
                } else { 
                    if (abs(corr) > max_correlation_preserved)
                    {
                        cont=cont+1
                        print(paste(cont," > Correlation of ",col1_name," [",j,"] with ",col2_name," [",k,"] is ",round(corr,2),sep=""))
                        ex_cor_df[cont,1]=col1_name
                        ex_cor_df[cont,2]=col2_name
                        ex_cor_df[cont,3]=round(corr,2)
                        ex_cor_df[cont,4]="OK"
                    }
                }
            }
        }
    }
    df_HC <- as.list(sqldf("select distinct(col1) as Highly_Correlated from ex_cor_df where corr>0 and other='OK'"))
    return(df_HC)
}
df <- testing
df_name <- "testing"

plot_histogram_pattern_missing_data <- function(df, df_name,num_slices=1,slice_num=1,plot=T)
{
    require(sqldf)
    k <- slice_num-1
    num_ini_cols=dim(df)[2]
    data <- df[,(num_ini_cols*k/num_slices):(num_ini_cols*(1+k)/num_slices)]
    aggr_plot <- aggr(data, col=c('navyblue','red'), numbers=TRUE, sortVars=TRUE, plot=plot,
        labels=names(data), cex.axis=.7, gap=3, ylab=c("Histogram of missing data","Pattern"))$missings
    t1 <- sqldf(paste("select '",df_name,"' as Data_Set,count(Count) as Number_of_Columns,Count as Number_of_Missing_Rows from aggr_plot group by Count",sep=""))
    tab <- cbind(t1,nrow(df),round(t1$Number_of_Missing_Rows/nrow(df)*100,2),round(t1$Number_of_Columns/dim(df)[2]*100,2))
    names(tab)<-c("DataSet","Num_Cols","Num_Missing_Rows","Total_Rows_in_DataSet","%_Missing_Rows_in_DataSet","%_Cols_by_Range_with_Missing_Rows")
    return(tab)
}

check_NA <- function(df)
{
    t1 <- data.frame(num_NA=colSums(is.na(df))[colSums(is.na(df))>0])
    names(t1) <- c("num_NAs")
    return(t1)
}

Nth_delete<-function(dataframe,n,verbose=0) 
{
    ini_rows=dim(dataframe)[1]
    dataframe <- dataframe[-(seq(n,to=nrow(dataframe),by=n)),]
    end_rows=dim(dataframe)[1]
    if (verbose>0) print(paste("Nth_delete > [verbosity:",verbose,"] Subsampling data evenly removing 1 of each ",n,
        " rows. From initial ",ini_rows," to ",end_rows,sep=""))
    return(dataframe)
}

# DOWNLOADING THE DATA

    training_url <- "https://d396qusza40orc.cloudfront.net/predmachlearn/pml-training.csv"
    testing_url <- "https://d396qusza40orc.cloudfront.net/predmachlearn/pml-testing.csv"
    training <- read.csv(training_url)
    testing <- read.csv(testing_url)
    
    # Creating a copy of the data to avoid redownloading the data and overloading server.
    
    copy_training <- training
    copy_testing <- testing
    
    # In case I need to start again.
    
    training <- copy_training
    testing  <- copy_testing

# DATA PROCESSING
    
    writeLines(paste("Training set dimension : ",toString(dim(training)),"\n",
          "Testing  set dimension : ",toString(dim(testing)),sep=""))

    # The volume of data in the training set could be overwhelming depending on computer speed availability
    
    # We could evenly subsample 1 in each 2 rows and reduce the data when we have too much and not enough computer power.
    # I leave it as a tool that could be useful.
    
    training <- Nth_delete(training,2,verbose=1)

    # We can see that the columns on testing and training are not the same.
    
    writeLines(paste("Columns on training not included on testing  : ",
        toString(names(training)[!(names(training) %in% names(testing))]),
        "\nColumns on testing  not included on training : ",
        toString(names(testing)[!(names(testing) %in% names(training))]),sep=""))
    

    # Let's plot the missing values in the whole dataset to see how this looks
    # We will remove the uncommon columns with the classe result set and the problem id 
    # (displaying training and testing together for a full picture)

    missing_together <- plot_histogram_pattern_missing_data(rbind(training[,1:(dim(training)[2]-1)],testing[,1:(dim(testing)[2]-1)]),"all_together",num_slices=1,plot=T)
    missing_training <- plot_histogram_pattern_missing_data(training,"training",num_slices=1,plot=F)
    missing_testing  <- plot_histogram_pattern_missing_data(testing,"testing",num_slices=1,plot=F)
    rbind(missing_together,missing_training,missing_testing)

    # The plot is displaying both training and testing together to get a full picture (with the classe resultset and the problem_id removed as they are uncommon and not needed here)    
    
    # What can we see in this plot and this table
    # It seems testing has some columns that are missing all the data for every row. We won't be needing those. [100 columns with everything missing]
    
    testing_all_NA <- rownames(check_NA(testing))
    testing  <- testing[,!(names(testing) %in% testing_all_NA)]
    print(paste("Removed every column (",length(testing_all_NA),") in testing set that had every single row missing. Remaining number of columns now : ",dim(testing)[2],sep=""))

    # We will be removing the same columns from training set as they are not needed either. The idea I get from this approach is that if we cannot infer anything on testing set
    # because they are missing all the data, the model obtained should not be using columns as data source that we won't be able to test.
    
    training <- training[,!(names(training) %in% testing_all_NA)]
    print(paste("Removed every column (",length(testing_all_NA),") in training set that had every single row missing on testing. Remaining number of columns now : ",dim(training)[2],sep=""))
    
    # What do we have now ?

    missing_together <- plot_histogram_pattern_missing_data(rbind(training[,1:(dim(training)[2]-1)],testing[,1:(dim(testing)[2]-1)]),"all_together",num_slices=1,plot=T)

    # Seems we have cleaned most of the missing values although the data shows some problematics. 
    
    str(rbind(training[,1:(dim(training)[2]-1)],testing[,1:(dim(testing)[2]-1)]))
    
    # It has some category type of columns that could be converted to numeric categories,
    # also it has factors that could bring some problems and some DIV0 data.    

    # In order to apply the same transformations I will create a copy of the training and testing data sets

    full <- rbind(training[,1:(dim(training)[2]-1)],testing[,1:(dim(testing)[2]-1)])
    writeLines(paste(
          "Training data set dimension : ",toString(dim(training)),
        "\nTesting  data set dimension : ",toString(dim(testing)),
        "\nFull     data set dimension : ",toString(dim(full)),sep=""))
    

    # I will be doing some preprocessing of the data, consisting in the following steps
    
    #   + Converting to numeric when needed. Categoric columns included.
    #   + Processing DIV0s like NAs
    #   + Trying to impute the NA values with a number of iterations using method 'cart'
    #   + Discard those columns whose % of missing rows is above the specified value
    
    full <- clean_df(df=full,max_pct_rate_NAs_to_keep_column = 50,verbose = 3, max_imputation_iterations=10)

    # Let's see the results
    
    missing_training <- plot_histogram_pattern_missing_data(training,"training",num_slices=1,plot=F)
    missing_testing  <- plot_histogram_pattern_missing_data(testing,"testing",num_slices=1,plot=F)
    missing_full     <- plot_histogram_pattern_missing_data(full,"full",num_slices=1,plot=T)
    
    rbind(missing_full,missing_training,missing_testing)
    
    # Let's create a list of the distinct correlations above 0.90 as I will
    # be removing those.
    
    HC <- list_Highly_Correlated(df=full,max_correlation_preserved=0.90)
    full <- full[,!(names(full) %in% as.list(HC))]
    
    # Finally I will be scaling and recentering the data
    
    full <- scale(full, center=TRUE, scale=TRUE)
    
    
# Spliting into Training and Testing and adding back "classe" and "problem id"
    
    training <- as.data.frame(full[1:dim(training)[1],])
    testing  <- as.data.frame(full[(dim(training)[1]+1):(dim(training)[1]+dim(testing)[1]),])
    
    training$classe <- Nth_delete(copy_training,2)$classe
    testing$problem_id <- copy_testing$problem_id
    
    dim(training);dim(testing)
    

# Creating 10 different models on training
    
    saveRDS(training,"training.rds")
    saveRDS(testing,"testing.rds")
    saveRDS(full,"full.rds")

mod01 <- train(classe ~., data=training,method ="gbm"      , na.action=na.omit ,verbose=F);saveRDS(mod01,"mod01")
mod02 <- train(classe ~., data=training,method ="rf"       , na.action=na.omit ,verbose=F);saveRDS(mod02,"mod02")
mod05 <- train(classe ~., data=training,method="lda"       , na.action=na.omit ,verbose=F);saveRDS(mod05,"mod05")
mod06 <- train(classe ~., data=training,method="treebag"   , na.action=na.omit ,verbose=F);saveRDS(mod06,"mod06")
mod21 <- train(classe ~., data=training,method="LogitBoost", na.action=na.omit ,verbose=F);saveRDS(mod21,"mod21")

pre01 <- predict(mod01,testing)
pre02 <- predict(mod02,testing)
pre03 <- predict(mod05,testing)
pre04 <- predict(mod06,testing)
pre05 <- predict(mod21,testing)

qplot(cbind(pre01,pre02,pre03,pre04,pre05),colour=classe,data=testing)




