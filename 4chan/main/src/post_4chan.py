class Post_4chan:

	'''
		Constructor for this class

		ARGS:
			reQuote: 	a list of strs that point to a previous post
			imgLink: 	the link to the image that accompanies this post (if one exists)
			postText: 	the text contained within this post
	'''
	def __init__(self, reQuote, imgLink, postText):
		self.reQuote 	= reQuote
		self.imgLink 	= imgLink
		self.postText 	= postText
