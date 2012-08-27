import re
from chatbot.chat import ChatResponse

class SlapbackFeature(object):
	allow_continuation = False
	match_re = r"slaps %s([.*])"
	
	def handles_query(self, query):
		if re.match(self.match_re % query.bot.nickname, query.query):
			return True
	
	def handle_query(self, query):
		target = query.user['raw'] if query.private else query.channel
		match = re.match(self.match_re % query.bot.nickname, query.query)
		return ChatResponse("slaps %s%s" % (query.nickname, match.group(1)), target=target, action=True)