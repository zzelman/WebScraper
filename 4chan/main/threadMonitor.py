import sys
import unicodedata

from main import parseSingleThread
from thread_4chan import Thread_4chan
from post_4chan import Post_4chan


# parse cli
imgOnly = False
echo 	= False
if 'img' in sys.argv:
	imgOnly = True
if 'echo' in sys.argv:
	echo = True
if len(sys.argv) < 3:
	usage()
	sys.exit()


# globals
outputFile_name = sys.argv[2]
outputFile = open(outputFile_name, 'w')
url_thread = sys.argv[1]
thread_data = []



'''
'''
def usage():
	print "Usage:"
	print "     python " + sys.argv[0] + " [4chan thread url] [output file] <args>"
	print "          img     - find image links only"
	print "          echo    - print/dump the findings"



'''
'''
def main():
	data = parseSingleThread(url_thread)
	for p in data:
		if not postExists(p):
			thread_data.append(p)
	printData()


'''
	checks if the post exists within global thread_data
	RETURNS:
		True if post exists
		False if post does not exist
'''
def postExists(post):
	for p in thread_data:
		if p.imgLink:
			if p.imgLink is post.imgLink:
				return True
		if p.postText:
			if p.postText is post.postText:
				return True
	return False


'''
'''
def printData():
	if imgOnly:
		printImages()
	else:
		printThread()


'''
'''
def printImages():
	for p in thread_data:
		if p.imgLink:
			outputFile.write(p.imgLink + '\n')
			if echo:
				print p.imgLink


'''
'''
def printThread():
	outputFile.write(url_thread + '\n')
	if echo:
		print url_thread
	for post in thread_data:
		if post.reQuote:
			for q in post.reQuote:
				outputFile.write(q + '\n')
				if echo:
					print q
		if post.imgLink:
			outputFile.write(post.imgLink + '\n')
			if echo:
				print post.imgLink
		if post.postText:
			text = unicodedata.normalize('NFKD', post.postText).encode('ascii','ignore')
			outputFile.write(text + '\n')
			if echo:
				print text


'''
'''
if __name__ == "__main__":
	main()
outputFile.close()
