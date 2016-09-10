import urllib
from tornado import httpclient

def show(resp):
	print resp.body


def test ():
	url = "http://www.douban.com/search/"
	
	data = {}
	
	data['title']='fury'
	
	post_data = urllib.urlencode(data)
	
	client = httpclient.AsyncHTTPClient()
	
	resp = yield client.fetch(url ,method="POST", body=post_data)
	
	show(resp)
	
