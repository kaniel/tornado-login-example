from __future__ import absolute_import 


from views import BaseHandler


class IndexHandler(BaseHandler):
	def get(self):
		self.write('<h1>Hello Tornado</h1>')

