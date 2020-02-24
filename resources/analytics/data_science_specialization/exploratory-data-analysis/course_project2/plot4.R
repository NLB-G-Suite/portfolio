# First we load both files

emissions_data  <- readRDS("summarySCC_PM25.rds")
scc_data        <- readRDS("Source_Classification_Code.rds")

# Using grep now to get the coal data

scc_coal_data <- scc_data[grep('coal', scc_data$Short.Name),]

# now we need the coal_emissions from the scc coal data we got before
coal_emissions <- emissions_data[emissions_data$SCC %in% scc_coal_data$SCC,]

# Now like previous times we aggregate (only by year now) but with the new subset we just created
coal_emissions_aggregated_by_year <-aggregate(Emissions ~ year, coal_emissions, sum)


# Now we plot that to a png file, I will use BASE again

png("plot4.png")
plot(coal_emissions_aggregated_by_year$year, coal_emissions_aggregated_by_year$Emissions ,type="b", xlab="Year",
     ylab=expression("PM"[2.5]* " Emissions (tons)"),
     main=expression("PM"[2.5]* " Emissions from coal combustion sources in US"))
dev.off()
