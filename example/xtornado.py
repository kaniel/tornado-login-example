from tornado import web, gen, ioloop
from concurrent.futures import ThreadPoolExecutor 

class BaseApplication(web.Application):
	pool_executor_cls = ThreadPoolExecutor
	max_workers = 4
	
	def start(self):
		self.pool = self.pool_executor_cls(max_workers=self.max_workers)
		if not self.options.unix_socket:
			self.listen(self.options.port, address=self.options.address,
						ssl_options=self.ssl_options,xheaders=self.options.xheaders)

		else:
			from tornado.netutil import bind_unix_socket
			server = HTTPServer(self)
			socket = bind_unix_socket(self.options.unix_socket)
			server.add_socket(socket)

		self.io_loop.add_future(
				control.ControlHandler.update_workers(app=self),
				callback=lambda x : logger.debug(
					"Successfully updated worker cache"))

		self.started = True
		self.io_loop.start()
	
	
	def stop(self):
		if self.started:
			self.pool.stutdown(wait=False)
			self.started = False

	def add_handler(self, *args):
		self.add_handlers('*.$', [args])

# Declare my Base RequestHandler

class BaseRequestHandler(web.RequestHandler):
	_available_plugins = []
	_execute_plugins = []


	def initialize(self, route_path, exec_func):
		self.route_path = route_path
		self.exec_func = exec_func

	def prepare(self):
		"""
			1,Check client ip.
			2,Check system load balance.
			3,Install plugin to tornado application before handle request.
		"""
		ip = self.request.headers.get("X-Real-Ip", self.request.remote_ip)
		ip = self.request.headers.get("X-Forwarded-For", ip)
		ip = ip.split(',')[0].strip()
		self.request.remote_ip=ip

		# Check Load Balance
		# `thread_in_use` is Dict's type, `sum` will return the sume of dict.values()
		# Example `sample_dict = { 'a':1,'b':2,'c':3,'d':4}
		# `a,b,c,...` is interface name 
		# sample_dict.values() == [1,2,3,4]
		# Example `sum([1,2,3,4]) == 10`
		# the sum(thread_in_use.values) range between (1, 16)
		if 100 * sum(thread_in_use.values()) / MAX_THREADS < 90:
			pass	# 
		elif 100 * thread_in_use[self.route_path] / MAX_THREADS > 50:
			# if one client interface have range `8 thread` ...
			self.send_error(503)
			return 
		else:
			pass	# TODO: don't need to do anything ...

		# If you system if okay, the `_available_plugins` will be apply!
		for func in self._available_plugins:
			func(self)	#: Install plugin to tornado application

	@gen.coroutine
	def handle(self, *args, **kwargs):
		"""
		"""
		try:
			# TODO Will init the counter ???
			thread_in_use[self.route_path] += 1	# increatment counter 
			ret = yield thread_executor.submit(self.execute, *args, **kwargs)
			self.write(ret)
		except:
			pass

		finally:
			thread_in_use[self.route_path] -= 1

	post = handle
	get = handle
	put = handle
	delete = handle

	
	
	def execute(self, *args, **kwargs):
		"""
			execute the pre-install plugin before
			handle request.
		"""
		for func in self._execute_plugins:
			func(self, *args, **kwargs)
		return self.exec_func(self, *args, **kwargs)

	@classmethod
	def execute_plugin(cls):	# TODO --> def install_plugin(cls)
		def deco_func(func):
			cls._execute_plugins.append(func)
			return func
		return deco_func

	@classmethod
	def route(cls, route_path):
		def _route(function_name):
			cls.add_handler(route_path, cls,{'route_path':route_path,'exec_func':function_name})
			# TODO cls.add_handler(route_path, cls,{route_path:function_name})
			thread_in_use[route_path] = 0	#: TODO is thread safe??
			def __route(function_args):
				function_name(function_args)
			return __route
		return __route 


if __name__ == '__main__':
	app = BaseApplication(**settings)
	app.start()
