import datetime

def char_count(lst):
	count = 0
	for element in lst:
		count += len(element)
		print(len(element))
	return count

def time_passed(member, hours):
	days = (datetime.datetime.now() - member.joined_at).days*24
	secs = (datetime.datetime.now() - member.joined_at).seconds/3600
	if int(days+secs) >= 3: return True
	else: return False