from __future__ import absolute_import


from views import BaseHandler
from tornado import web

class DashIndexHandler(BaseHandler):
	@web.authenticated
	def get(self):
		self.render("dashboard/index.html")

class DashAddStudentHandler(BaseHandler):
	@web.authenticated
	def get(self):
		self.render("dashboard/add_student.html")
	
	@web.authenticated
	def post(self):
		self.render("dashboard/add_student.html")

class StudentInfoHandler(BaseHandler):
	@web.authenticated
	def get(self):
		self.render("dashboard/student_info.html")
