from __future__ import absolute_import

import tornado
import tornado.web
from tornado import escape
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


class JinjaHandlerMixin(object):
	"""
		A simple class to hold methods for rendering templates.
	"""
	def render_string(self, template_name, **context):
		self.require_setting("template_path", "render")
		default_context = {
			'handler':self,
			'request':self.request,
			'current_user':self.current_user,
			'static_url':self.static_url,
			'xsrf_form_html':self.xsrf_form_html,
			'reverse_url':self.reverse_url,
			'flash_message':self.flash_message(),
		}

		escape_context = {
			'escape':escape.xhtml_escape,
			'xhtml_escape':escape.xhtml_escape,
			'url_escape':escape.url_escape,
			'json_encode':escape.json_encode,
			'squeeze':escape.squeeze,
			'linkify':escape.linkify,
		}
		context.update(default_context)
		context.update(escape_context)
		context.update(self.ui)	# Enabled tornado UI modules and methods
		template = self.application.jinja_env.get_template(
				template_name)
		return template.render(**context)
		

class BaseHandler(JinjaHandlerMixin, tornado.web.RequestHandler):
	
	def get_current_user(self):
		return self.get_secure_cookie("user")

	def flash_message(self):
		message =  self.get_secure_cookie("flash")
		if isinstance(message,str):
			self.clear_cookie("flash")
			return message
		else:
			return None

	def flash(self, message):
		self.set_secure_cookie("flash",message)
