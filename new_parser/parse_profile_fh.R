# Parse One profile to get

"user ID --> alphabetical order as data is processed
mood ID --> current_moodid
post ID --> itemid
post Date --> eventtime
post content (the text itself) --> event"

library(dplyr)
library(XML)

fileUrl<-"zzzzzzzzzzzzzzz.xml"
doc = xmlParse(fileUrl)

userID = getNodeSet(doc,"//post/user")
moodID = getNodeSet(doc,"//post/current_moodid")
postID = getNodeSet(doc,"//post/ditemid/int")
postDate = getNodeSet(doc,"//post/eventtime/string")
postContent = getNodeSet(doc,"//post/event/string")

userID<-sapply(userID,xmlValue)
moodID<-sapply(moodID,xmlValue)
postID<-sapply(postID,xmlValue)
postDate<-sapply(postDate,xmlValue)
postContent<-sapply(postContent,xmlValue)