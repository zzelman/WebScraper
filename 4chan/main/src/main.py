import sys
import urllib2
import types
import unicodedata

from threading import Thread
from bs4 import BeautifulSoup
from time import gmtime, strftime

from thread_4chan import Thread_4chan
from post_4chan import Post_4chan

url_4chan = 'http://www.4chan.org'
url_boardsRoot = 'http://boards.4chan.org/'

# usage within sys.argv
imgOnly = False
gen 	= False
single 	= False
echo 	= False
titles	= False
if 'img' in sys.argv:
	imgOnly = True
if 'gen' in sys.argv:
	gen = True
if 'single' in sys.argv:
	single = True
if 'echo' in sys.argv:
	echo = True
if 'title' in sys.argv:
	titles = True
if len(sys.argv) < 2:
	usage()
	sys.exit()

# argv checking
if single and gen:
	usage()
	sys.exit()


'''
'''
def usage():
	print "Usage:"
	print "     python " + sys.argv[0] + " [bot.config] <args>"
	print "     args:"
	print "          img     - find image links only"
	print "          gen     - generate the config file (defaults to all 4chan boards)"
	print "          single  - config file is treated as having thread urls (not board urls)"
	print "          echo    - print/dump the findings"
	print "          title   - find only the titles of threads"


'''
'''
def main():
	# generate a config file with ALL boards from 4chan
	if gen:
		generateConfig(sys.argv[1])

	# pull boards from config file to search
	board_list = parseConfig(sys.argv[1])

	# to increase efficancy, threading can be enabled
# 	threads_max = 5
# 	runThreads(board_list, threads_max)

	# sequentially step through the requested boards & collect data
	if single:
		threads_data = []
		for t in board_list:
			threads_data.append(Thread_4chan(t, strftime("%Y-%m-%d %H:%M:%S", gmtime()), parseSingleThread(t)))

		if echo:
			for thread in threads_data:
				if imgOnly:
					printImages(thread)
				else:
					printThread(thread)
				print
	else:
		threads_data = runSequentially(board_list)

		if echo:
			# print what you find
			for key in threads_data:
				print '>>>>>> ' + key + ' <<<<<<'
				thread_list = threads_data[key]
				for thread in thread_list:
					if imgOnly:
						printImages(thread)
					else:
						printThread(thread)
					print
				print "\n========================================\n"


'''
'''
def generateConfig(fileName):
	try:
		soup = BeautifulSoup(urllib2.urlopen(url_4chan).read())
	except:
		print "urllib2.urlopen exception on: " + url_4chan
		raise
	with open(fileName, 'w') as f:
		for link in soup.find_all('a'):
			text = link.get('href')
			if not 'thread' in str(text):
				if 'boards.4chan.org' in str(text):
					f.write('http:' + str(text) + '\n')


'''
'''
def parseConfig(fileName):
	boards = []
	with open(fileName, 'r') as f:
		for line in f:
			boards.append(line.rstrip())
	return boards


'''
'''
def runThreads(board_list, threads_max):
	threads = []
	for board in board_list:
		t = Thread(target = parseSingleThread, args = (board, ))
		threads.append(t)
	threads_current = 0
	# TODO: algorithum to kick off a finite amount of threads
	# 		at once and then sequentially re-add them as they finish
	# 		to not bog down the system


'''
'''
def runSequentially(boards_list):
	threads_total = []
	for b in boards_list:
		board_url = b
		boardChar = board_url[len(url_boardsRoot):-1]
		try :
			read = urllib2.urlopen(board_url).read()
		except:
			print "urllib2.urlopen exception on: " + board_url
			continue
		boardsSoup = BeautifulSoup(read)
		for link in boardsSoup.find_all('a'):
			text = link.get('href')
			if text[1:-1] not in boards_list:
				if text.startswith('thread') and text.count('/') == 2:
					threads_total.append(url_boardsRoot + boardChar + '/' + text)
# 					threads_total.append('/' + b + '/' + text)
	return findThreadData(threads_total)


