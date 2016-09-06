import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		if not self.get_cookie("mycookie"):
			self.set_cookie("mycookie","myvalue")
		else:
			self.write("Your cookie was set!")

class CheckCookieHandler(tornado.web.RequestHandler):
	def get(self):
		self.set_cookie("newcookie","newcookie")
		self.write(self.get_cookie("mycookie"))


def make_app():
	return tornado.web.Application([
			(r"/",MainHandler),
			(r"/cc",CheckCookieHandler),
			])

if __name__ == '__main__':
	app = make_app()
	app.listen(8800)
	tornado.ioloop.IOLoop.current().start()
