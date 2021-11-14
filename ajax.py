import sys
import logging
args = sys.argv[1:]
kwargs = dict(arg.upper().split('=') for arg in args)
numeric_level = getattr(logging, kwargs.get('LOG', "CRITICAL"), None)
logging.basicConfig(level=numeric_level)


from lib.constants import README
from lib.invoker import Invoker
from lib.utils.WakeWordDetector import WakeWordDetector

from lib.config.devices.windowsLaptopConfig import configuredInterpreter, commandHooks
	

def main():
		
	print(README)
	
	agent = WakeWordDetector()
	bot = configuredInterpreter
	invoker = Invoker()
	invoker.registerAll(commandHooks)

	bot.switchOnSound()
	
	while True:
		try:
			bot.adjust_for_ambient_noise()
			print("\nReady")
			agent.waitForWakeWord()
			command, arg = bot.listen()
			invoker.execute(command, arg)
		except KeyboardInterrupt:
			del bot
			del agent
			break
		


if __name__ == "__main__":
	
	
	
	# logging.disable(logging.CRITICAL)
	
			

	main()
