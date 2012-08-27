import re

class ChatQuery(object):
	ADDRESSED_RE = "%s\s*[:,\-]?\s*(.*)"
	
	def __init__(self, **kwargs):
		self.raw_data = kwargs
		self.bot = kwargs['bot']
		self.nickname = kwargs['user'].split('!', 1)[0]
		self.private = True if kwargs['channel'] == self.bot.settings['nickname'] else False
		self.query = kwargs['message']
		self.channel = kwargs['channel']
		
		# check if the match is addressed
		addressed_match = re.match(self.ADDRESSED_RE % self.bot.settings['nickname'], self.query)
		if addressed_match:
			self.addressed = True
			self.query = addressed_match.group(1)
		else:
			self.addressed = False

class ChatResponse(object):
	
	def __init__(self, content, **kwargs):
		self.content = content
		self.target = kwargs['target']
	
	def __str__(self):
		return content