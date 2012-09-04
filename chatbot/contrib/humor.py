import re
from chatbot.chat import ChatResponse
from chatbot.contrib.base import Feature

class SlapbackFeature(Feature):
	match_re = r"slaps %s(.*)"
	
	def handles_query(self, query):
		if re.match(self.match_re % query.bot.nickname, query.query):
			return True
	
	def handle_query(self, query):
		match = re.match(self.match_re % query.bot.nickname, query.query)
		return ChatResponse("slaps %s back%s" % (query.nickname, match.group(1)), action=True)