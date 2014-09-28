import sys
import types
import operator

from lib import *


'''
'''
def main():
	configFile = "hitCount.bot.config"
	generateConfig(configFile)
	board_list = parseConfig(configFile)
	data_all = runSequentially(board_list)

	search_str = sys.argv[1]
	thread_hitcount = {}
	for board_char, thread_list in data_all.iteritems():
		for thread in thread_list:
			thread_hitcount[thread] = countHit(thread, search_str)

# 	thread_hitcount_sorted = thread_hitcount
	thread_hitcount_sorted = sorted(thread_hitcount.items(), key=operator.itemgetter(1), reverse=True)
	for i in thread_hitcount_sorted:
# 		print "val = " + str(i) + ", key = " + str(t.thread_url)
		if i[1] > 0:
			print str(i[1]) + "\t\t" + str(i[0].thread_url)
			downloadImages_obj(i[0])

# 	for t in thread_hitcount_sorted:
# 		print t.thread_url

'''
'''
def countHit(thread, search_str):
	count = 0
	for post in thread.thread_data:
		count += countHit_post(post, search_str)
	return count


'''
'''
def countHit_post(post, search_str):
	if post.postText:
		s = post.postText
		if isinstance(s, unicode):
			s = unicodedata.normalize('NFKD', post.postText).encode('ascii','ignore')
		if s.lower().count(search_str) != 0:
			return 1
		else:
			return 0
	return 0


if __name__ == "__main__":
	main()
