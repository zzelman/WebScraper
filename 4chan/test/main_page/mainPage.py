import urllib2
from bs4 import BeautifulSoup
import sys

url_base = 'http://www.4chan.org'
url_read = urllib2.urlopen(url_base).read()
soup = BeautifulSoup(url_read)

#################################
# print soup.get_text()
#################################

#################################
# for link in soup.find_all('a'):
# 	text = link.get('href')
# 	if not 'thread' in str(text):
# 		if 'boards.4chan.org' in str(text):
# 			print text
#################################

#################################
import re

boards_list = []
for link in soup.find_all('a'):
	text = link.get('href')
	if not 'thread' in str(text):
		if 'boards.4chan.org' in str(text):
			boards_list.append(text[len("//boards.4chan.org/"):-1])
# print boards_list

url_boardsRoot = 'http://boards.4chan.org/'
url_boardsList = []
for b in boards_list:
	text = url_boardsRoot + b + '/'
	url_boardsList.append(text)
# print url_boardsList

threads_total = []
images_total = []
for b in boards_list:
	board_url = url_boardsRoot + b + '/'
	read = urllib2.urlopen(board_url).read()
	boardsSoup = BeautifulSoup(read)
	for link in boardsSoup.find_all('a'):
		text = link.get('href')
		if text[1:-1] not in boards_list:
			if text.startswith('//i.'):
				images_total.append('http:' + text)
# 				images_total.append(text)
			elif text.startswith('thread') and text.count('/') == 2:
				threads_total.append(url_boardsRoot + b + '/' + text)
# 				threads_total.append('/' + b + '/' + text)

with open('threads.txt', 'w') as f:
	for s in threads_total:
		f.write(s + '\n')
with open('images.txt', 'w') as f:
	for s in images_total:
		f.write(s + '\n')

#################################
