from lxml import etree
import queue 
# make a dictionary of the url and the post/comment that it corresponds to
# print all posts found on the user's page on a file 
s = set()
filename = 'hemoleleis23.xml'
username = filename[:-4]

with open(filename ,'rt') as f:
   tree = etree.parse(f)

# for each post returns a list of list where each element in that list 
# contains all the words in one sentence in that post
def bag_of_words(post):
	words = []
	sentences = post.split(".")
	for i in sentences:
		words.append(i.split())
	return words

previous_tag = ''
file_to_bag = {}
for i in list(tree.iter()):
	if i.tag == 'string' and previous_tag == 'event':
		post = i.text
	if i.tag == 'string' and previous_tag == 'eventtime':
		timestamp = i.text
		filename = timestamp + "_" + username + ".txt"
		#write the post to a file with the username and timestamp on it 
		with open(filename, 'w') as f:
			f.write(post)
		# using a dictionary, it links each post with the bag_of_words that we created
		file_to_bag[filename] = bag_of_words(post)
	previous_tag = i.tag





