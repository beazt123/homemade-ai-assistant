import logging


class Dispatcher:
	logger = logging.getLogger(__name__)
	def __init__(self, invoker = None, iot_client = None):
		self.invoker = invoker
		self.iot_client = iot_client
		
		
	def dispatch(self, event, data):
		try:
			Dispatcher.logger.info(f"Attempting to dispatch ({event}:{data}) to invoker")
			self.invoker.execute(event, data)
			Dispatcher.logger.info(f"Dispatched ({event}:{data}) to invoker")

		except ValueError:
			Dispatcher.logger.info(f"{event} not found in invoker. Dispatching ({event}:{data}) to IOT client")

			if self.iot_client:
				published = self.iot_client.publish(event, data)	

				if published:
					Dispatcher.logger.info(f"Dispatched ({event}:{data}) to IOT client")
				else:
					Dispatcher.logger.info(f"No such IOT command. Ignored.")
			else:
				Dispatcher.logger.info("Command not found and IOTClient absent to publish message. Ignoring current command")
		
	def standBy(self):
		''' Blocking command used by slave nodes '''
		pass
		
	# # private method
	# def invoke(self, event, data = None):
	# 	try:
	# 		self.invoker.execute(event, data)
	# 	except KeyError:
	# 		Dispatcher.logger.error(f"Non existent event({event}) called on {Dispatcher.__name__}")
		
	
		
	


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