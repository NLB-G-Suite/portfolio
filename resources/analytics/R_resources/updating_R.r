# installing/loading the package:
if(!require(installr)) {
    install.packages("installr"); 
    require(installr)
} #load / install+load installr

updateR()



## get packages installed
packs = as.data.frame(installed.packages(.libPaths()[1]), stringsAsFactors = F)

## and now re-install install packages using install.packages()
install.packages(packs$Package)

