from __future__ import absolute_import 


from views import BaseHandler
from tornado import web

class IndexHandler(BaseHandler):
	
	@web.authenticated
	def get(self):
		self.render("index.html")

