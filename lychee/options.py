from __future__ import absolute_import

import types

from tornado.options import define
from tornado.options import options


DEFAULT_CONFIG_FILE = 'lycheeconfig.py'


define("port", default=5555,
		help="run on the given port" ,type=int)

define("address", default='',
		help="run on the given address" ,type=str)

define("unix_socket", default='',
		help="path to unix socket to bind" ,type=str)

define("xheaders", default=False,
		help="enable support for the 'X-Real-Ip' and 'X-Scheme' headers." ,type=bool)

define("debug", default=True,
		help="run in debug mode" ,type=bool)

define("ca_certs", default=None,
		help="SSL certificate authority (CA) file" ,type=str)

define("certfile", default=None,
		help="SSL certificate file" ,type=str)

define("keyfile", default=None,
		help="SSL key file" ,type=str)

define("cookie_secret", default=None,
		help="secure cookie secret" ,type=str)


default_options = options
