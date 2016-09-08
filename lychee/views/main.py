from __future__ import absolute_import 


from views import BaseHandler
from tornado import web

class IndexHandler(BaseHandler):
	
	def get(self):
		self.render("index.html")

