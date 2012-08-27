import re
import urllib2
from chatbot.chat import ChatResponse

class PyPIFeature(object):
	"""
	Handles any query that includes pypi://<package_name> one or more times
	in the content. Responds with the pypi url for each instance.
	
	"""
	
	MATCHES_STRING = r'pypi://([\w-]*)'
	INDEX_URL = "http://pypi.python.org/pypi/%s/"

	allow_continuation = True
	
	def handles_query(self, query):
		if re.search(self.MATCHES_STRING, query.query):
			return True
		return False
	
	def handle_query(self, query):
		target = query.user['raw'] if query.private else query.channel
		search_results = re.findall(self.MATCHES_STRING, query.query)
		response_content = ""
		for package_name in search_results:
			response_content = response_content + self._get_pypi_url(package_name) + "\n"
		return ChatResponse(response_content, target=target)
	
	def _get_pypi_url(self, package_name):
		# TODO: make this correct package names somehow (e.g., 'django' to 'Django', 'django-compressor' to 'django_compressor')
		try:
			page = urllib2.urlopen(self.INDEX_URL % package_name)
			return self.INDEX_URL % package_name
		except:
			return "No package `%s` found on PyPI" % package_name