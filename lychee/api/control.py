from tornado import gen


class ControlHandler(object):

	@classmethod
	@gen.coroutine
	def update_workers(cls, app, workname=None):
		pass
