import re

class ChatQuery(object):
	ADDRESSED_RE = "%s\s*[:,\-]?\s*(.*)"
	
	def __init__(self, **kwargs):
		self.raw_data = kwargs
		self.bot = kwargs['bot']
		self.client = kwargs['client']
		self.nickname = kwargs['user'].split('!', 1)[0]
		self.private = True if kwargs['channel'] == self.bot.settings['nickname'] else False
		self.query = kwargs['message']
		self.channel = kwargs['channel']
		self.action = kwargs['action'] if 'action' in kwargs else False
		
		# check if the match is addressed
		addressed_match = re.match(self.ADDRESSED_RE % self.client.settings['nickname'], self.query)
		if addressed_match:
			self.addressed = True
			self.query = addressed_match.group(1)
		else:
			self.addressed = False

class ChatResponse(object):

	def __init__(self, content, **kwargs):
		self.content = content
		if 'target' in kwargs:
			self.target = kwargs['target']
		self.action = kwargs['action'] if 'action' in kwargs else False
	
	def __str__(self):
		return content