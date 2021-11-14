


from lib.constants import readme
from lib.invoker import Invoker
from lib.utils.WakeWordDetector import WakeWordDetector

from lib.config.devices.windowsLaptopConfig import configuredInterpreter, commandHooks
	

def main():
		
	print(readme)
	
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
	main()
