from twisted.words.protocols import irc
from twisted.internet import protocol
from chatbot.chat import ChatQuery, ChatResponse

class IRCBot(irc.IRCClient):
	
	def __init__(self, settings=None, bot=None, *args, **kwargs):
		self.settings = settings
		self.features = []
		self.nickname = self.settings['nickname']
		self.channels = self.settings['channels']
		self.password = settings['server_password']
		self.bot = bot
		for feature in self.settings['features']:
			self.features.append(feature)
	
	def signedOn(self):
		for channel in self.channels:
			self.join(channel)
	
	def privmsg(self, user, channel, message, action=False):
		"Upon receiving a message, handle it with the bot's feature set."
		query = ChatQuery(user=user, channel=channel, message=message, bot=self.bot, client=self, action=action)
		for feature in self.features:
			# If they query is unaddressed and addressing is required, move to the next feature
			if feature.addressing_required and not query.addressed:
				continue
			if feature.handles_query(query):
				default_target = query.user['raw'] if query.private else query.channel
				response = feature.handle_query(query)
				if response is not None:
					# if a target it attached to the response, use it
					target = getattr(response, 'target', default_target)
					# Send either an action or a message.
					if response.action:
						self.describe(target, response.content)
					else:
						self.msg(target, response.content)
				# if the feature disallows continuation, stop iterating over features here
				if not feature.allow_continuation:
					break

	def action(self, user, channel, data):
		self.privmsg(user, channel, data, action=True)

class IRCBotFactory(protocol.ClientFactory):
	protocol = IRCBot
	
	def __init__(self, settings=None, bot=None, *args, **kwargs):
		self.settings = settings
		self.bot = bot
	
	def clientConnectionLost(self, connector, reason):
		"If disconnected, reconnect."
		connector.connect()
	
	def buildProtocol(self, addr):
		bot = self.protocol(self.settings, bot=self.bot)
		bot.factory = self
		return bot
		
	def clientConnectionFailed(self, connector, reason):
		print "connection failed: ", reason