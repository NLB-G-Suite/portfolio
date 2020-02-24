# First we load both files

emissions_data  <- readRDS("summarySCC_PM25.rds")
scc_data        <- readRDS("Source_Classification_Code.rds")


# Ok now we need those from Baltimore and ON-ROAD type and the same for Los Angeles


motor_emissions <- emissions_data[emissions_data$type=="ON-ROAD" & emissions_data$fips %in% c('24510','06037'),]

# And also aggreagate like the past ones
both_cities_aggregated_by_year <- aggregate(Emissions ~ year + fips , motor_emissions,sum)

both_cities_aggregated_by_year$fips[both_cities_aggregated_by_year$fips=="24510"] <- "Baltimore, MD"
both_cities_aggregated_by_year$fips[both_cities_aggregated_by_year$fips=="06037"] <- "Los Angeles, CA"


# Now we plot that to a png file, using ggplot2 to compare better

library(ggplot2)

png("plot6.png")
g <- ggplot(both_cities_aggregated_by_year, aes(factor(year),Emissions))
g <- g + facet_grid(. ~ fips)
g <- g + geom_bar(stat="identity") + xlab("year") + ylab("Total PM 2.5 Emissions") +
  ggtitle("Total Emissions from motor vehicles in Baltimore and Los Angeles")

print(g)
dev.off()
