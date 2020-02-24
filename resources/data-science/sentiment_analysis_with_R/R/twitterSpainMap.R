# No funciona el register_google(key=api) si se tiene ggmap 2.6.1  hay que quitarlo
#########################################################################################

#remove.packages("ggmap")

#########################################################################################
#Luego se instala desde:
#########################################################################################

#devtools::install_github("dkahle/ggmap")


#########################################################################################
# Echa un ojo aqui https://lucidmanager.org/geocoding-with-ggmap/
# Si el tibble da problemas -> https://stackoverflow.com/questions/41918543/warning-in-install-packages-cannot-remove-prior-installation-of-package-data
#########################################################################################

require(ggmap)
api <- "here your ggmap api"
register_google(key=api)



#########################################################################################
#   An R function to make a personalized map of people you follow and who follow you on twitter. 
#   R functions Copyright (C) 2011 Jeff Leek (jtleek@gmail.com), and the Simply Statistics Blog
#   (http://simplystatistics.tumblr.com, http://twitter.com/simplystats)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details, see <http://www.gnu.org/licenses/>.
#
#
#   These functions depend on the packages: twitteR, maps, geosphere, and RColorBrewer. It will
#   attempt to install them if they are not installed when you source this function. Care
#   should be used when using this function since the twitteR API has rate limiting in place.
#   If you have a large number of followers, or run the function many times, you may be
#   rate limited. 
#
#
#   How to use: 
#       # Source the function
#       source("http://biostat.jhsph.edu/~jleek/code/twitterMap.R")
#
#      # Make your twittermap
#      twitterMap("simplystats")
#
#      #If your location can't be found or latitude longitude can't be calculated
#      #choose a bigger city near you. The list of cities used by twitterMap
#      #can be found like so:
#      data(world.cities)
#      grep("Baltimore",world.cities[,1])
#
#      # Then make the map using that big city
#      twitterMap("simplystats",userLocation="Baltimore")
#   
#      #If you want both your followers and people you follow in a plot you can do:
#      twitterMap("simplystats",plotType="both")
#      
########################################################################################



getPckg <- function(pckg) install.packages(pckg, repos = "http://cran.r-project.org")

pckg = try(require(twitteR))
if(!pckg) {
  cat("Installing 'twitteR' from CRAN\n")
  getPckg("twitteR")
  require("twitteR")
}

pckg = try(require(maps))
if(!pckg) {
  cat("Installing 'maps' from CRAN\n")
  getPckg("maps")
  require("maps")
}

# VER ARRIBA DEL TODO DEL CODIGO !!!
#####################################
# pckg = try(require(ggmap))
# if(!pckg) {
#   cat("Installing 'ggmap' from CRAN\n")
#   getPckg("ggmap")
#   require("ggmap")
# }

pckg = try(require(ggalt))
if(!pckg) {
  cat("Installing 'ggalt' from CRAN\n")
  getPckg("ggalt")
  require("ggalt")
}


pckg = try(require(geosphere))
if(!pckg) {
  cat("Installing 'geosphere' from CRAN\n")
  getPckg("geosphere")
  require("geosphere")
}


pckg = try(require(RColorBrewer))
if(!pckg) {
  cat("Installing 'RColorBrewer' from CRAN\n")
  getPckg("RColorBrewer")
  require("RColorBrewer")
}


get_geocode_string<-function(locationText,radius){ return( paste(paste(geocode(locationText),collapse=","),",",radius,sep="")) }

