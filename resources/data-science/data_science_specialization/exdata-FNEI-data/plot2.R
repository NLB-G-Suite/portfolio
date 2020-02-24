

# First we load both files

emissions_data  <- readRDS("summarySCC_PM25.rds")
scc_data        <- readRDS("Source_Classification_Code.rds")


# Baltimore emissions code is 24510 (fips)

baltimore_emissions <- emissions_data[emissions_data$fips=='24510',]


# Now we aggregate by year

baltimore_emissions_aggregated_by_year <-aggregate(Emissions ~ year, baltimore_emissions, sum)

# Now we plot that to a png file 

png("plot2.png")
barplot(height=baltimore_emissions_aggregated_by_year$Emissions, names.arg=baltimore_emissions_aggregated_by_year$year,xlab="years",ylab=expression("Total PM"[2.5]*" emission"),main=expression("Total PM"[2.5]*' in the Baltimore City , MD emissions in various years'))
dev.off()
