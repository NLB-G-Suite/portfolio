library(plyr)
library(tidyr)



# You should create one R script called run_analysis.R that does the following.
#

# =========================================================================
# 1 / Merges the training and the test sets to create one data set.
# =========================================================================
#       - what training data ?
#           - 'train/X_train.txt': Training set.
#           - 'train/y_train.txt': Training labels.
#       - what test sets data?
#           - 'test/X_test.txt': Test set.
#           - 'test/y_test.txt': Test labels.	
#       - how can we merge them?
#           - 'train/y_train.txt' and 'test/y_test.txt': labels. - numbers from 1 to 6 ??	
#           - both y and x_train have 7352 
#           - both y and x_test have 2947
#           * So we should be able to join x and y as columns from x_train, y_train, x_test, y_test into xmerged, ymerged

            x_train<-read.table("train/x_train.txt",header=FALSE)
            y_train<-read.table("train/y_train.txt",header=FALSE)
            x_test<-read.table("test/x_test.txt",header=FALSE)
            y_test<-read.table("test/y_test.txt",header=FALSE)
            xmerged<-rbind(x_train,x_test)
            ymerged<-rbind(y_train,y_test)

#       - Now we add the names of the columns (features)
            
            feature_names<-read.table("features.txt",header=FALSE)
            feature_names<-feature_names[,2]  # we only want the second column
            # we modify xmerged column names with the feature_names
            names(xmerged)<-feature_names
            
# =========================================================================
# 2 / Extracts only the measurements on the mean and standard deviation for each measurement.
# =========================================================================

            # We get the column names with "mean("  and with "std(" . We need to escape those chars
            only_mean_std<-grep("mean\\(|std\\(",names(xmerged))
            
            # we create a filtered_merge only with those columns
            filtered_merge <- xmerged[,only_mean_std]

# =========================================================================            
# 3 / Uses descriptive activity names to name the activities in the data set
# =========================================================================

            # Now seems this question refers to y data having numbers from 1 to 6
            
            # Where do we get the activity names? -> activity_labels.txt so we import them
            
            y_labels <- read.table("activity_labels.txt",header=FALSE)
            
            # so we need to replace the numbers with the activities. 
            
            # I transpose first the imported values from column to row
            t_y_labels<-t(y_labels)[2,]
            # Now we get them into activities
            Activity <- t_y_labels[ymerged$V1]
            

# =========================================================================
# 4 / Appropriately labels the data set with descriptive variable names.
# =========================================================================

            # First checking the labels we have:
            head(filtered_merge,n=1)
            # quite ugly indeed
            
            # Labeling changes convention is as follows:
            # . . . . . . . . . . . . . . . . . . . . . . 
            #     t -> Time                 -  at the beginning so i will use ^
            #     f -> Frequency            -  at the beginning so i will use ^
            #     mean -> Mean             
            #     std  -> StdDev           
            #
            
            names(filtered_merge)<-gsub("^t","Time",names(filtered_merge))
            names(filtered_merge)<-gsub("^f","Frequency",names(filtered_merge))
            names(filtered_merge)<-gsub("mean","Mean",names(filtered_merge))
            names(filtered_merge)<-gsub("std","StdDev",names(filtered_merge))
            
            # Other tidying:
            # . . . . . . . . 
            #     Removing those BodyBody repetitions and the "-" and the "()"
            
            # All these changes should be applied to the titles so names():

            names(filtered_merge)<-gsub("BodyBody","Body",names(filtered_merge))
            names(filtered_merge)<-gsub("-","",names(filtered_merge))
            names(filtered_merge)<-gsub("\\(","",names(filtered_merge))
            names(filtered_merge)<-gsub("\\)","",names(filtered_merge))
            

# =========================================================================            
# 5 / From the data set in step 4, creates a second, independent tidy data set 
# with the average of each variable for each activity and each subject.
# =========================================================================            
            
            # We need to load more data subject_test.txt & subject_train.txt probably
            # The files do not have headers
            
            subject_test=read.table("test/subject_test.txt", header=FALSE)
            subject_train=read.table("train/subject_train.txt", header=FALSE)
            
            # We bind both toghether in the same way as x and y data with the train first, test second
            Subject<-rbind(subject_train,subject_test)[,1]
            


            # Now we are going to create  "averages" with the required data
            # and also the different (and tidy) measures from the X table
            # I am not adding the third column name as they already have correct (and tidy) ones
            
            averages <- cbind(Subject,Activity,filtered_merge)
            
            # So now we should create a mean for each variable but there are many so we will use ddply
            
            mean_only_vars <-function(df)
            {
              return_this<-colMeans(df[,-c(1,2)])
              return_this
            }

            tidy<-ddply(averages,.(Subject,Activity),mean_only_vars)
            
            # Now we will add "Mean" in all those columns, again except 1 and 2. I will use regexpr here

            names(tidy)[-c(1,2)]<-gsub("^F","MeanF",names(tidy)[-c(1,2)])
            names(tidy)[-c(1,2)]<-gsub("^T","MeanT",names(tidy)[-c(1,2)])


# =========================================================================            
# 6 / Writing the tidy result to file
# =========================================================================            
            
            write.table(tidy,"tidyMeans.txt",row.names=FALSE)
            
            
            
            
            