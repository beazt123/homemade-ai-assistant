import os
import logging
import warnings
from configparser import ConfigParser
from lib.constants import readme
from lib.engine.systemconfigapi import SystemConfig
from lib.engine.userpreferencesapi import UserPreferences
from lib.engine.voiceAssistantToolkit import WakeWordDetector, Bot


def main():
	pathToSysConfig = os.path.join("lib", "config-files", "sysconfig.ini")
	systemConfig = SystemConfig(pathToSysConfig)
	
	pathToUserConfig = os.path.join("lib", "config-files", "userconfig.ini")
	userConfig = UserPreferences(pathToUserConfig)
	
	
	
	if systemConfig.MODE == "production":
		warnings.filterwarnings("ignore")
		logging.disable(logging.CRITICAL)
	elif systemConfig.MODE == "development":
		logging.basicConfig(level="DEBUG")
		
		
	print(readme)
	
	agent = WakeWordDetector()
	bot = Bot(systemConfig, userConfig)
	
	while True:
		try:
			bot.adjust_for_ambient_noise()
			print("\nReady")
			agent.waitForWakeWord()
			bot.listen()
		except KeyboardInterrupt:
			del bot
			del agent
			break
		


if __name__ == "__main__":
	main()