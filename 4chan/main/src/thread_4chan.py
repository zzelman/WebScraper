class Thread_4chan:
	'''
		Constructor for this Thread_4chan object

		ARGS:
			thread_url: 	The url that this thread occored at
			read_time: 		str representation of the time that this thread was parsed at
			thread_data: 	a list of Post_4chan objects
	'''
	def __init__(self, thread_url, read_time, thread_data):
		self.thread_url 	= thread_url
		self.read_time 		= read_time
		self.thread_data 	= thread_data
