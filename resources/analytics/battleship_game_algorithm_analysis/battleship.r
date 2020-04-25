

#install.packages("viridis")
#install.packages("formattable")
require(viridis)
require("lattice")
library(formattable)
library(sqldf)



verify_OpenWaters<-function(i_row,i_col,ship_Size,matrix,ver1_hor0)
{
    DEBUG=0
    Open_Area=1
    if(ver1_hor0==0) for (i in 0:(ship_Size-1)) if (matrix[i_row,i_col+i]>0) Open_Area=0
    if(ver1_hor0==1) for (j in 0:(ship_Size-1)) if (matrix[i_row+j,i_col]>0) Open_Area=0
    if (Open_Area==0 & DEBUG==1) print("The area is not free !!")
    return(Open_Area)
}

place_Ship<-function(ship_Size,matrix,mark_type=1)
{
    # mark_type is the type of marks we will apply to the battlefield matrix when the ship is placed:
    #      1 - just ones
    #      2 - ship_Size - 22, 333, 333, 4444, 55555
    #      3 - orientation - horizontal / vertical
    
    DEBUG=0
    not<-function(x) return(ifelse(x==1,0,1))
    test_matrix<-matrix
    Open_Area=1
    
    hh=ifelse(sample(0:1,1)==0,0,1)
    i_row=sample(1:(dim(test_matrix)-not(hh)*ship_Size)[1],1)
    i_col=sample(1:(dim(test_matrix)-hh*ship_Size)[2],1)
    if (DEBUG==1) print(paste("Trying to add ",ifelse(hh==1,"horizontal","vertical")," ship of size ",ship_Size," at position ",i_row,",",i_col,sep=""))    
    while(verify_OpenWaters(i_row,i_col,ship_Size,test_matrix,not(hh))==0)
    {
        i_row=sample(1:(dim(test_matrix)-not(hh)*ship_Size)[1],1)
        i_col=sample(1:(dim(test_matrix)-hh*ship_Size)[2],1)
        if (DEBUG==1) print(paste("Trying to add ",ifelse(hh==1,"horizontal","vertical")," ship of size ",ship_Size," at position ",i_row,",",i_col,sep=""))    
    }
    for(i in 0:(ship_Size-1))
    {
        if(test_matrix[i_row+not(hh)*i,i_col+hh*i]==0)
        {
            test_matrix[i_row+not(hh)*i,i_col+hh*i]=ifelse(mark_type==1,1,ifelse(mark_type==2,ship_Size,1+ver1_hor0))
            if (DEBUG==1) print(paste("    Coordinates ",i_row,",",i_col+i,"=",test_matrix[i_row+not(hh)*i,i_col+hh*i],sep=""))
        } else {
            print("ERROR: Why here?")
        }
    }
    return(test_matrix)
}

place_fleet<-function(matrix,mark_type=1)
{
    matrix<-place_Ship(2,matrix,mark_type)
    matrix<-place_Ship(3,matrix,mark_type)
    matrix<-place_Ship(4,matrix,mark_type)
    matrix<-place_Ship(5,matrix,mark_type)
    matrix<-place_Ship(6,matrix,mark_type)
    return(matrix)
}

empty_matrix<-matrix(0,nrow=10,ncol=10)
sumat_matrix<-matrix(0,nrow=10,ncol=10)
colnames(sumat_matrix)<-toupper(letters[c(1:10)])
rownames(sumat_matrix)<-c(1:10)

for(a in 1:1000)
{
  sumat_matrix<-sumat_matrix+place_fleet(empty_matrix)  
}


formattable(sumat_matrix)

levelplot(sumat_matrix,col.regions=inferno(500),xlab.top="BATTLESHIP GAME - RANDOM SHIP 10000 PLACEMENT MONTECARLO HEATMAP")




check_Square <- function(x,y,matrix,verbose=0)
{
    ret=ifelse(matrix[x,y]>0,matrix[x,y],0)
    return(ret)
}