findLatLon <- function(loc){
  latlon = NA
  cont = NA
  
  # Asia = 1, Africa = 2, North America = 3, South America = 4, Australia/New Zealand = 5, Europe = 6
  continents = matrix(NA,nrow=length(unique(world.cities[,2])),ncol=2)
  continents[,1] = unique(world.cities[,2])
  continents[1:10,2] = c(1,1,1,2,1,1,1,1,1,1)
  continents[11:20,2]= c(1,1,2,1,1,2,1,2,2,2)
  continents[21:30,2] = c(2,1,6,6,6,6,6,6,6,6)
  continents[31:40,2] = c(6,6,6,6,2,4,4,1,2,1)
  continents[41:50,2] = c(4,6,1,4,6,1,3,1,6,6)
  continents[51:60,2] = c(3,2,4,2,6,1,6,1,3,2)
  continents[61:70,2] = c(1,2,2,2,3,6,3,3,6,6)
  continents[71:80,2] = c(1,1,2,6,3,4,3,4,6,1)
  continents[81:90,2] = c(3,3,3,2,2,6,6,6,6,4)
  continents[91:100,2] = c(2,5,2,2,3,1,1,1,1,1)
  continents[101:110,2] = c(1,2,1,1,1,3,2,5,1,6)
  continents[111:120,2] = c(1,6,1,1,2,6,1,1,6,2)
  continents[121:130,2] = c(6,6,6,1,1,3,4,3,4,2)
  continents[131:140,2] = c(6,6,2,2,1,1,1,4,1,1)
  continents[141:150,2] = c(1,2,2,1,1,1,4,6,6,2)
  continents[151:160,2] = c(4,1,1,1,1,2,4,6,2,2)
  continents[161:170,2] = c(1,2,2,1,6,2,1,1,6,1)
  continents[171:180,2] = c(1,1,1,2,6,2,2,6,1,1)
  continents[181:190,2] = c(2,6,2,1,6,6,3,3,3,3)
  continents[191:200,2] = c(2,2,2,2,3,2,3,2,3,1)
  continents[201:210,2] = c(3,2,2,2,2,2,2,1,6,2)
  continents[211:220,2] = c(1,3,1,6,2,4,3,6,3,4)
  continents[221:230,2] = c(1,1,1,3,2,3,3,6,1,6)
  continents[231:232,2] = c(2,1)
  
  
  # Get the first element of the location
  # firstElement = strsplit(loc,"[^[:alnum:]]")[[1]][1]
  firstElement = strsplit(loc,",")[[1]][1]
  if(is.na(firstElement)){firstElement="zzzzzzzzz"}
  
  # See if it is a city
  tmp = grep(firstElement,world.cities[,1],fixed=TRUE)
  tmp2 = grep(firstElement,state.name,fixed=TRUE)
  tmp3 = grep(firstElement,world.cities[,2],fixed=TRUE)
  
  if(length(tmp) == 1){
    latlon = world.cities[tmp,c(5,4)]
    cont = continents[which(world.cities[tmp,2]==continents[,1]),2]
  }else if(length(tmp) > 1){
    tmpCities = world.cities[tmp,]
    latlon = tmpCities[which.max(tmpCities$pop),c(5,4)]
    cont = continents[which(tmpCities[which.max(tmpCities$pop),2]==continents[,1]),2]
  }else if(length(tmp2) == 1){
    latlon = c(state.center$x[tmp2],state.center$y[tmp2])
    cont = 3
  }else if(length(tmp3) > 0){
    tmpCities = world.cities[tmp3,]
    latlon = tmpCities[which.max(tmpCities$pop),c(5,4)]
    cont = continents[which(tmpCities[which.max(tmpCities$pop),2]==continents[,1]),2]
  }
  
  return(list(latlon=latlon,cont=as.numeric(cont)))
  
}


getGreatCircle = function(userLL,relationLL){
  tmpCircle = greatCircle(userLL,relationLL)
  start = which.min(abs(tmpCircle[,1] - userLL[1,1]))
  end = which.min(abs(tmpCircle[,1] - relationLL[1]))
  greatC = tmpCircle[start:end,]
  return(greatC)
}

trim <- function (x) gsub("^\\s+|\\s+$", "", x)

#######################################################################
#######################################################################
#######################################################################
#######################################################################
#######################################################################
#######################################################################

source("prepare_tweet_search.R")

