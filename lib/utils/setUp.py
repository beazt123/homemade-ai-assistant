import logging
import pyttsx3
import yaml
from ..iot.MQTTClient import MQTTClient

from speech_recognition import Microphone as computerMic
from configparser import ConfigParser
from .WakeWordDetector import WakeWordDetector
from .interpreter import Interpreter
from .dispatcher import Dispatcher
from ..invoker import Invoker
from ..receivers.engines.sound_engine import SoundEngine
from ..receivers import *
from ..constants import README
from ..commands import (
	DefineWord,
	GetNews,
	DefaultCommand,
	GetWeatherForecast,
	GoogleSearch,
	PlayYoutubeVideo,
	ShutdownSystem,
	StartOfflineMusic,
	StopOfflineMusic,
	StopProgram,
	TellAJoke,
	TellTime,
	WikiSearch
)

'''
logger

import & read all config

intialise system level objects: speech engine, sound engine

Initialise & configure receivers

create a command hook dictionary -> create & configure invoker

wrap invoker with dispatcher
'''
logger = logging.getLogger(__name__)

class App:
	def __init__(self, 
				 wakeWordDetector = None,
				 interpreter = None,
				 dispatcher = None) -> None:
		self.wakeWordDetector = wakeWordDetector
		self.interpreter = interpreter
		self.dispatcher = dispatcher
		self.main = None

	def run(self):
		if self.main:
			self.main(self.wakeWordDetector,
						self.interpreter,
						self.dispatcher)
		else:
			raise ValueError("Main attribute must be set before app.run() can be called.")

def set_up_iot_client(config):
	iot_client = None
	client_type = config.get("IOT", "TYPE")
	if client_type.lower() == "mqtt":
		iot_client = MQTTClient(config.get("MQTT", "IP_ADDR"))
	else:
		raise ValueError("No IOT client setting provided in system configuration")
	return iot_client

def getSetUpConfig(filepath):
	with open(filepath, 'r') as stream:
		dictionary = yaml.safe_load(stream)
		# for key, value in dictionary.items():
		#     print (key + " : " + str(value))
	return dictionary

def getConfig(*filepaths):
	configParser = ConfigParser()
	for filepath in filepaths:
		configParser.read(filepath)
	
	return configParser
		
def runAsStandalone(wakeWordDetector, interpreter, dispatcher):
	print(README)
	interpreter.switchOnSound()

	while True:
		try:
			interpreter.adjust_for_ambient_noise()
			print("\nReady")
			wakeWordDetector.waitForWakeWord()
			command, arg = interpreter.listen()
			dispatcher.dispatch(command, arg)
		# invoker.execute(command, arg)
		except KeyboardInterrupt:
			del interpreter
			del wakeWordDetector
			break

def createApp(config, setUpConfig) -> App:
	
	soundEngine = SoundEngine()
	speechEngine = pyttsx3.init()
	
	commandsToUse = list()
	receivers = setUpConfig["receivers"]
	if "Dictionary" in receivers:
		englishDictionary = Dictionary(config, speechEngine)
		logger.info(f"Created {Dictionary.__name__} ")
		commandsToUse.append(DefineWord(englishDictionary))
	if "GeneralReceiver" in receivers:
		generalReception = GeneralReceiver(config, speechEngine)
		logger.info(f"Created {GeneralReceiver.__name__} ")
		commandsToUse.extend([
			TellAJoke(generalReception),
			TellTime(generalReception)
		])
	if "News" in receivers:
		newsCaster = News(config, speechEngine, soundEngine)
		logger.info(f"Created {News.__name__} ")
		commandsToUse.append(GetNews(newsCaster))
	if "OfflineMusic" in receivers:
		offlineMusicPlayer = OfflineMusic(config, speechEngine)
		logger.info(f"Created {OfflineMusic.__name__} ")
		commandsToUse.extend([
			StartOfflineMusic(offlineMusicPlayer),
			StopOfflineMusic(offlineMusicPlayer)
		])
	if "Searcher" in receivers:
		searcher = Searcher(config, speechEngine, soundEngine)
		logger.info(f"Created {Searcher.__name__} ")
		commandsToUse.extend([
			GoogleSearch(searcher),
			PlayYoutubeVideo(searcher),
			WikiSearch(searcher)
		])
	if "System" in receivers:
		systemInterface = System(config, speechEngine, soundEngine)
		logger.info(f"Created {System.__name__} ")
		commandsToUse.extend([
			StopProgram(systemInterface),
			ShutdownSystem(systemInterface)
		])
	if "Weather" in receivers:
		weatherForecaster = Weather(config, speechEngine)
		logger.info(f"Created {Weather.__name__} ")
		commandsToUse.append(GetWeatherForecast(weatherForecaster))

	fallbackReceiver = FallbackReceiver(config, soundEngine)
	logger.info(f"Created {FallbackReceiver.__name__} ")
	commandsToUse.append(DefaultCommand(fallbackReceiver))
	
	commandHooks = {command.__class__.__name__: command for command in commandsToUse}
	
	wakeWordDetector = WakeWordDetector(config.get("WAKE-WORD-DETECTOR", "ACCESS_KEY"))

	invoker = Invoker()
	invoker.registerAll(commandHooks)
	iot_client = set_up_iot_client(config)
	dispatcher = Dispatcher(invoker, iot_client)
	
	interpreter = Interpreter(config, soundEngine, computerMic())
	logger.info(f"Created {Interpreter.__name__} ")


	app = App(wakeWordDetector, interpreter, dispatcher)
	if setUpConfig["type"] == "standalone":
		app.main = runAsStandalone
	
	return app
	