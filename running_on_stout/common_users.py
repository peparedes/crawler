#Checks common users between old and new data
import re

f1 = open("name2id_0")
f2 = open("new_usernames.txt")

txt1 = f1.read()
txt2 = f2.read()

old_users = re.split('\n',txt1)
old_users = [i.split('|')[-1] for i in old_users]

new_users = re.split('\n',txt2)

print("The number of new usernames is:", len(new_users)-len(set(new_users).intersection(set(old_users))))
