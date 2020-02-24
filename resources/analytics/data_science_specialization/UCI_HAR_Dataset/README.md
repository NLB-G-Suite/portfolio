README.md

[ Related to the script run_analysis.R and its function ]

#Tidy Data from the Human Activity Recognition Using Smartphones Dataset

run_analysis gets information from various text files and reorganizes them in a tidy format in an output file "tidyMeans.txt"



##Description of the output file tidyMeans.txt

Contains a table with the following columns:

Subject , Activity , (1) [ a list with the Mean values for a list of measurements ] 

Where (1) List of columns with the following structure:

Mean{Time or Frequency}{Specific Measurement}{Mean or StdDev}{XY or Z}

Examples:

	- MeanTimeBodyAccStdDevZ
	- MeanTimeGravityAccMeanX
	- MeanTimeGravityAccMeanY
	- MeanTimeGravityAccMeanZ
	- MeanTimeGravityAccStdDevX
	- MeanTimeBodyAccJerkMeanY
	- MeanTimeBodyAccJerkMeanZ
	- MeanTimeBodyAccJerkStdDevX
	- MeanTimeBodyGyroMeanY
	- MeanTimeBodyGyroMeanZ
	- MeanTimeBodyGyroStdDevX

The Subject is an identifier with the number of test subject
The Activity is one in six possible Activity States being measured. i.e:

	- WALKING
	- WALKING UPSTAIRS
	- WALKING DOWNSTAIRS
	- SITTING
	- STANDING
	- LAYING
	
NOTICE: This data presentation has been done according to the "wide format specification" from Wickham http://vita.had.co.nz/papers/tidy-data.pdf
	- Single row for each subject/activity pair
	- Single Column for each measurement

##More details about the project:

The experiments have been carried out with a group of 30 volunteers within an age bracket of 19-48 years. Each person performed six activities (WALKING, WALKING_UPSTAIRS, WALKING_DOWNSTAIRS, SITTING, STANDING, LAYING) wearing a smartphone (Samsung Galaxy S II) on the waist. Using its embedded accelerometer and gyroscope, we captured 3-axial linear acceleration and 3-axial angular velocity at a constant rate of 50Hz. The experiments have been video-recorded to label the data manually. The obtained dataset has been randomly partitioned into two sets, where 70% of the volunteers was selected for generating the training data and 30% the test data. 

The sensor signals (accelerometer and gyroscope) were pre-processed by applying noise filters and then sampled in fixed-width sliding windows of 2.56 sec and 50% overlap (128 readings/window). The sensor acceleration signal, which has gravitational and body motion components, was separated using a Butterworth low-pass filter into body acceleration and gravity. The gravitational force is assumed to have only low frequency components, therefore a filter with 0.3 Hz cutoff frequency was used. From each window, a vector of features was obtained by calculating variables from the time and frequency domain.

http://archive.ics.uci.edu/ml/datasets/Human+Activity+Recognition+Using+Smartphones






