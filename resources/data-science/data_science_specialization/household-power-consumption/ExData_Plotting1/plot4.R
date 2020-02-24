# ----------------------------
# Downloading the file
# ----------------------------

      # First let's delete everything to avoid troubles
      rm(list=ls())
      # Destination file
      filename="exdata-data-household_power_consumption.zip"
      if(!file.exists(filename)) {
        download.file("https://d396qusza40orc.cloudfront.net/exdata%2Fdata%2Fhousehold_power_consumption.zip",filename)
        file <- unzip(filename)
        unlink(filename)
      }

# ----------------------------
# Loading the csv data & getting only the rows we are going to use for speed
# ----------------------------
      
      imported<-read.table("household_power_consumption.txt",sep=";",header=T)
      formatted_date<-as.Date(imported$Date,format="%d/%m/%Y")
      imported$Date<-as.Date(imported$Date,format="%d/%m/%Y")

# ----------------------------
# Preformatting the data
# ----------------------------      
      # In order to work properly we convert to numeric
      # i had to be very careful here because my date is normally written different with month instead of day order
      # i was getting wrong data
      DATA <- imported[(imported$Date=="2007-02-01") | (imported$Date=="2007-02-02"),]
      DATA$Global_active_power <- as.numeric(as.character(DATA$Global_active_power))
      DATA$Global_reactive_power <- as.numeric(as.character(DATA$Global_reactive_power))
      DATA$Voltage <- as.numeric(as.character(DATA$Voltage))
      DATA <- transform(DATA, Datetime=as.POSIXct(paste(Date, Time)), "%d/%m/%Y %H:%M")
      DATA$Sub_metering_1 <- as.numeric(as.character(DATA$Sub_metering_1))
      DATA$Sub_metering_2 <- as.numeric(as.character(DATA$Sub_metering_2))
      DATA$Sub_metering_3 <- as.numeric(as.character(DATA$Sub_metering_3))


# ----------------------------
# PLOT4
# ----------------------------      
      
      # Now 4 graphs 
      par(mfrow=c(2,2))
      # Change the locale if needed as explained in Plot2 
      Sys.setlocale("LC_TIME","English") 
      
      
      # First the Plot2. Seems the ylab does not have the (kilowatts)
      plot(DATA$Datetime,DATA$Global_active_power,type="l",col="black",xlab="",ylab="Global Active Power")      

      # Second one. This is a new one. 
      # Seems just a plot with Voltage, Datetime, xlab & ylab, col="black" ?, type="l"
      
      plot(DATA$Datetime,DATA$Voltage, col="black",type="l",xlab="datetime",ylab="Voltage")
      
      
      
      # Third one. we already have it. But seems we don't need the legend box
      # to remove the legend box is bty="n"
      
      plot(DATA$Datetime,DATA$Sub_metering_1,type="l",col="black",xlab="",ylab="Energy sub metering")
      lines(DATA$Datetime, DATA$Sub_metering_2, col="red")
      lines(DATA$Datetime, DATA$Sub_metering_3, col="blue")
      legend("topright",bty="n", col=c("black","red","blue"),c("Sub_metering_1","Sub_metering_2","Sub_metering_3"),lty=c(1,1))
      
      # Fourth one. Another new one
      # Seems it is another simple plot with datetime and the inactive power, col="black"
      # the two labels, type line again and no title
      
      plot(DATA$Datetime,DATA$Global_reactive_power, col="black",type="l",xlab="datetime",ylab="Global_reactive_power")
      
      
      # And again let's save under PLOT4.PNG
      dev.copy(png, file="plot4.png", width=480, height=480)
      dev.off()      
      
      
      
      
      
      
      
      
      
      