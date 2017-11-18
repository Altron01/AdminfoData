library(lubridate)
library(dplyr)

games <- tbl_df(read.csv("gameData.csv", sep = "~", colClasses = c("character", "character", "character", "character", "character", "character", "character", "character", "character")))

View(games)
#Data Cleaning for games
#Remove rows without id
games <- games %>% filter(!is.na(as.integer(id)))
games$id <- as.integer(games$id)
#Remove repeated games
games <- games[!duplicated(games[, c("url")]), ]
#Take out games without cost
games <- filter(games, realCost != "")
#Clean the realCost of games
games$realCost <- gsub("\t", "", games$realCost)
games$realCost <- gsub("S/.", "", games$realCost)
games$realCost <- gsub("Free.*", "0", games$realCost)
games$realCost <- as.numeric(games$realCost)
#Clean the discCost of games
games$discountCost <- gsub("S/.", "", games$discountCost)
games$discountCost <- as.integer(games$discountCost)
#Clean the date into a date column
dates <- read.table(text = gsub(",", "", games$releaseDate), sep = " ", colClasses = "character")
dates <- with(dates, paste(V1, V2, V3, sep="-"))
games$releaseDate <- dates
