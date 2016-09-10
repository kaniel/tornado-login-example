from __future__ import absolute_import

import os

from tornado.web import StaticFileHandler, url


#from api import post_order
#from api import get_order

from views import auth
from views import main
from views import dashboard
from views.error import NotFoundErrorHandler
from utils import gen_cookie_secret


settings = dict(
		template_path = os.path.join(os.path.dirname(__file__), "templates"),
		static_path = os.path.join(os.path.dirname(__file__), "static"),
		cookie_secret=gen_cookie_secret(),
		static_url_prefix='/static/',
		login_url='/login',
		debug=True,
)

handlers = [

	# Main
	url(r"/",main.IndexHandler),
	url(r"/adduser",main.AddUserHandler),
	
	# Dash
	url(r"/dashboard", dashboard.DashIndexHandler),
	url(r"/dashboard/addstudent", dashboard.DashAddStudentHandler),
	url(r"/dashboard/studentinfo", dashboard.StudentInfoHandler),
	
	# Auth
	(r"/login", auth.LoginHandler),
	url(r"/logout",auth.LogoutHandler, name='logout'),

	# Static
	(r"/static/(.*)", StaticFileHandler,
	 {"path":settings['static_path']}),

	# Error
	(r".*", NotFoundErrorHandler),
]
