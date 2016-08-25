# Parse One profile to get

"user ID --> alphabetical order as data is processed
mood ID --> current_moodid
post ID --> itemid
post Date --> eventtime
post content (the text itself) --> event"

library(dplyr)
library(XML)

fileUrl<- "downloads/0-s-a-r-a-0.xml"
doc = xmlParse(fileUrl)

values = getNodeSet(doc, "//member/value")
names = getNodeSet(doc, "//member/name")

values<-sapply(values, xmlValue)
names<-sapply(names, xmlValue)

df<- data.frame(names=names, values=values)

#split the dataframe into an array of dataframes, one for each post

#make a factor containing all the different posts
counter<-0
splitting_array<-c()
for (name in df$names) {
    if (name=="itemid") {
        counter= counter+1
    }
    splitting_array <- c(splitting_array, counter)
}

# x is an array of data frames each of which contains info about 1 post in
# the users document
x<-split(df, splitting_array)

for (i in 1:length(x)) {
    temp_df<-x[[i]]
    x[[i]]<-filter(temp_df, names=="eventtime" | names=="current_moodid"
                   | names=="itemid" | names=="event")
    colnames(x[[i]])<-c("names", "values")
}

x <- x[2:length(x)]
file_list <- list.files("downloads")
sorted_file_list<-sort(file_list)

userid <-match(substring(fileUrl, 11), sorted_file_list)

for (i in 1:length(x)) {
    x[[i]]<-rbind(x[[i]], data.frame(names="userid", values=userid))
}
