from __future__ import absolute_import

import json
import functools
import re





from views import BaseHandler


class LoginHandler(BaseHandler):
	def get(self):
		self.write("<h1>Login </h1>")


class LogoutHandler(BaseHandler):
	def get(self):
		self.clear_cookie('user')
		self.render('404.html', message='Successfulyy logged out!')
