from twisted.words.protocols import irc
from twisted.internet import protocol
from chatbot.chat import ChatQuery, ChatResponse
from chatbot.utils import import_class

class IRCBot(irc.IRCClient):
	
	def __init__(self, settings=None, *args, **kwargs):
		self.settings = settings
		self.features = []
		self.nickname = self.settings['nickname']
		self.channels = self.settings['channels']
		self.password = settings['server_password']
		for feature in self.settings['features']:
			feature_class = import_class(feature)
			self.features.append(feature_class())
	
	def signedOn(self):
		for channel in self.channels:
			self.join(channel)
	
	def privmsg(self, user, channel, message, action=False):
		"Upon receiving a message, handle it with the bot's feature set."
		query = ChatQuery(user=user, channel=channel, message=message, bot=self, action=action)
		for feature in self.features:
			if feature.handles_query(query):
				response = feature.handle_query(query)
				if response is not None:
					# Send either an action or a message.
					if response.action:
						self.me(response.target, response.content)
					else:
						self.msg(response.target, response.content)
				# if the feature disallows continuation, stop here
				if not feature.allow_continuation:
					break

	def action(self, user, channel, data):
		self.privmsg(user, channel, data, action=True)

class IRCBotFactory(protocol.ClientFactory):
	protocol = IRCBot
	
	def __init__(self, settings=None, *args, **kwargs):
		self.settings = settings
	
	def clientConnectionLost(self, connector, reason):
		"If disconnected, reconnect."
		connector.connect()
	
	def buildProtocol(self, addr):
		bot = self.protocol(self.settings)
		bot.factory = self
		return bot
		
	def clientConnectionFailed(self, connector, reason):
		print "connection failed: ", reason