twitterSpainMap <- function(userName,locationText,radius,Zoomv,nMax = 1000,mincol,maxcol){
  # nMax=1000
  # userName="vox_es"
  # userLocation=NULL
  # # Get Location data
  # cat("Getting data from Twitter, this may take a moment.\n")
  userName="votar a vox"
  locationText="Madrid"
  radius="500mi"
  Zoomv=6
  mincol="#009900"
  maxcol="#003300"
  nMax=5000
  


             
             
  #geocodetext=paste(paste(paste(geocode(locationText),collapse=","),",",radius,sep=""))
  #followers<-prepare_tweet_search(userName,nMax,FechaInicial=NULL,FechaFinal=NULL,RetryLimit=5,NoRetweet=FALSE,"CODE")
  st<-searchTwitter(userName, n=nMax,lang="es",retryOnRateLimit=5)#,geocode=geocodetext) 
  #st = twListToDF(strip_retweets(st))
  st = twListToDF(st)  
  followers<-do.call("rbind",lapply(st,as.data.frame))
          #followersLocation = sapply(followers2,function(x){location(x)})
  # Find the latitude and longitude of the user
  # cat("Getting geographic (latitude/longitude) of Twitter users.\n")
  # userLL <- findLatLon(userLocation)$latlon
  # if(any(is.na(userLL))){stop("We can't find the latitude and longitude of your location from Twitter")}
  
  # Find the latitude and longitude of each of the followers
  # and calculate the distance to the user
  followersLL = matrix(NA,nrow=length(st),ncol=4)
  for(i in 1:length(followers_o)){
    if(length(followersLocation[[i]]) > 0){
      tmpLL = findLatLon(trim(followersLocation[[i]]))
      if(any(!is.na(tmpLL$latlon))){
        #followersLL[i,] = c(unlist(tmpLL$latlon),distCosine(userLL,tmpLL$latlon),unlist(tmpLL$cont))
        followersLL[i,] = c(unlist(tmpLL$latlon),1,unlist(tmpLL$cont))
      }
    }
  }
  followersLL = followersLL[order(-followersLL[,3]),]
  followersLL = followersLL[!is.na(followersLL[,1]),]
  cat("Plotting results.\n")
  cols = brewer.pal(7,"Set2")
  mydata=followersLL
  mv_num_collisions = data.frame(mydata[,3], mydata[,1], mydata[,2])
  colnames(mv_num_collisions) = c('collisions','lon','lat')    
  
  df<-mv_num_collisions
  dfNZ<-df[df[1]>0,] 

  Spain_map <- get_map(location=locationText, zoom=Zoomv,api_key=key,color="bw")  
  qq<-ggmap(Spain_map, extent = "device") + 
    geom_point(aes(x = lon, y = lat, colour = "#003300"), data = dfNZ,size=10 )
      stat_density2d(data = dfNZ,
                     aes(x = lon, y = lat, fill = ..collisions.., alpha = ..collisions..), size = 100,
                     bins = 5, geom = "polygon",contour=TRUE) + #scale_fill_gradient(low = mincol, high = maxcol) +
      scale_alpha(range = c(0.4, 0.75), guide = FALSE)     ###  
  print(qq)
#  return(dfNZ)
}


Zoomv=12

  vox<-twitterSpainMap("vox_es","Madrid",Zoomv,nMax = 300,mincol,maxcol)
  filename=paste(path,"Analisis/","vox",".png",sep="")
  dev.copy(png,filename,width=1280,height=1280)
  dev.off()
  print(paste("emocion_comparativa::Nuevo fichero de salida en ",filename,sep=""))  

  
  
  
  
  
   
