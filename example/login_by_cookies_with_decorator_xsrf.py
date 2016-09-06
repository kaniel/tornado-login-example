import os
import tornado.ioloop
import tornado.web

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("user")

class MainHandler(BaseHandler):
	@tornado.web.authenticated
	def get(self):
		name = tornado.escape.xhtml_escape(self.current_user)
		self.write("Hello, " + name)

	
class LoginHandler(BaseHandler):
	def get(self):
		self.render("login.html")

	def post(self):
		self.set_secure_cookie("user", self.get_argument("name"))
		self.redirect("/")




def make_app():
	return tornado.web.Application([
			(r"/",MainHandler),
			(r"/login",LoginHandler),
			],
			cookie_secret="__TODO:_HARD_TO_GUESS_STRING",
			login_url="/login",
			xsrf_cookies=True,
			template_path = os.path.join(os.path.dirname(__file__),"templates"),
			)

if __name__ == '__main__':
	app = make_app()
	app.listen(8800)
	tornado.ioloop.IOLoop.current().start()
