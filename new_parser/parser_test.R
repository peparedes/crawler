"Script that puts all the information from an xml document in a data frame
that contains 2 columns:
-- names: string containing the information label. e.g. event or logtime 
or eventtime

-- values: string that contains the information relevant. e.g. all posts are
the values to a row with the name event (there is a subtle point that needs to be
resolved here)
"
library(XML)
library(dplyr)

#Open a raw file from those downloaded so far
fileUrl<- "downloads/ghost-luc.xml"
doc = xmlParse(fileUrl)
#Get all the contents of name and value tags that are contained in a member tag
#that exist in the doc
values = getNodeSet(doc, "//member/value")
names = getNodeSet(doc, "//member/name")

#get only the contents of the retrieved tags
values<-sapply(values, xmlValue)
names<-sapply(names, xmlValue)

#Put the retrieved names and their values in a dataframe
df<- data.frame(names=names, values=values)

#as an example retrieve all the mood ids contained in the document
mood<-filter(df, names=="current_moodid")

# code to show the dataframe
View(df)
View(mood)