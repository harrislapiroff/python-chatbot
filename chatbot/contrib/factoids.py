import re

from chatbot.contrib.base import Feature
from chatbot.db import Base

from sqlalchemy import Column, String, Integer, Sequence, Boolean
from sqlalchemy.orm import sessionmaker

class Factoid(Base):
	__tablename__ = 'factoids'

	id = Column(Integer, Sequence('factoid_id_seq'), primary_key=True)
	key = Column(String)
	are = Column(Boolean)
	value = Column(String)

	def __init__(self, key, value, conjugation='is'):
		self.key = key
		self.value = value
		self.are = False if conjugation == 'is' else True

class FactoidSaver(Feature):
	allow_continuation = True
	addressing_required = False
	match_re = r'(?P<key>.*) (?P<conjugation>is|are) (?P<value>.*)'

	def handles_query(self, query):
		# If the query matches the regular expression, return True.
		if re.match(self.match_re, query.query):
			return True

	def handle_query(self, query):
		matches = re.match(self.match_re, query.query).groupdict()
		factoid = Factoid(matches['key'], matches['value'], matches['conjugation'])
		Session = sessionmaker(bind=query.bot.database)
		session = Session()
		session.add(factoid)
		session.commit()