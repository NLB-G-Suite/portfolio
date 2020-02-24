# First we load both files

emissions_data  <- readRDS("summarySCC_PM25.rds")
scc_data        <- readRDS("Source_Classification_Code.rds")


# Ok now we need those from Baltimore and ON-ROAD type

baltimore_motor_emissions <- emissions_data(emissions_data$fips=="24510" & emissions_data$type=="ON-ROAD")

# And also aggreagate like the past ones
baltimore_motor_emissions_aggregated_by_year <-aggregate(Emissions ~ year, baltimore_motor_emissions, sum)


# Now we plot that to a png file, I will use BASE again 

png("plot5.png")
plot(baltimore_motor_emissions_aggregated_by_year$year, baltimore_motor_emissions_aggregated_by_year$Emissions ,type="b", xlab="Year",
     ylab=expression("PM"[2.5]* " Emissions (tons)"),
     main=expression("PM"[2.5]* " Emissions from motor vehicles in Baltimore City"))
dev.off()
