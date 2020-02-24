# First we load both files

emissions_data  <- readRDS("summarySCC_PM25.rds")
scc_data        <- readRDS("Source_Classification_Code.rds")


# Now we aggregate by year

total_emissions_by_year <-aggregate(Emissions ~ year, emissions_data, sum)

# Now we plot that to a png file 

png("plot1.png")
plot(total_emissions_by_year$year,total_emissions_by_year$Emissions,type="b",
     xlab="Year",
     ylab="PM2.5 Emissions (tons)",
     main="Total PM2.5 Emissions in U.S")
dev.off()