fire_Square <- function(x,y,matrix,verbose=0)
{
    ret=0
    ret=check_Square(x,y,matrix)
    if (ret>0) 
    {
        matrix[x,y]=0
        if (verbose==2) print(paste("fire_Square > Ship hit at ",x,",",y," = ",ret,sep=""))
    } else { 
        if (verbose==2) print(paste("fire_Square > Water at ",x,",",y," = ",ret,sep=""))
    }
    return(matrix)
}

#strat3_df<-as.data.frame(shots_byStrategy(runs,strategy=3))
shots_byStrategy<-function(number_runs=100,strategy=1,verbose=0)
{
    result_df <- data.frame(strategy=character(),num_shots=integer(),run_number=integer(),stringsAsFactors=FALSE) 
    for (a in 1:number_runs)
    {
        matrix<- place_fleet(empty_matrix,mark_type=2)  
        result_df[a,1]=strategy
        result_df[a,2]=sink_All(matrix,strategy,verbose)
        result_df[a,3]=a
    }
    return(result_df)
}




is_SinkingShip <-function(ship_Size,strategy_matrix, verbose=0) 
{
    if (sum(sum(strategy_matrix==ship_Size)) < ship_Size & sum(sum(strategy_matrix==ship_Size)) > 0) 
        ret = ship_Size - sum(sum(strategy_matrix==ship_Size)) else ret = 0
        if (verbose > 1 & ret > ship_Size) print(paste("        is_SinkingShip > Ship Squares missing of type ",ship_Size," ? : ",ret,sep=""))
        return (ret)
}

sinking_Ships <- function(strategy_matrix,verbose = 0)
{
    ret = FALSE
    for (a in 2:6)
    {
        if (is_SinkingShip(a,strategy_matrix) > 0) ret = TRUE
    }
    if (verbose > 0) print(paste("    sinking_Ships > Any ? : ",ret,sep=""))
    return (ret)    
}


last_position_SinkingShips<-function(strategy_matrix,verbose=0)
{
    
    sinking_Df <- data.frame(row=integer(),col=integer(),ship_size=integer(),stringsAsFactors=FALSE) 
    killoff_Df <- data.frame(row=integer(),col=integer(),stringsAsFactors=FALSE) 
    for (k in 2:6)
    {
        if (is_SinkingShip(k,strategy_matrix) > 0 )
        {
            if (verbose > 1) print(paste("last_position_SinkingShips > Ship ",k," is sinking - remaining tiles = ",sum(sum(strategy_matrix==k))))
            if (verbose > 1) which(strategy_matrix==k,arr.ind=TRUE)
            pre_sinking_Df<-as.data.frame(which(strategy_matrix==k,arr.ind=TRUE))
            pre_sinking_Df$ship_size<-k
            sinking_Df<-rbind(sinking_Df,pre_sinking_Df)
        }
    }
    return(sinking_Df)
}



