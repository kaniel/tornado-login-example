from __future__ import absolute_import

import logging

from functools import partial
#from concurrent.futures import ThreadPoolExecutor 
import tornado.web
from tornado import ioloop
from tornado.httpserver import HTTPServer


from api import control
from urls import handlers ,settings
from options import default_options
from jinja2 import Environment, FileSystemLoader


logger = logging.getLogger(__name__)


class JinjaApplicationMixin(object):
	def __init__(self, *args, **settings):
		super(JinjaApplicationMixin, self).__init__(*args, **settings)
		if "template_path" not in settings:
			return 

		if "template_loader" in settings:
			loader = settings['template_loader']
		else:
			loader = FileSystemLoader(settings['template_path'])

		if 'debug' in settings:
			auto_reload = settings['debug']
		else:
			auto_reload = False

		autoescape = bool(settings.get('autoescape', False))
		self.jinja_env = Environment(
				loader = loader,
				auto_reload = auto_reload,
				autoescape = autoescape,)


class Lychee(JinjaApplicationMixin ,tornado.web.Application):
	#pool_executor_cls = ThreadPoolExecutor
	max_workers = 4

	def __init__(self, options=None, io_loop=None, **kwargs):
		kwargs.update(handlers=handlers)
		super(Lychee, self).__init__(**kwargs)
		self.options = options or default_options
		self.io_loop = io_loop or ioloop.IOLoop.instance()
		self.ssl_options = kwargs.get('ssl_options', None)

		self.started = False

	def start(self):
		#self.pool = self.pool_executor_cls(max_workers=self.max_workers)
		if not self.options.unix_socket:
			self.listen(self.options.port, address=self.options.address,
						ssl_options=self.ssl_options,xheaders=self.options.xheaders)

		else:
			from tornado.netutil import bind_unix_socket
			server = HTTPServer(self)
			socket = bind_unix_socket(self.options.unix_socket)
			server.add_socket(socket)

#self.io_loop.add_future(
			# TODO ...
#				)

		self.started = True
		self.io_loop.start()


	def stop(self):
		if self.started:
			#self.pool.stutdown(wait=False)
			self.started = False

	#def delay(self, method, *args, **kwargs):
	#	return self.pool.submit(partial(method, *args, **kwargs))


			


if __name__ == '__main__':
	app = Lychee(**settings)
	app.start()
