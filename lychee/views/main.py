from __future__ import absolute_import 


from views import BaseHandler
from tornado import web

class IndexHandler(BaseHandler):

	def get(self):
		self.render("index.html")

class AddUserHandler(BaseHandler):

	@web.authenticated
	def get(self):
		self.render("adduser.html")

