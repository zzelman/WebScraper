import urllib2
from bs4 import BeautifulSoup

thread_url = 'http://boards.4chan.org/a/thread/113940628/what-the-actual-fuck-am-i-reading-did-the-mangaka'
soup_all = BeautifulSoup(urllib2.urlopen(thread_url).read())

# OP post
for hit_all in soup_all.find_all(attrs={'class' : 'post op'}):
	# image
	div = hit_all.find('div', {'class' : 'file'})
	if div:
		fileText = div.find('div', {'class' : 'fileText'})
		imgLink = fileText.find('a')
		print imgLink.get('href')

	# Post text
	blockquote = hit_all.find('blockquote')
	if blockquote:
		print blockquote.text
	print '\n'

# RE post
for hit_all in soup_all.find_all(attrs={'class' : 'post reply'}):
	# image
	div = hit_all.find('div', {'class' : 'file'})
	if div:
		fileText = div.find('div', {'class' : 'fileText'})
		imgLink = fileText.find('a')
		print "http:" + imgLink.get('href')

	# Post text w/ optional quote link
	blockquote = hit_all.find('blockquote')
	quote = blockquote.findAll('a')
	if quote:
		for q in quote:
			print q.text
		blockquote_text = blockquote.text
		for q in quote:
			blockquote_text = blockquote_text.replace(q.text, '')
		print blockquote_text
	else:
		print blockquote.text
	print '\n'
