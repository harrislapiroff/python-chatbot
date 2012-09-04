class Feature(object):
	"A base feature class that provides some sane defaults and should be subclassed."
	allow_continuation =  False
	addressing_required = False
	
	def __init__(self, allow_continuation=False, addressing_required=False):
		self.allow_continuation = allow_continuation
		self.addressing_required = addressing_required
	
	def handles_query(self, query):
		raise NotImplementedError('`handles_query` method must be defined on %s.' % self.__class__.__name__)
	
	def handle_query(self, query):
		raise NotImplementedError('`handle_query` method must be defined on %s.' % self.__class__.__name__)