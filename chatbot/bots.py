from twisted.internet import reactor

from chatbot.db import Base
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
		
		if 'database' in self.settings:
			# Instantiate the database engine
			self.database = create_engine(self.settings['database'])
			# Create any tables that have not been created.
			Base.metadata.create_all(self.database)

	def run(self):
		factory = IRCBotFactory(self.settings, bot=self)
		reactor.connectTCP(self.settings['hostname'], self.settings['port'], factory)
		reactor.run()
