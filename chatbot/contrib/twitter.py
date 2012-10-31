import re
import urllib2
import json
from chatbot.chat import ChatResponse
from chatbot.contrib.base import Feature

class TweetReader(Feature):
	match_re = r'http[s]?://twitter.com/(?P<user_name>[^/]+)/status/(?P<status_id>[0-9]+)/?'
	api_url_pattern = 'http://api.twitter.com/1/statuses/show.json?id=%s&include_entities=true'

	def handles_query(self, query):
		if re.search(self.match_re, query.query):
			return True

	def handle_query(self, query):
		search_results = re.findall(self.match_re, query.query)
		response_content = ""
		for result in search_results:
			user_name = result[0]
			tweet_id = result[1]
			try:
				page = urllib2.urlopen(self.api_url_pattern % tweet_id)
			except urllib2.URLError:
				response_content = response_content + "Error accessing tweet from %s." % user_name + "\n"
				continue
			data = json.load(page)
			response_content = "%s (%s): %s" % (data['user']['name'], data['user']['screen_name'], data['text']) + "\n"
		return ChatResponse(str(response_content))