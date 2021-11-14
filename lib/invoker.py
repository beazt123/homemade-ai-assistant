from collections import defaultdict

class Invoker:
	def __init__(self):
		self._commands = defaultdict(list)
		
	def register(self, cmd_name, cmd):
		self._commands[cmd_name] = cmd
	
	def registerAll(self, cmd_dict):
		self._commands.update(cmd_dict)
		
	def execute(self, event, data = None):
		if event in self._commands.keys():
			self._commands[event](data)