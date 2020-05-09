# SHINY - PART1

# Web Application framework for R
# Graphical interfaces : visualization, models, algorithms, ...


install.packages("shiny")
library(shiny)


# SHINY needs two R files in a directory (at least):

# ui.R (user interface and how it looks)
# server.R (controls how your app does)


# EXAMPLE OF ui.R

library(shiny)
shinyUI(fluidPage(
    titlePanel("Data science FTW!"),
    sidebarLayout(
        sidebarPanel(
            h3("Sidebar Text")
        ),
        mainPanel(
            h3("Main Panel Text")
        )
    )
))