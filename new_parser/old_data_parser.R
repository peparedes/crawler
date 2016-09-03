#parser for old data on stout
library(dplyr)
library(XML)
library(plyr)

setwd("../old_downloads")

file_list<-list.files()

# returns a list of dataframes each of which contains info about 1 post of the particular user
parse_xml <- function(fileName, file_list) {
    #print(fileName)
    
    doc = tryCatch({
        xmlParse(fileName)
    }, error = function(e) {
        if (!file.exists("../new_parser/old_corrupted_files.txt")) {
            file.create("../new_parser/old_corrupted_files.txt")
        }
        write(fileName,file="../new_parser/old_corrupted_files.txt",append=TRUE)
        NA
    })
    
    if (is.na(doc)) {
        return (NA)
    }
    
    # collect all the posts in a list
    posts <- getNodeSet(doc,"//post")
    
    x<-c()
    
    for (post in posts) {
        x<-rbind(x, parse_post(post))
    }
    
    return (data.frame(x))
}

#function that takes in a post and returns a data frame with all the info
parse_post<- function (post) {
    userID <- xmlValue(post[['user']][[1]])
    moodID <- xmlValue(post[['props']][['current_moodid']][['int']][[1]])
    postID = xmlValue(post[['ditemid']][['int']][[1]])
    postDate = xmlValue(post[['eventtime']][['string']][[1]])
    postContent = xmlValue(post[['event']][['string']][[1]])
    
    if (is.na(moodID)) {
        moodID=""
    }
    if (is.null(moodID)) {
        moodID=""
    }
    
    return (list(userID=userID, moodID=moodID, postID=postID,postDateID=postDate, postContent=postContent))
}

parsed_info <- parse_xml("zzzzzzzzzzzzzzz.xml", sort(file_list))
View(parsed_info)

