import re
import urllib2
from chatbot.chat import ChatResponse


class BaseURLFeature(object):
	allow_continuation = True
	
	def __init__(self):
		if not hasattr(self, 'request_re'):
			raise NotImplementedError('`request_re` must be defined on %s.' % self.__class__.__name__)
	
	def handles_query(self, query):
		if re.search(self.request_re, query.query):
			return True
	
	def handle_query(self, query):
		search_results = re.findall(self.request_re, query.query)
		response_content = ""
		for keyword in search_results:
			url = self.get_url(keyword)
			if url:
				response_content = response_content + url + "\n"
			else:
				response_content = response_content + "URL not found for %s" % keyword + "\n"
		return ChatResponse(response_content)
	
	def get_url(self, keyword):
		"Returns either a URL associated with the keyword, or false if error."
		if not hasattr(self, 'url_format'):
			raise NotImplementedError('Attribute `url_format` or method `get_url` must be defined on %s.' % self.__class__.__name__)
		url = self.url_format % keyword
		try:
			page = urllib2.urlopen(url)
			return url
		except:
			return False


class PyPIFeature(BaseURLFeature):
	request_re = r"pypi:([\w\-_]*)"
	url_format = r"http://pypi.python.org/pypi/%s/"


class WikipediaFeature(BaseURLFeature):
	request_re = r"wiki:([\w\-_]*)"
	url_format = r"http://en.wikipedia.org/wiki/%s"
	
	def get_url(self, keyword):
		"""
		Wikipedia blocks bots from requesting URLs, so this just returns the
		url without checking it.
		"""
		return self.url_format % keyword


class DictionaryFeature(BaseURLFeature):
	request_re = r"word:([\w\-_']*)"
	url_format = r"http://dictionary.reference.com/browse/%s"