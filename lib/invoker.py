import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class Invoker:
	def __init__(self):
		self._commands = defaultdict()
		
	def register(self, cmd_name, cmd):
		self._commands[cmd_name] = cmd
	
	def registerAll(self, cmd_dict):
		self._commands.update(cmd_dict)
		
	def execute(self, event, data = None):
		logger.info(f"{self.__class__.__name__} attempting to call {event} with {data}")
		if event in self._commands.keys():
			self._commands[event](data)
			logger.info(f"{self.__class__.__name__} call {event} with {data} successful")
		else:
			raise ValueError("No such command")