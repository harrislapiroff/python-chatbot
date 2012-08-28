from twisted.internet import reactor
from chatbot.client import IRCBotFactory
from chatbot.settings import default_settings

class Bot(object):
	def __init__(self, **settings):
		self.settings = default_settings.copy()
		self.settings.update(settings)

	def run(self):
		factory = IRCBotFactory(self.settings)
		reactor.connectTCP(self.settings['hostname'], self.settings['port'], factory)
		reactor.run()
