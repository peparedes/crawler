from lxml import etree
import queue 
# make a dictionary of the url and the post/comment that it corresponds to
# print all posts found on the user's page on a file 
filename = 'hemoleleis23.xml'
username = filename[:-4]


def get_posts(filename):
    with open(filename ,'rt') as f:
         tree = etree.parse(f)         
    posts_count = 0
    url_count = 0 
    time_count = 0
    mood_count = 0

    urls = queue.Queue()
    posts = queue.Queue()
    time = queue.Queue()
    mood = queue.Queue()
    previous_tag = ''

    for i in list(tree.iter()):
        print(i.tag)
        # for some reason, it never gets into the if loops
        if i.tag == 'string' and previous_tag == 'event':
            if mood_count == posts_count - 1:
                mood.put(-1)
                mood_count += 1
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

        if i.tag == 'int' and previous_tag == 'current_moodid':
            mood.put(i.text)
            mood_count += 1
        previous_tag = i.tag

    return [posts, urls, time, mood]
        
# puts all posts + timestamp + url inside one file
def to_file(lst):
    posts = lst[0]
    urls = lst[1]
    time = lst[2]
    mood = lst[3]
    print(posts.qsize())
    print(urls.qsize())
    print(time.qsize())
    print(mood.qsize())

    if (mood.qsize() < posts.qsize()):
        mood.put(-1)

    timestamp = time.get()
    filename = username + ".txt"
    with  open(filename, 'w') as f:
        while posts.qsize() > 0:
            post = posts.get() 
            f.write(post + "\n")
            f.write(urls.get() + "\n")
            f.write(str(mood.get()) + "\n")
            f.write(timestamp + "\n\n")
