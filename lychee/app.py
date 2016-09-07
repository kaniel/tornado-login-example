from __future__ import absolute_import

import logging

from functools import partial
#from concurrent.futures import ThreadPoolExecutor 
import tornado.web
from tornado import ioloop
from tornado.httpserver import HTTPServer


from api import control
from urls import handlers
from options import default_options

logger = logging.getLogger(__name__)


class Lychee(tornado.web.Application):
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
	app = Lychee()
	app.start()
