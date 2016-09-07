from __future__ import absolute_import


import uuid
import base64
import os.path

def gen_cookie_secret():
	return base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
