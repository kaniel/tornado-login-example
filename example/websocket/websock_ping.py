import ujson
from tornado.websocket import WebSocketHandler
import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler

class MyWebSocketHandler(WebSocketHandler):
	"""
	"""
	#override
	def prepare(self):
		pass

	#override
	def check_origin(self, origin):
		return True

	
	#override
	def open(self):
		#logger.debug('A client has connected ...')
		print 'A client has connected ...'

	
	#override
	def on_message(self, msg):
		#logger.debug(msg)
		if msg == 'x':		# ping ...
			self.write_message('you said:%s' % msg)
		else:
			self.write_message('you said:%s' % msg)
	
	def on_close(self):
		#logger.debug ..
		#for mid in matches.keys():
		#	if matches[mid].nodes.has_key(str(id(self))):
		#		matches[mid].nodes.pop(str(id(self)))
		self.close()

	
	#override
	def write_message(self, msg):
		if not self.stream.closed():
			super(MyWebSocketHandler, self).write_message(msg)
		else:
			self.on_connection_close()

def make_app():
	return tornado.web.Application([
			(r'/ws',MyWebSocketHandler),
			],
			debug=True)

if __name__ == '__main__':
	app = make_app()
	app.listen(9909)
	tornado.ioloop.IOLoop.current().start()
