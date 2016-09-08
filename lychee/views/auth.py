from __future__ import absolute_import

import json
import functools
import re


sample_user = 'admin'
sample_password = 'admin'


from views import BaseHandler
from tornado import web

class LoginHandler(BaseHandler):
	def get(self):
		self.render("login.html")


	def post(self):
		username = self.get_argument('username','')
		password = self.get_argument('password','')
		
		if username == sample_user and password == sample_password:
			self.set_secure_cookie("user", str(username), expires_days=7)
			self.redirect('/')

		else:
			self.redirect('/login')



class LogoutHandler(BaseHandler):
	def get(self):
		self.clear_cookie('user')
		self.redirect('/')
	
	def post(self):
		self.clear_cookie('user')
		self.redirect('/')
