from __future__ import absolute_import
import re
import random
from copy import copy
from chatbot.chat import ChatResponse
from chatbot.contrib.base import Feature

class Match(Feature):
	
	def __init__(self, match_re, response, allow_continuation=True, addressing_required=False):
		"""
		Arguments:
		match_re -- the regular expression to match
		response -- either a single ChatResponse/text string/replacement
		            function, or a list of the same to choose randomly from.
		            Text can include $1, et. al. for pattern
		            match interpolation.
		            Response text should be formatted as a replacement string
		            to be handled by Python's re.sub()
		
		"""
		
		self.match_re = match_re
		self.response = response
		self.allow_continuation = allow_continuation
		self.addressing_required = addressing_required
	
	def handles_query(self, query):
		# If the query matches the regular expression, return True.
		if re.match(self.match_re, query.query):
			return True
	
	def handle_query(self, query):
		response = self.get_response(query) # pass the query for subclasses that override get_response and need the query to be available
		compiled_re = re.compile(self.match_re)
		
		if isinstance(response, ChatResponse):
			# if the response is already a ChatResponse instance, modify it in place
			response.content = compiled_re.sub(response.content, query.query)
		else:
			# otherwise, it's a string -- use the string and create a ChatResponse
			content = compiled_re.sub(response, query.query)
			response = ChatResponse(content)
		
		return response
	
	def get_response(self, query):
		"""
		Returns either a response object or a response string. Copies the
		response to avoid modifying the original instance attribute.
		
		"""
		
		if hasattr(self.response, '__iter__'):
			# if the response variable is an iterable, select one item randomly
			response = random.choice(self.response)
		else:
			# otherwise, assume it's a single string/ChatResponse
			response = self.response
		return copy(response)