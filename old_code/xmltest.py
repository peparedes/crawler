from lxml import etree
import queue 
# make a dictionary of the url and the post/comment that it corresponds to
# print all posts found on the user's page on a file 
s = set()
filename = 'hemoleleis23.xml'
username = filename[:-4]

# for each post returns a list of list where each element in that list 
# contains all the words in one sentence in that post
def bag_of_words(post):
    words = []
    sentences = post.split(".")
    for i in sentences:
        words.append(i.split())
    return words

def get_posts(filename):
    with open(filename ,'rt') as f:
         tree = etree.parse(f)         
    posts_count = 0
    url_count = 0 
    time_count = 0

    urls = queue.Queue()
    posts = queue.Queue()
    time = queue.Queue()
    mood = queue.Queue()
    previous_tag = ''

    for i in list(tree.iter()):
        if i.tag == 'string' and previous_tag == 'event':
            if i.text != None:
                posts.put(i.text)
                posts_count += 1

        if i.tag == 'string' and previous_tag == 'url':
            if i.text != None and url_count == posts_count - 1:
                urls.put(i.text)
                url_count += 1
                
        if i.tag == 'string' and previous_tag == 'eventtime':
            if i.text != None and time_count == posts_count - 1:
                timestamp = i.text
                time.put(timestamp)
                time_count += 1
        previous_tag = i.tag

        # some posts have moods, perhaps I can get those too. 
        # I will have to put a dummy value if there is no mood
        # if i.tag == 'int' and previous_tag == 'current_moodid':
        #   if i.text != None:
        #       mood.put(i.text)
    return [posts, urls, time]
        

def to_file(lst):
    posts = lst[0]
    urls = lst[1]
    time = lst[2]
    bag = {}
    while (not posts.empty()):
        timestamp = time.get()
        filename = timestamp + "_" + username + ".txt"
        with  open(filename, 'w') as f:
            post = posts.get() 
            bag[filename] = bag_of_words(post)
            f.write(post + "\n")
            f.write(urls.get() + "\n")
            f.write(timestamp + "\n")
    return bag_of_words

bag = to_file(get_posts(filename))

# old code
# previous_tag = ''
# file_to_bag = {}
# for i in list(tree.iter()):
#   if i.tag == 'string' and previous_tag == 'event':
#       post = i.text
#   if i.tag == 'string' and previous_tag == 'eventtime':
#       timestamp = i.text
#       filename = timestamp + "_" + username + ".txt"
#       #write the post to a file with the username and timestamp on it 
#       with open(filename, 'w') as f:
#           f.write(post)
#       # using a dictionary, it links each post with the bag_of_words that we created
#       file_to_bag[filename] = bag_of_words(post)
#   previous_tag = i.tag