'''
	Data Structure format returned:
		{'board_char' : [thread obj found in board],
		 'board_char' : [thread obj found in board]}
'''
def findThreadData(threads_total):
	threads_data = {}
	for t in threads_total:
		l = len(url_boardsRoot)
		board_char = t[l:t.find('/', l)]
		thread_object = Thread_4chan(t, strftime("%Y-%m-%d %H:%M:%S", gmtime()), parseSingleThread(t))
		if board_char in threads_data:
			threads_data[board_char].append(thread_object)
		else:
			threads_data[board_char] = [thread_object]
	return threads_data



'''
'''
def parseSingleThread(board_url):
	thread_url = board_url
	try:
		soup_all = BeautifulSoup(urllib2.urlopen(thread_url).read())
	except:
		print "urllib2.urlopen exception on: " + thread_url
		return []

	post_data = []

	# OP post
	for hit_all in soup_all.find_all(attrs={'class' : 'post op'}):
		# data extracted
		reQuote = []
		imgLink = None
		postText = None

		# image
		div = hit_all.find('div', {'class' : 'file'})
		if div:
			fileText = div.find('div', {'class' : 'fileText'})
			if fileText:
				img = fileText.find('a')
				imgLink = "http:" + img.get('href')

		# Post text
		blockquote = hit_all.find('blockquote')
		if blockquote:
			postText = parseBlockquote(blockquote)

		# Create object
		post_data.append(Post_4chan(reQuote, imgLink, postText))

	# RE post
	for hit_all in soup_all.find_all(attrs={'class' : 'post reply'}):
		# data extracted
		reQuote = []
		imgLink = None
		postText = None

		# image
		div = hit_all.find('div', {'class' : 'file'})
		if div:
			fileText = div.find('div', {'class' : 'fileText'})
			if fileText:
				img = fileText.find('a')
				imgLink = "http:" + img.get('href')

		# Post text w/ optional quote link
		blockquote = hit_all.find('blockquote')
		quote = blockquote.findAll('a')
		if quote:
			for q in quote:
				reQuote.append(q.text)
			blockquote_text = blockquote.text
			for q in quote:
				blockquote_text = blockquote_text.replace(q.text, '')
			postText = parseBlockquote(blockquote)
		else:
			postText = parseBlockquote(blockquote)

		# Create object
		post_data.append(Post_4chan(reQuote, imgLink, postText))

	return post_data


'''
'''
def parseBlockquote(blockquote):
	text = ''
	for elem in blockquote.recursiveChildGenerator():
		if isinstance(elem, types.StringTypes):
			text += elem.strip()
		elif elem.name == 'br':
			text += '\n'
	return text


'''
'''
def printImages(thread):
	if titles:
		print thread.thread_url
	else:
		print thread.thread_url
		print thread.read_time
		for post in thread.thread_data:
			if post.imgLink:
				print post.imgLink


'''
'''
def printThread(thread):
	if titles:
		print thread.thread_url
	else:
		print thread.thread_url
		print thread.read_time
		for post in thread.thread_data:
			printPost(post)


'''
'''
def printPost(post):
	if post.reQuote:
		for q in post.reQuote:
			print q
	if post.imgLink:
		print post.imgLink
	if post.postText:
		print unicodedata.normalize('NFKD', post.postText).encode('ascii','ignore')


'''
'''
if __name__ == "__main__":
# 	blockquote = BeautifulSoup('<blockquote class="postMessage" id="m113976861"><a href="#p113976697" class="quotelink">&gt;&gt;113976697</a><br><s>Things won&#039;t get better until you want them to.</s></blockquote>')
# 	print parseBlockquote(blockquote)

# 	url = 'http://boards.4chan.org/a/thread/113974193'
# 	t = parseSingleThread(url)
# 	for s in t:
# 		print str(s)
# 		print '##########################\n'
# 	print str(t[0]) + '\n'

# 	d = {'' : []}
# 	d['a'] = ['thread1', 'thread2']
# 	if 'a' in d:
# 		d['a'].append('thread3')
# 	print d.get('a')

	main()
