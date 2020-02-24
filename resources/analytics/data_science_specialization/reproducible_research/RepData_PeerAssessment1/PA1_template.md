# Untitled


```r
knitr::opts_chunk$set(echo = TRUE)
```

# Loading and preprocessing the data

## 1&2.- Load the data and Process/Transform de data (as necessary)


```r
data <- read.csv(unz("activity.zip", "activity.csv"))
```

# What is mean total number of steps taken per day?

## 1.- Calculate the total number of steps taken per day 

### (i will display only the top 20 to avoid a huge list)


```r
aggr_steps_date<-aggregate(steps ~ date, data=data,FUN=sum)
head(aggr_steps_date,n=20)
```

```
##          date steps
## 1  2012-10-02   126
## 2  2012-10-03 11352
## 3  2012-10-04 12116
## 4  2012-10-05 13294
## 5  2012-10-06 15420
## 6  2012-10-07 11015
## 7  2012-10-09 12811
## 8  2012-10-10  9900
## 9  2012-10-11 10304
## 10 2012-10-12 17382
## 11 2012-10-13 12426
## 12 2012-10-14 15098
## 13 2012-10-15 10139
## 14 2012-10-16 15084
## 15 2012-10-17 13452
## 16 2012-10-18 10056
## 17 2012-10-19 11829
## 18 2012-10-20 10395
## 19 2012-10-21  8821
## 20 2012-10-22 13460
```


## 2.- Make a histogram of the total number of steps taken each day


```r
hist(aggr_steps_date$steps)
```

![](PA1_template_files/figure-html/b2-1.png)<!-- -->
## 3.- Calculate and report the mean and median of the total number of steps taken per day


```r
mean(aggr_steps_date$steps)
```

```
## [1] 10766.19
```

```r
median(aggr_steps_date$steps)
```

```
## [1] 10765
```

# What is the average daily activity pattern?

## 1.- Make a time series plot (i.e. type = "l") of the 5-minute interval (x-axis) and the average number of steps taken, averaged across all days (y-axis)



```r
aggregate_value<-aggregate(steps ~ interval, data=data, FUN=mean)
plot(aggregate_value,type="l")
```

![](PA1_template_files/figure-html/c1-1.png)<!-- -->

## 2.- Which 5-minute interval, on average across all the days in the dataset, contains the maximum number of steps?


```r
aggregate_value$interval[which.max(aggregate_value$steps)]
```

```
## [1] 835
```

# Imputing missing values

## Note that there are a number of days/intervals where there are missing values (coded as NA). The presence of missing days may introduce bias into some calculations or summaries of the data.

## 1.- Calculate and report the total number of missing values in the dataset (i.e. the total number of rows with NAs)


```r
TotalNA<-sum(is.na(data$steps))
TotalNA
```

```
## [1] 2304
```


## 2.- Devise a strategy for filling in all of the missing values in the dataset. The strategy does not need to be sophisticated. For example, you could use the mean/median for that day, or the mean for that 5-minute interval, etc.

### Using 0


```r
datacopy<-data
datacopy$steps[is.na(datacopy$steps)]<-0
```


## 3.- Create a new dataset that is equal to the original dataset but with the missing data filled in.


```r
data$steps[is.na(data$steps)]<-0
```


## 4.- Make a histogram of the total number of steps taken each day and Calculate and report the mean and median total number of steps taken per day. Do these values differ from the estimates from the first part of the assignment? What is the impact of imputing missing data on the estimates of the total daily number of steps?


```r
mean(aggr_steps_date$steps)
```

```
## [1] 10766.19
```

```r
median(aggr_steps_date$steps)
```

```
## [1] 10765
```

```r
hist(aggr_steps_date$steps)
```

![](PA1_template_files/figure-html/d4-1.png)<!-- -->


# Are there differences in activity patterns between weekdays and weekends?

## For this part the weekdays() function may be of some help here. Use the dataset with the filled-in missing values for this part.

## 1.- Create a new factor variable in the dataset with two levels - "weekday" and "weekend" indicating whether a given date is a weekday or weekend day.


```r
weekend<-c("Saturday","Sunday")
day <- as.factor(ifelse(is.element(weekdays(as.Date(datacopy$date)),weekend),"Weekend","Weekday"))
```


## 2.- Make a panel plot containing a time series plot (i.e. type = "l") of the 5-minute interval (x-axis) and the average number of steps taken, averaged across all weekday days or weekend days (y-axis). See the README file in the GitHub repository to see an example of what this plot should look like using simulated data.


```r
par(mfrow=c(1,2))
for (day_clasification in c("Weekday","Weekend"))
{
  group_day_clasification <- aggregate(steps ~ interval, data=datacopy, subset=day==day_clasification, FUN=mean)
  plot(group_day_clasification,type="l",main=day_clasification)
}
```

![](PA1_template_files/figure-html/e2-1.png)<!-- -->
## End
