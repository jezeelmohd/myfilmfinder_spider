import os
import random
from scrapy.conf import settings
from scrapy import log
import base64

class ProxyMiddleware(object):
	def process_request(self, request, spider):
		#ua  = random.choice(settings.get('PROXY_LIST'))
		request.meta['proxy'] = 'http://uk.proxymesh.com:31280'
		"""
		proxy_user_pass = "USERNAME:PASSWORD"
		# setup basic authentication for the proxy
		encoded_user_pass = base64.encodestring(proxy_user_pass)
		request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
		"""
class RandomUserAgentMiddleware(object):
	def process_request(self, request, spider):
		ua  = random.choice(settings.get('USER_AGENT_LIST'))
		if ua:
		   request.headers.setdefault('User-Agent', ua)
		   log.msg("USER AGENT IS: "+ua, level=log.INFO)
