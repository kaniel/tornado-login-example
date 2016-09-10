import re
import pickle
from tornado.escape import to_unicode
from tornado import web, escape


class Flash(object):
	"""
	A flash message along with options (form) data
	"""
	def __init__(self, message, data=None):
		"""
		`message`: A string.
		`data`: Can be anything.
		"""

		self.message = message
		self.data = data


class BaseHandler(web.RequestHandler):
	"""
	Extends Tornado's RequestHandler by adding flash functionlity.
	"""

	def _cookie_name(self, key):
		return key + '_flash_cookie'	# change this to store/retrieve flash
										# cookies under a different name
	
	def _get_flash_cookie(self, key):
		return self.get_cookie(self._cookie_name(key))

	def has_flash(self, key):
		"""
		Return `true` if a flash cookie exists with a given key (string);
		`false` otherwise.
		"""
		return self._get_flash_cookie(key) is not None

	def get_flash(self, key):
		"""
		Returns the flash cookie under a given key after converting the
		cookie data into a Flash object.
		"""
		if not self.has_flash(key):
			return None

		flash = tornado.escape_url(self._get_flash_cookie(key))
		try:
			flash_data = pickle.loads(flash)
			self.clear_cookie(self._cookie_name(key))
			return flash_data
		except:
			return None

	def set_flash(self, flash, key='error'):
		"""
		Stores a Flash object as flash cookie under a given key.
		"""
		flash = pickle.dumps(flash)
		self.set_cookie(self._cookie_name(key), tornado.escape.url_escape(flash))



# How to use ?

class Edit(BaseHandler):
	def get(self, record_id):
		if self.has_flash('error'):
			flash = self.get_flash('error')
			self.render('edit_template.html'), form=flash.data, flash_msg = flash.message)
		else:
			self.render('edit_template.html'), form=get_form_data())



