from __future__ import absolute_import
import re
import random
from chatbot.chat import ChatResponse

class DiceFeature(object):
	"""
	Rolls dice and responds with the results.
	
	Example queries that should be matched by match_re:
	
		/me rolls 1d6
		Rolls one six-sided die.
		
		/me rolls 3d2+1
		Rolls three two-sided dice and adds 1 to each result.
		
		/me rolls 6d6 - 4
		Rolls six six-sided dice and subtracts 4 from each result.
	
	"""
	allow_continuation = False
	match_re = r"rolls ([0-9]+)d([0-9]+)[\s]*([\+\-]?)[\s]*([0-9]*)"
	
	def handles_query(self, query):
		if query.action and re.match(self.match_re, query.query):
			return True
	
	def handle_query(self, query):
		bits = re.match(self.match_re, query.query)
		dice_count = int(bits.group(1))
		dice_sides = int(bits.group(2))
		operator = bits.group(3)
		addend_or_subtrahend = int(bits.group(4)) if operator != "" else None
		
		results = [random.randint(1, dice_sides) for x in range(0, dice_count)]
		results_sum = sum(results)
		
		# add or subtract the addend_or_subtrahend if an operator is present
		if operator == "+":
			results_sum = results_sum + addend_or_subtrahend
		elif operator == "-":
			results_sum = results_sum - addend_or_subtrahend
			
		results_text = ", ".join(str(i) for i in results)
		response_content = "%s got %s for a total of %d" % (query.nickname, results_text, results_sum)
		
		# if the response is too long, don't display individual results
		if len(response_content) > query.bot.settings['message_max_length']:
			response_content = "%s rolled %sd%s for a total of %d" % (query.nickname, dice_count, dice_sides, results_sum)
		
		return ChatResponse(response_content)

class ChoiceFeature(object):
	allow_continuation = False
	match_re = r"(.*) or ([^?]*)\??"
	
	def handles_query(self, query):
		if query.addressed and re.match(self.match_re, query.query):
			return True
	
	def handle_query(self, query):
		bits = re.match(self.match_re, query.query)
		choice = random.randint(1,2)
		
		return ChatResponse(bits.group(choice))