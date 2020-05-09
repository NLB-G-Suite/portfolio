# SHINY 1.2
# ------------------------------------------------------------------------------------------------------------------------
# Talks about creating the Shiny web app through "File/New/Shiny and select the two files : UI.R and SERVER.R" 
# It is possible in the other way too, only with app.r because what matters is just the named functions inside the file.
# Still we are going with UI.R and server.R
# ------------------------------------------------------------------------------------------------------------------------

# Example Files :

# UI.R

library(shiny)
shinyUI(fluidPage(                            # it is a default type of page. We are using it.
    titlePanel("Data Science FTW!"),
    sidebarLayout(
        sidebarPanel(
            h3("Sidebar Text")
        ),
        mainPanel(
            h3("Main Panel Text")
        )
    )
))

# SERVER.R

library(shiny)
shinyServer(function(input,output)
{
    # In this case the server is not going to do anything so it is left blank
    
}
)


# We can run it through the "run button" or by command


setwd("~/test") # or wherever you have it
runApp()


# or 

runApp("~/test") #directly
