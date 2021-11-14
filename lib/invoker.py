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
'''

subscribers = defaultdict(list)

def subscribe(event_type, fn):
    subscribers[event_type].append(fn)

def post_event(event_type, data): 
    if event_type in subscribers:
        for fn in subscribers[event_type]:
            fn(data)
			
			
class Engine:
	def youtube(self, search):
		pass
		
	def google(self, search):
		pass
		
	def offline_music(self):
		pass
		
	def define(self, word):
		pass
		
	# extensible by way of methods
		

e = Engine(systemConfig, userPreferences)


d = Dispatcher()
d.add_handler("youtube", e.youtube)
d.add_handler("google", e.google)
d.add_handler("offline_music", e.offline_music)
d.add_handler("define", e.define)

# only for google home interface
d.add_handler("gender", e.changae_ai_gender)


command = bot.listen()...
event, data = bot.process(command)

bot.dispatcher.post_event(event, data)





e = Engine(systemConfig, userPreferences)


d = Dispatcher()
d.add_handler("youtube", e.youtube)
d.add_handler("google", e.google)
d.add_handler("offline_music", e.offline_music)
d.add_handler("define", e.define)

ArgumentParser().addHandler()




'''