kill_off_SinkingShips<-function(sinking_Df,matrix,ps_mat3,selection_type=0,verbose=0)
{
    verbose=2
    max_row=dim(ps_mat3)[1]
    max_col=dim(ps_mat3)[1]
    if (selection_type==0)
    {
        if (verbose > 1) print(paste("Ships sinking:",sep=""))
        sqldf("select ship_size,count(*) as num_tiles,row,col from sinking_Df group by ship_size order by num_tiles ")
        ship_with_min_remaining_tiles <- sqldf("select ship_size,count(*) as num_tiles,row,col from sinking_Df group by ship_size order by num_tiles ")[1,1]
        previous_hits=which(ps_mat3==ship_with_min_remaining_tiles,arr.ind=TRUE)
        # if (nrow(previous_hits)==1)
        # { 
        if (verbose > 0) print(paste("kill_off_SinkingShips > SHOOTING AROUND HIT CELL AT ",previous_hits[1],",",previous_hits[2],"!!!!!",sep=""))
        formattable(ps_mat3)
        possible_shots_X=c(min(max_row,previous_hits[1,1]+1),max(1,previous_hits[1,1]-1))
        possible_shots_Y=c(min(max_col,previous_hits[1,2]+1),max(1,previous_hits[1,2]-1))
        x = possible_shots_X[sample(1:length(possible_shots_X),1)]
        y = possible_shots_Y[sample(1:length(possible_shots_Y),1)]
        while(check_Square(x,y,ps_mat3) > 0)
        {
            x <- possible_shots_X[sample(1:length(possible_shots_X),1)]
            y <- possible_shots_Y[sample(1:length(possible_shots_Y),1)]
        }
        check = check_Square(x,y,ps_mat3) 
        if (check > 0) 
        { 
            if (verbose > 0) print("kill_off_SinkingShips > This should not be happening")
            ps_mat3[x,y] = check
        } else { 
            if (verbose > 0) print(paste("kill_off_SinkingShips > I have never shot at coordinates ",x,",",y,". Storing coordinates for future and firing",sep=""))
            ps_mat3[x,y] = 1 
        }
        matrix_pre_fire <- matrix
        matrix <- fire_Square(x,y,matrix,verbose)
        if (sum(matrix_pre_fire) != sum(matrix))
        {
            print("kill_off_SinkingShips > SHIP HIT - Storing the type of ship in previous_shot_matrx")
            
            ps_mat3[x,y] <- matrix_pre_fire[x,y]
        } 
    }
    return(ps_mat3)
}

#  TESTING PURPOSES - STRATEGY 3
#  matrix<- place_fleet(empty_matrix,mark_type=2)  
#  rm(ps_mat3)
#  ps_mat3<-matrix(0,nrow=dim(matrix)[1],ncol=dim(matrix)[2])
#  strat3_df <- shots_byStrategy(number_runs=1,strategy=3,verbose=2)

sink_All <- function(matrix,strategy = 1,verbose = 0)
{
    shot_Counter = 0
    if (strategy == 2) ps_mat2 <- matrix(0,nrow=dim(matrix)[1],ncol=dim(matrix)[2])
    if (strategy == 3) ps_mat3 <- matrix(0,nrow=dim(matrix)[1],ncol=dim(matrix)[2])

    while(sum(matrix) > 0)
    {
        if (verbose > 0) print(paste("sink_All > shot number ",shot_Counter+1,sep=""))
        if (strategy == 1) matrix <- fire_Square(sample(1:dim(matrix)[1],1),sample(1:dim(matrix)[2],1),matrix,verbose)
        if (strategy == 2)
        {
            x <- sample(1:dim(matrix)[1],1)
            y <- sample(1:dim(matrix)[1],1)
            while(check_Square(x,y,ps_mat2) > 0)
            {
                x <- sample(1:dim(matrix)[1],1)
                y <- sample(1:dim(matrix)[1],1)
            }
            ps_mat2[x,y] = 1
            matrix <- fire_Square(x,y,matrix,verbose)
        }
        if (strategy == 3 )
        {
            if (verbose > 0) print(paste("sink_All > Using Strategy 3",sep=""))
            if (!sinking_Ships(matrix))
            {
                x <- sample(1:dim(matrix)[1],1)
                y <- sample(1:dim(matrix)[1],1)
                if (verbose > 1) print(paste("sink_All > Verifying if we already shot at coordinates ",x,",",y," = ",check_Square(x,y,ps_mat3),sep=""))
                while(check_Square(x,y,ps_mat3) > 0)
                {
                    x <- sample(1:dim(matrix)[1],1)
                    y <- sample(1:dim(matrix)[1],1)
                    if (verbose > 1) print(paste("sink_All > We had already shot there !. Verifying if we already shot at coordinates ",x,",",y," = ",check_Square(x,y,ps_mat3),sep=""))
                }
                check = check_Square(x,y,ps_mat3) 
                if (check > 0) 
                { 
                    if (verbose > 0) print("This should not be happening")
                    ps_mat3[x,y] = check
                } else { 
                    if (verbose > 0) print(paste("I have never shot at coordinates ",x,",",y,". Storing coordinates for future and firing",sep=""))
                    ps_mat3[x,y] = 1 
                }
                if (verbose > 1) print(paste("sink_All > We can shot (untested) at coordinates ",x,",",y," !!!",sep=""))
                matrix_pre_fire <- matrix
                matrix <- fire_Square(x,y,matrix,verbose)
                if (sum(matrix_pre_fire) != sum(matrix))
                {
                    print("sink_All > SHIP HIT - Storing the type of ship in previous_shot_matrx")
                    ps_mat3[x,y] <- matrix_pre_fire[x,y]
                } 
            } else {
                print("sink_All > We have sinking ships already, let's kill them off first !")
                sinking_Df<-last_position_SinkingShips(matrix,verbose)
                ps_mat3<-kill_off_SinkingShips(sinking_Df,matrix,ps_mat3,selection_type=0,verbose)
            }
            
        }
        shot_Counter=shot_Counter + 1
    }
    if (verbose > 0 & strategy == 1) print(paste("Strategy ",strategy," - All Sunk - it took : ",shot_Counter," shots",sep = ""))
    if (verbose > 0 & strategy == 2) print(paste("Strategy ",strategy," - All Sunk - it took : ",shot_Counter," shots - remembered: ",sum(ps_mat2),sep = ""))
    if (verbose > 0 & strategy == 3) print(paste("Strategy ",strategy," - All Sunk - it took : ",shot_Counter," shots - remembered: ",sum(ps_mat3),sep = ""))
    return(shot_Counter)
}


