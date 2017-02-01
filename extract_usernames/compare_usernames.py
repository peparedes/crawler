old_user_file = open("../running_on_stout/name2id_0", "r")
old_users = old_user_file.readlines()

parsed_user_file = open("./new_usernames.txt", "r")
parsed_users = parsed_user_file.readlines()

process_ = lambda x: x.split('|')[1][:-2]
process = lambda x: x[:-2]
old_users = list(map(process_, old_users))
parsed_users = list(map(process, parsed_users))


new_users = []
print(len(old_users))
for user in parsed_users:
	if not user in old_users:
		new_users.append(user)

new_file = open('new_users_filtered.txt', 'w')
print(new_users)
for item in new_users:
  		print>>new_file, item

print(str(len(new_users)*100/len(parsed_users)) + "% of the downloaded usernames are new.")
