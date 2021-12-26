import sys
import logging
import paho.mqtt.client as mqtt

from logging.handlers import SocketHandler
from logging import StreamHandler
args = sys.argv[1:]
kwargs = dict(arg.upper().split('=') for arg in args)

numeric_level = getattr(logging, kwargs.get('LOG', "CRITICAL"), None)

sockethandler = SocketHandler('127.0.0.1', 19996)
streamHandler = StreamHandler(sys.stdout)
streamHandler.setLevel(numeric_level)

logging.basicConfig(
	level=logging.NOTSET, 
	handlers=[
		sockethandler,
		streamHandler
		]
	)



from lib.constants import README
from lib.invoker import Invoker
from lib.utils.WakeWordDetector import WakeWordDetector
from lib.config.devices.windowsLaptopConfig import configuredInterpreter, commandHooks
from os import path
from configparser import ConfigParser
from lib.utils.dispatcher import Dispatcher



def set_up_mqtt_client():
	config = ConfigParser()
	config.read(path.join("lib", "config", "devices", "rpi_mqtt_broker_config.ini"))
	
	client = mqtt.Client("P1") #create new instance
	client.connect(config.get("MQTT", "IP_ADDR")) #connect to broker
	# client.publish("topic1","HURRAY IT WORKS") #publish
	return client
	

def main():
		
	print(README)
	
	agent = WakeWordDetector()
	bot = configuredInterpreter
	invoker = Invoker()
	invoker.registerAll(commandHooks)
	dispatcher = Dispatcher(invoker, set_up_mqtt_client())
	bot.switchOnSound()
	
	while True:
		try:
			bot.adjust_for_ambient_noise()
			print("\nReady")
			agent.waitForWakeWord()
			command, arg = bot.listen()
			dispatcher.dispatch(command, arg)
			# invoker.execute(command, arg)
		except KeyboardInterrupt:
			del bot
			del agent
			break
		


if __name__ == "__main__":
	main()