matrix<- place_fleet(empty_matrix,mark_type=2)  
formattable(matrix)



runs=100
strat1_df<-as.data.frame(shots_byStrategy(runs,strategy=1))
strat2_df<-as.data.frame(shots_byStrategy(runs,strategy=2))
strat3_df<-as.data.frame(shots_byStrategy(runs,strategy=3))
title1_str=paste("HISTOGRAM - Shots Needed to Sink All Ships ",runs," Runs",sep="")
title2_str=paste("SCATTERPLOT - Shots Needed to Sink All Ships ",runs," Runs",sep="")
par(mfrow=c(2,2))
hist(strat1_df$num_shots,main=paste("STRATEGY 1 'Random Shooting, No Memory' : ",title1_str,sep=""),xlab="Number of Shots",freq=TRUE,breaks=20,col="orange")
plot(strat1_df$num_shots,main=title2_str,xlab="Run Number",ylab="Shots Needed",col="black",ylim=c(0,max(strat1_df$num_shots)))
lines(lowess(strat1_df$run_number,strat1_df$num_shots),col="orange")

hist(strat2_df$num_shots,main=paste("STRATEGY 2 'Random Shooting, No Repeated Shots' : ",title1_str,sep=""),xlab="Number of Shots",freq=TRUE,breaks=20,col="orange")
plot(strat2_df$num_shots,main=title2_str,xlab="Run Number",ylab="Shots Needed",col="black",ylim=c(0,max(strat2_df$num_shots)))
lines(lowess(strat1_df$run_number,strat2_df$num_shots),col="orange")

hist(strat3_df$num_shots,main=paste("STRATEGY 3 'Random Shooting, Killing off found Ships' : ",title1_str,sep=""),xlab="Number of Shots",freq=TRUE,breaks=20,col="orange")
plot(strat3_df$num_shots,main=title2_str,xlab="Run Number",ylab="Shots Needed",col="black",ylim=c(0,max(strat3_df$num_shots)))
lines(lowess(strat1_df$run_number,strat3_df$num_shots),col="orange")




mean(strat2_df$num_shots)
mean(strat3_df$num_shots)