SeguidoresTwitter<-function(userName,locationText,radius,Zoomv,nMax = 1000,mincol,maxcol){
    ###############################
    # TESTING
    ###############################
    # userName="vox_es"
    # locationText="Madrid"
    # radius="500mi"
    # Zoomv=12
    # mincol="#009900"
    # maxcol="#003300"
    # nMax=200
    ###############################
    tmp=getUser(userName)
    followers_o=tmp$getFollowers(n=nMax)
    followersLocation_o = sapply(followers_o,function(x){location(x)})
    followersLL_o = matrix(NA,nrow=length(followers_o),ncol=2)
    for(i in 1:length(followers_o)){
      if(length(followersLocation_o[[i]]) > 0){
        #tmpLL_o2 = findLatLon(trim(followersLocation_o[[12]]))                         # <- CUIDADO CON EL tmpLL_o . LA CLAVE ESTA AQUI. USA EL GEOCODE
        #tmpLL_o = geocode(trim(followersLocation_o[[i]]))
        dec<-geocode(trim(followersLocation_o[[i]]))
        followersLL_o[i,]=c(dec$lat,dec$lon)
        # if(any(!is.na(tmpLL_o$lat))){                                             # <- CUIDADO CON EL tmpLL_o . LA CLAVE ESTA AQUI. USA EL GEOCODE
        #   followersLL_o[i,] = c(unlist(tmpLL_o$lat),unlist(tmpLL_o$lon))      # <- CUIDADO CON EL tmpLL_o . LA CLAVE ESTA AQUI. USA EL GEOCODE  
        # }
      }
    }
    #followersLL_o = followersLL_o[order(-followersLL_o[,3]),]
    followersLL_o = followersLL_o[!is.na(followersLL_o[,1]),]
    cat("Plotting results.\n")
    cols = brewer.pal(7,"Set2")
    mydata_o=followersLL_o
    mv_num_collisions_o = data.frame(mydata_o[,1], mydata_o[,2])
    colnames(mv_num_collisions_o) = c('lat','lon')    
    
    df_o<-mv_num_collisions_o
    dfNZ_o<-df_o[df_o[1,]>0] 
    
    Spain_map_o <- get_map(location=locationText, zoom=Zoomv,api_key=key,color="bw")  
    theme_set(theme_bw(base_size=8))
    
    ############
    ############
    ############

    qq<-ggmap(Spain_map_o, extent = "device") + 
      geom_point(aes(x = lon, y = lat, colour = maxcol), data = df_o ,size=2 )#+
     # stat_density2d(data = df_o,
     #                aes(x = lon, y = lat, fill = ..level.., alpha = ..level..), size = 1,
     #                bins = 50, geom = "polygon",contour=TRUE) + #scale_fill_gradient(low = mincol, high = maxcol) +
      # scale_alpha(range = c(0.1, 0.2), guide = FALSE)     ###  
    
    
    print(qq)
        
     #  qq<-ggmap(Spain_map_o, extent = "device") + 
     # #   #geom_point(aes(x = lon, y = lat, colour = "#003300"), data = dfNZ_o,size=10 )+
     #     stat_density2d(data = dfNZ_o,
     #                    aes(x = lon, y = lat, fill = ..level.., alpha = ..level..), size = 1,
     #                    bins = 5, geom = "polygon",contour=TRUE,h=0.01) + scale_fill_gradient(low = mincol, high = maxcol) +
     #     scale_alpha(range = c(0.1, 0.1), guide = FALSE)     ###  
     #   print(qq)
    #  print(qq)
      # pred.stat.map<-ggmap(Spain_map_o,extent="device") + #dfNZ_o + 
      #   geom_point(aes(x = lon, y = lat, z=collisions),data=dfNZ_o)+
      #   stat_summary_2d(fun=median,binwidth=c(.05,.05),alpha=0.5,z=collisions,data=dfNZ_o) + 
      #   scale_fill_gradientn(name="Median",colours=terrain.colors(10),space="Lab")+
      #   labs(x="Longitud",y="Latitud")+coord_map()
      # print(pred.stat.map)
    #  geom_point(aes(x = lon, y = lat, colour = "#003300"), data = dfNZ_o,size=10 )
    # stat_density2d(data = dfNZ_o,
    #                aes(x = lon, y = lat, fill = ..level.., alpha = ..level..), size = 1,
    #                bins = 30, geom = "polygon",contour=TRUE,h=0.01) + scale_fill_gradient(low = mincol, high = maxcol) +
    # scale_alpha(range = c(0.1, 0.1), guide = FALSE)     ###  
    
    
    # pred.points<-ggplot(data=dfNZ_o,aes(x=lon,y=lat,colour=mincol))+
    #   stat_summary_2d(fun=mean,binwidth=c(.05,.05))+
    #   scale_fill_gradientn(name="Median",colours="YlOrBr",space="Lab")+coord_map()
    # print(pred.points)
    
    #########################################################################
    #########################################################################
    #########################################################################
    
    # data=dfNZ_o
    # GEO_CENTROID_LON=dfNZ_o$lon
    # GEO_CENTROID_LAT=dfNZ_o$lat
    # prediction=dfNZ_o$collisions
    # 
    # pred.points <- ggplot(data = data,
    #                       aes(x = GEO_CENTROID_LON,
    #                           y = GEO_CENTROID_LAT,
    #                           colour = prediction)) + 
    #   geom_point()
    # print(pred.points)
    #########################################################################
    #########################################################################
    #########################################################################
    
    # pred.stat <- ggplot(data = data,
    #                     aes(x = GEO_CENTROID_LON,
    #                         y = GEO_CENTROID_LAT,
    #                         z = prediction)) + 
    #   stat_summary2d(fun = mean)
    # print(pred.stat)
    #########################################################################
    #########################################################################
    #########################################################################
    # require("RColorBrewer")
    # YlOrBr <- c("#FFFFD4", "#FED98E", "#FE9929", "#D95F0E", "#993404")
    # pred.stat.bin.width <- ggplot(data = data,
    #                               aes(x = GEO_CENTROID_LON,
    #                                   y = GEO_CENTROID_LAT,
    #                                   z = prediction)) + 
    #   stat_summary2d(fun = median, binwidth = c(.05, .05)) + 
    #   scale_fill_gradientn(name = "Median",
    #                        colours = YlOrBr,
    #                        space = "Lab") +
    #   coord_map()
    # print(pred.stat.bin.width)
    #########################################################################
    #########################################################################
    #########################################################################
    # COMO REFERENCIA
    
    #qq<-ggmap(Spain_map_o, extent = "device") + 
    #  geom_point(aes(x = lon, y = lat, colour = "#003300"), data = dfNZ_o,size=10 )
    # stat_density2d(data = dfNZ_o,
    #                aes(x = lon, y = lat, fill = ..level.., alpha = ..level..), size = 1,
    #                bins = 30, geom = "polygon",contour=TRUE,h=0.01) + scale_fill_gradient(low = mincol, high = maxcol) 
    #########################################################################
    #########################################################################
    #########################################################################
    
    # require(ggmap)
    # locationText="Madrid"
    # map.in <- get_map(location=locationText, zoom=Zoomv,api_key=key,color="bw")  # c(min(data$GEO_CENTROID_LON),min(data$GEO_CENTROID_LAT),max(data$GEO_CENTROID_LON),max(data$GEO_CENTROID_LAT)),source = "osm")
    # theme_set(theme_bw(base_size = 8))
    
    
    # pred.stat.map <- ggmap(map.in,extent="device")+
    #   #geom_point(aes(x = GEO_CENTROID_LON,y = GEO_CENTROID_LAT),data=dfNZ_o)+
    #   geom_point(aes(x=lon,y=lat),data=dfNZ_o,pch=21,size=5)+
    #      # z = prediction)) +
    #   #stat_summary_2d(fun = median, binwidth = c(.05, .05), alpha = 0.5)+
    #   stat_summary_2d(fun = function(x) sum(x),data=dfNZ_o,aes(x=GEO_CENTROID_LON,y=GEO_CENTROID_LAT,z=1), binwidth = c(.05, .05), alpha = 0.5 ) + 
    #   scale_fill_gradientn(name = "Median",
    #                        colours = YlOrBr,
    #                        space = "Lab") + 
    #   labs(x = "Longitude",
    #        y = "Latitude") +
    #   coord_map()
    # print(pred.stat.map)
    #########################################################################
    #########################################################################
    #########################################################################
    
    
    filename=paste(path,"Analisis/",userName,"_followers_",as.character(Zoomv),".png",sep="")
    dev.copy(png,filename,width=1380*2,height=1035*2)
    dev.off()
    print(paste("emocion_comparativa::Nuevo fichero de salida en ",filename,sep=""))
    
    return(filename)
  }
  vox   <-  SeguidoresTwitter("vox_es",locationText,"500mi",11,nMax = 1000,"#009900","#003300")
  psoe  <-  SeguidoresTwitter("psoe",locationText,"500mi",11,nMax = 1000,"#990000","#330000")
  pp    <-  SeguidoresTwitter("ppopular",locationText,"500mi",11,nMax = 1000,"#000099","#000033")
  cds   <-  SeguidoresTwitter("ciudadanoscs",locationText,"500mi",11,nMax = 1000,"#FFA500","#AA5100")
  podemos  <-  SeguidoresTwitter("podemos",locationText,"500mi",11,nMax = 1000,"#FFA500","#AA5100")
  
  figure1 <- multi_panel_figure(columns=4,rows=2,panel_label_type="lower-alpha",width=1380*2,height=1035*2,panel_clip="false",figure_name=outputfile,unit="points")  
  figure1 %<>%
    fill_panel(vox, column = 1, row = 1,scaling="fit") %<>%
    fill_panel(psoe, column = 3, row = 1,scaling="fit") %<>%
    fill_panel(cds, column = 3, row = 2,scaling="fit") %<>%
    fill_panel(pp, column = 4, row = 1,scaling="fit") %<>%
    fill_panel(podemos, column = 4, row = 2,scaling="fit") 
  figure1
    

  vox   <-  SeguidoresTwitter("vox_es",locationText,"500mi",11,nMax = 2400,"#009900","#003300")
  psoe  <-  SeguidoresTwitter("psoe",locationText,"500mi",11,nMax = 5000,"#990000","#330000")
  pp    <-  SeguidoresTwitter("ppopular",locationText,"500mi",11,nMax = 5000,"#000099","#000033")
  cds   <-  SeguidoresTwitter("ciudadanoscs",locationText,"500mi",11,nMax = 5000,"#FFA500","#AA5100")
  