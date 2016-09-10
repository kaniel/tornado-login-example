import json
import tornado.ioloop
from tornado import web
from tornado import gen
from tornado import httpclient
import urllib

class MainHandler(web.RequestHandler):

	@web.asynchronous
	@gen.coroutine
	def get(self):
		url = "http://www.douban.com/search/"
		data = {}
		data['title'] = 'fury'
		post_data = urllib.urlencode(data)
		client = httpclient.AsyncHTTPClient()
		response = yield client.fetch(url , method="POST", body=post_data)
		self.on_response(response)


	def on_response(self, resp):
		body = json.loads(resp.body)
		if body == None:
			self.write('error')
		else:
			self.write(body)

		return 


def make_app():
	return web.Application([
			(r"/",MainHandler),
			])

if __name__ == '__main__':
	app = make_app()
	app.listen(8800)
	tornado.ioloop.IOLoop.current().start()
