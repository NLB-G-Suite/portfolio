# First we load both files

emissions_data  <- readRDS("summarySCC_PM25.rds")
scc_data        <- readRDS("Source_Classification_Code.rds")

# ggplot2 required this time 
library(ggplot2)

# Baltimore emissions code is 24510 (fips) this time aswell

baltimore_emissions <- emissions_data[emissions_data$fips=='24510',]

# Now we aggregate by year AND type

baltimore_emissions_aggregated_by_year_and_type <-aggregate(Emissions ~ year + type, baltimore_emissions, sum)


# Now we plot that to a png file 

png("plot3.png")
g <- ggplot(baltimore_emissions_aggregated_by_year_and_type, aes(year, Emissions, color = type))
g <- g  + geom_line() + xlab("year") + ylab(expression("Total PM"[2.5]*" Emissions")) +
  ggtitle("Total Emissions in Baltimore City from 1999 to 2008")
print(g)
dev.off()
