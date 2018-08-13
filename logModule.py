import time

class logModule:
	def __init__(self):
		self.init = 1
	def info(self,act):
		print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+ ' Info: ' + act)
	def debug(self,act):
		print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+ ' Debug: ' + act)
	def error(self,act):
		print (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())+ ' Error: ' + act)

#logger = logModule()
#logger.info('test')
#logger.debug('test')
#logger.error('test')
