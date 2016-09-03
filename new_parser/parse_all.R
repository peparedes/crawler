library(dplyr)
library(XML)
library(plyr)

# there are some issues with files that are corrupted in some way. Need
# to add error handling to not halt execution 
setwd("../downloads")

file_list<-list.files()

# returns a list of dataframes each of which contains info about 1 post of the particular user
parse_xml <- function(fileName, file_list) {
    print(fileName)
    
    doc = tryCatch({
        xmlParse(fileName)
    }, error = function(e) {
        if (!file.exists("../new_parser/corrupted_files.txt")) {
            file.create("../new_parser/corrupted_files.txt")
        }
        write(fileName,file="../new_parser/corrupted_files.txt",append=TRUE)
        NA
    })

    if (is.na(doc)) {
        return (NA)
    }
    
    
    values = getNodeSet(doc, "//member/value")
    names = getNodeSet(doc, "//member/name")
    
    values<-sapply(values, xmlValue)
    names<-sapply(names, xmlValue)
    
    df<- data.frame(names=names, values=values)
    
    counter<-0
    splitting_array<-c()
    for (name in df$names) {
        if (name=="itemid") {
            counter= counter+1
        }
        splitting_array <- c(splitting_array, counter)
    }
    
    x<-split(df, splitting_array)
    
    for (i in 1:length(x)) {
        temp_df<-x[[i]]
        x[[i]]<-filter(temp_df, names=="eventtime" | names=="current_moodid"
                       | names=="itemid" | names=="event" | names=="url")
        colnames(x[[i]])<-c("names", "values")
    }
    
    x <- x[2:length(x)]
    userid<-match(fileName, file_list)
    
    for (i in 1:length(x)) {
        x[[i]]<-rbind(x[[i]], data.frame(names="userid", values=as.character(userid)))
    }
    return (x)
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
