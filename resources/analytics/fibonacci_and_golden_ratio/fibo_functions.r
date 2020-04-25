fibo_Value <- function(nx)
{
    for (k in 0:nx)
    {
            if (k==0) fibo = 0
            if (k==1) fibo = 1
            if (k==2) fibo = 1
            if (k>2)  fibo=fibo_Value(k-1)+fibo_Value(k-2)
    }
    return(fibo)
}



lucas_Value <- function(nx)
{
    for (k in 0:nx)
    {
        if (k==0) lucas = 0
        if (k==1) lucas = 1
        if (k==2) lucas = 3
        if (k>2)  lucas=lucas_Value(k-1)+lucas_Value(k-2)
    }
    return(lucas)
}

for (k in 0:25) print(paste(k," - ",fibo_Value(k),"-",lucas_Value(k),sep=""))




Binet_formula <- function(nx)
# To find quickly fibo    
{
    
    Phi = (1 + sqrt(5))/2
    phi = 1 - Phi

    ret = (Phi^nx -(-phi)^nx)/sqrt(5)
    return (ret)
    
}


for (k in 0:20) print(paste(k," - ",fibo_Value(k),"-",Binet_formula(k),sep=""))

