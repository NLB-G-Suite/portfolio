
# NOTA !!!

# Recuerda el setwd("c:/tudirectorio/") antes de empezar !!


# Fichero de configuracion:
#
# Aqui datos de autenticacion del bot de twitter

consumer_key <- "your_consumer_key"
consumer_secret <- "your_consumer_secret"

access_token <- "your_access_token"
access_secret <- "your_access_secret"

# PATH

path<-"/tuit_sentimiento/R/"

# BUSQUEDAS



get_code<-function()
{
  return(sample(1000000:9999999,1,replace=T))
}

filtraPalabras<-function(lista){
  filtro <- c("por","eso","cual","que","no","se","les","va","un","como","este","haya","han","lo","de","la","en","es","más","del","forma","parte","con","algunos","pero","los","muy","qué","las","...","como","empezado","esto","esta","siendo","mañana","ñ","para",'"dict...',"ante","esos","sobre","debería","hace")
  filtro_letters  <- letters[1:26]
  lista <- removeWords(removeWords(lista,filtro),filtro_letters)
  return(lista)
}