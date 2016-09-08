from __future__ import absolute_import

import tornado.web

from views import BaseHandler

class NotFoundErrorHandler(BaseHandler):
	def get(self):
#raise tornado.web.HTTPError(404)
		self.render("error/404.html")

	def post(self):
		raise tornado.web.HTTPError(404)
