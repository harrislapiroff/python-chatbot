from twisted.internet import reactor
from chatbot.client import IRCBotFactory
from chatbot.settings import default_settings
from sqlalchemy import create_engine

class Bot(object):
	"""
	The Bot object manages the IRC client factory and the database. It
	provides a high-level interface through which to issue management commands
	to the bot.

	"""

	def __init__(self, **settings):
		self.settings = default_settings.copy()
		self.settings.update(settings)
		
		# instantiate the database engine
		if 'database' in self.settings:
			self.database = create_engine(self.settings['database'])

	def run(self):
		factory = IRCBotFactory(self.settings)
		reactor.connectTCP(self.settings['hostname'], self.settings['port'], factory)
		reactor.run()
