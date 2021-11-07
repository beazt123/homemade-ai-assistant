import os
import logging
import warnings
from speech_recognition import Microphone as computerMic
from configparser import ConfigParser
from lib.constants import readme
from lib.engine.systemconfigapi import SystemConfig
from lib.engine.userpreferencesapi import UserPreferences
from lib.engine.voiceAssistantToolkit import WakeWordDetector, Bot, Engine
from lib.events.dispatcher import Dispatcher
from lib.constants import FAILED_TOKEN


def load_config():
	pathToApiConfig = os.path.join("lib", "config-files", "config.ini")
	api = ConfigParser()
	api.read(pathToApiConfig)
	weather_api_key = api.get("WEATHER", "API_KEY")
	
	
	pathToSysConfig = os.path.join("lib", "config-files", "sysconfig.ini")
	systemConfig = SystemConfig(pathToSysConfig)
	systemConfig.APPID = weather_api_key
	
	pathToUserConfig = os.path.join("lib", "config-files", "userconfig.ini")
	userConfig = UserPreferences(pathToUserConfig)
	
	if systemConfig.MODE == "production":
		warnings.filterwarnings("ignore")
		logging.disable(logging.CRITICAL)
	elif systemConfig.MODE == "development":
		logging.basicConfig(level=systemConfig.LOG_LEVEL)
		
	return userConfig, systemConfig

def create_dispatcher(engine):
	dispatcher = Dispatcher()
	dispatcher.add_handler(FAILED_TOKEN, engine.ignore)#event, callback
	dispatcher.add_handler("shutdown", engine.shutdown)
	dispatcher.add_handler("youtube", engine.youtube)
	dispatcher.add_handler("music", engine.offlineMusic)
	dispatcher.add_handler("wiki", engine.wiki)
	dispatcher.add_handler("google", engine.google)
	dispatcher.add_handler("define", engine.define)
	dispatcher.add_handler("terminal", engine.terminal)
	dispatcher.add_handler("tell", engine.tell)
	dispatcher.add_handler("news", engine.news)
	dispatcher.add_handler("options", engine.updateOptions)
	dispatcher.add_handler("weather", engine.weather)
	dispatcher.add_handler("ready", engine.readySoundEffect)
	
	return dispatcher

	

def main():
	userConfig, systemConfig = load_config()
		
	print(readme)
	
	agent = WakeWordDetector()
	engine = Engine(systemConfig, userConfig, enableVoiceResponses = True)
	dispatcher = create_dispatcher(engine)
	bot = Bot(computerMic(), dispatcher)
	
	while True:
		try:
			bot.adjust_for_ambient_noise()
			print("\nReady")
			agent.waitForWakeWord()
			bot.listen()
		except KeyboardInterrupt:
			del bot
			del agent
			del engine
			break
		


if __name__ == "__main__":
	main()
