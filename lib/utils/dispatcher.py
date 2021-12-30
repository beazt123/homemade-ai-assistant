import logging

logger = logging.getLogger(__name__)

class Dispatcher:
	def __init__(self, invoker = None, iot_client = None):
		self.invoker = invoker
		self.iot_client = iot_client
	
	# @property
	# def invoker(self):
	# 	return self.invoker
		
	# @invoker.setter
	# def invoker(self, externalInvoker):
	# 	self.invoker = externalInvoker
		
	def dispatch(self, event, data):
		try:
			logger.info(f"Attempting to dispatch ({event}:{data}) to invoker")
			self.invoker.execute(event, data)
			logger.info(f"Dispatched ({event}:{data}) to invoker")

		except ValueError:
			logger.info(f"{event} not found in invoker. Dispatching ({event}:{data}) to IOT client")

			self.iot_client.publish(event, data)#publish
			logger.info(f"Dispatched ({event}:{data}) to IOT client")
		
	def standBy(self):
		''' Blocking command used by slave nodes '''
		pass
		
	# # private method
	# def invoke(self, event, data = None):
	# 	try:
	# 		self.invoker.execute(event, data)
	# 	except KeyError:
	# 		logger.error(f"Non existent event({event}) called on {Dispatcher.__name__}")
		
	
		
	


'''
Use Event as topic, data/null as arg

event, data = bot.listen()
invoker.invoke(event, data)

## SELECTED USE CASE
	event, data = bot.listen()
	dispatcher.dispatch(event, data)


event, data = bot.listen()
if invoker.invoke(event, data):
    continue
else:
    dispatcher.dispatch(event, data)

'''