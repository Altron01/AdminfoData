library(lubridate)
library(dplyr)
library(stringr)

getData <- function(column, textStart, textEnd){
  container <- column
  container <- gsub(textStart, "" , container)

    container <- gsub(textEnd, "" , container)
  container <- gsub(",", "" , container)
  return (container)
}

dateGenerator <- function(){
  reviews <- mutate(reviews, postDate = as.Date(with(reviews, paste(day, month, year, sep = "-")), "%d-%m-%Y"))
  reviews <- select(reviews, -day, -month, -year)
}
reviews <- tbl_df(read.csv("reviews.csv", sep = "~", colClasses = c("character", "character", "character", "character", "character", "character", "character", "character"), comment.char = "", quote=""))

#id cleaned as integer
#rows without id tend to have error in others elements so they cant be cleaned
reviews$id <- as.integer(gsub("[^0-9]", "" , reviews$id))
reviews <- filter(reviews, !is.na(id))
#helpfulReview cleaned as integer
reviews$helpfulReview <- as.integer(getData(reviews$helpfulReview, "\t", " of.*"))
#funnyReview cleaned as integer
reviews$funnyReview <-as.integer(getData(reviews$funnyReview, "@@@@@@@@@@", " people.*"))
#hoursPlayed cleaned as integer
reviews$hoursPlayed <-as.numeric(getData(reviews$hoursPlayed, "@@@@@@@@@@", " hrs.*"))
#postDate cleaner into date
reviews$postDate <- getData(reviews$postDate, "Posted: ", "@@@@@@@@@@")
for (i in 1:length(reviews$postDate)){
  if(length(unlist(strsplit(reviews$postDate[i], " "))) > 3){
    reviews$postDate[i] <- NULL
  }
}
#Clear duplicates
reviews <- reviews[!duplicated(reviews[, c("reviewText")]), ]
#Clear unusable rows
reviews <- reviews[-grep("Posted: ", reviews$reviewText),]

#Random Stuff
View(reviews[grep("Posted: ", reviews$reviewText), ])
View(reviews %>% filter(str_detect(reviewText, "Posted:")))
View(reviews)
