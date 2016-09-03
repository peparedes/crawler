#parser for old data on stout
library(dplyr)
library(XML)
library(plyr)

setwd("../old_downloads")

file_list<-list.files()

# returns a list of dataframes each of which contains info about 1 post of the particular user
parse_xml <- function(fileName, file_list) {
    print(fileName)
    
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
    
    userID = getNodeSet(doc,"//post/user")
    moodID = getNodeSet(doc,"//post/current_moodid")
    postID = getNodeSet(doc,"//post/ditemid/int")
    postDate = getNodeSet(doc,"//post/eventtime/string")
    postContent = getNodeSet(doc,"//post/event/string")
    return (c(userID, moodID, postID, postDate, psitContent))
}

#create a folder within downloads to put the parsed data
if(!dir.exists("parsed_data")) {
    dir.create("parsed_data")
}

for (i in 1:length(file_list)) {
    parsed_info <- parse_xml(file_list[i], sort(file_list))
    if (is.na(parsed_info)) {
    } else {
        #df of all assembled dfs to write in file
        super_df<-ldply(parsed_info, rbind)
        super_df<-super_df[ , !(names(super_df) %in% c(".id"))]
        username<-substr(file_list[i], 1, nchar(file_list[i])-4)
        write.csv(super_df, paste("parsed_data/",username, ".csv", sep=""), row.names = FALSE)
    }
}
