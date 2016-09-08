from __future__ import absolute_import

import tornado
import tornado.web
from tornado import escape
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


class TemplateRendering(object):
	"""
		A simple class to hold methods for rendering templates.
	"""
	def render_template(self, template_name, **kwargs):
		template_dirs = []
		if self.settings.get('template_path', ''):
			template_dirs.append(self.settings['template_path'])
		env = Environment(loader=FileSystemLoader(template_dirs))

		try:
			template = env.get_template(template_name)
		except TemplateNotFound:
			raise TemplateNotFound(template_name)
		content = template.render(kwargs)
		return content

class JinjaHandlerMixin(object):
	def render_string(self, template_name, **context):
		self.require_setting("template_path", "render")
		default_context = {
			'handler':self,
			'request':self.request,
			'current_user':self.current_user,
			'static_url':self.static_url,
			'xsrf_form_html':self.xsrf_form_html,
			'reverse_url':self.reverse_url,
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


###	def render_html(self, template_name, **kwargs):
###		kwargs.update({
###				'settings':self.settings,
###				'STATIC_URL':self.settings.get('static_url_prefix','/static/'),
###				'request':self.request,
###				'current_user':self.current_user,
###				'xsrf_token':self.xsrf_token,
###				'xsrf_from_html':self.xsrf_from_html,
###				})
###		content = self.render_template(template_name, **kwargs)
###		self.write(content)
