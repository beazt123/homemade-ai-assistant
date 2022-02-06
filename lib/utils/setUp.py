import logging
import pyttsx3
from speech_recognition import Microphone as computerMic

from .article_builder import ArticleBuilder
from ..constants import USER_GUIDES
from ..interpreters import MasterInterpreter
from ..iot.MQTTClient import MQTTClient
from .WakeWordDetector import WakeWordDetector
from ..interpreters import RasaInterpreter, RegexInterpreter
from .dispatcher import Dispatcher
from ..invoker import Invoker
from ..receivers.engines.sound_engine import SoundEngine
from ..receivers import *
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
from lib import receivers

logger = logging.getLogger(__name__)


class App:
	def __init__(self, 
				 wakeWordDetector = None,
				 interpreter = None,
				 dispatcher = None):
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
			raise ValueError("Main attribute of app object must be set before app.run() can be called.")

def set_up_iot_client(config, iot_topics, logger):
	iot_client = None
	client_type = config.get("IOT", "TYPE")
	logger.info(f"Retrieved client type: {client_type}")
	logger.info(f"Topics to subscribe to: {iot_topics}")
	if client_type.lower() == "mqtt":
		iot_client = MQTTClient(iot_topics, config.get("MQTT", "IP_ADDR"))
		logger.info(f"Created {MQTTClient.__name__}: {iot_client}")
		logger.info(f"{iot_client} subscribed to {iot_topics}")
	else:
		raise ValueError("No IOT client setting provided in system configuration")
	return iot_client

def create_help_msg(wakeWordDetector, receivers):

	
	user_guide_builder = ArticleBuilder()
	user_guide_builder.title("A.I general assistant")
	user_guide_builder.subtitle("Wake words")
	user_guide_builder.startSection()
	user_guide_builder.content(f"Please say any 1 of the following words to wake me up:")
	user_guide_builder.content(', '.join(wakeWordDetector.wake_words))
	user_guide_builder.br()

	user_guide_builder.endSection()
	user_guide_builder.subtitle("What I can do:")
	user_guide_builder.startSection()

	for receiver in receivers:
		user_guide_builder.subtitle(USER_GUIDES[receiver]["title"])
		user_guide_builder.startSection()
		for line in USER_GUIDES[receiver]["content"]:
			user_guide_builder.content(line)
		user_guide_builder.endSection()
		user_guide_builder.br(2)
	user_guide_builder.endSection()

	return user_guide_builder.getArticleInPlainText()


	
		
def runAsStandalone(wakeWordDetector, interpreter, dispatcher, receivers):
	print(create_help_msg(wakeWordDetector, receivers))
	interpreter.switchOnSound()

	while True:
		try:
			# interpreter.adjust_for_ambient_noise()
			print("\nReady")
			wakeWordDetector.waitForWakeWord()
			command, arg = interpreter.interpret()
			dispatcher.dispatch(command, arg)
		# invoker.execute(command, arg)
		except KeyboardInterrupt:
			del interpreter
			del wakeWordDetector
			break

def runAsSlave(wakeWordDetector, interpreter, dispatcher):
	dispatcher.standBy()


def createApp(config, setUpConfig) -> App:
	wakeWordDetector = None
	interpreter = None
	dispatcher = None
	main = None
	
	soundEngine = SoundEngine()
	speechEngine = pyttsx3.init()
	
	commandsToUse = list()
	receivers = setUpConfig["receivers"]
	if Dictionary.__name__ in receivers:
		englishDictionary = Dictionary(config, speechEngine)
		logger.info(f"Created {Dictionary.__name__} ")
		commandsToUse.append(DefineWord(englishDictionary))
	if GeneralReceiver.__name__ in receivers:
		generalReception = GeneralReceiver(config, speechEngine)
		logger.info(f"Created {GeneralReceiver.__name__} ")
		commandsToUse.extend([
			TellAJoke(generalReception),
			TellTime(generalReception)
		])
	if News.__name__ in receivers:
		newsCaster = News(config, speechEngine, soundEngine)
		logger.info(f"Created {News.__name__} ")
		commandsToUse.append(GetNews(newsCaster))
	if OfflineMusic.__name__ in receivers:
		offlineMusicPlayer = OfflineMusic(config, speechEngine)
		logger.info(f"Created {OfflineMusic.__name__} ")
		commandsToUse.extend([
			StartOfflineMusic(offlineMusicPlayer),
			StopOfflineMusic(offlineMusicPlayer)
		])
	if Searcher.__name__ in receivers:
		searcher = Searcher(config, speechEngine, soundEngine)
		logger.info(f"Created {Searcher.__name__} ")
		commandsToUse.extend([
			GoogleSearch(searcher),
			PlayYoutubeVideo(searcher),
			WikiSearch(searcher)
		])
	if System.__name__ in receivers:
		systemInterface = System(config, speechEngine, soundEngine)
		logger.info(f"Created {System.__name__} ")
		commandsToUse.extend([
			StopProgram(systemInterface),
			ShutdownSystem(systemInterface)
		])
	if Weather.__name__ in receivers:
		weatherForecaster = Weather(config, speechEngine)
		logger.info(f"Created {Weather.__name__} ")
		commandsToUse.append(GetWeatherForecast(weatherForecaster))

	fallbackReceiver = FallbackReceiver(config, soundEngine)
	logger.info(f"Created {FallbackReceiver.__name__} ")
	commandsToUse.append(DefaultCommand(fallbackReceiver))
	
	commandHooks = {command.__class__.__name__: command for command in commandsToUse}
	invoker = Invoker()
	invoker.registerAll(commandHooks)
	logger.info("Added command hooks to invoker")
	iot_topics = setUpConfig.get("iot_topics")
	if iot_topics:
		iot_client = set_up_iot_client(config, iot_topics, logger)
		logger.info("Set up IOT client")
	else:
		iot_client = None
	dispatcher = Dispatcher(invoker, iot_client)
	

	if setUpConfig["type"].lower() == "standalone" or setUpConfig["type"].lower() == "master":
		chosen_wakewords = setUpConfig["wakewords"]
		wakeWordDetector = WakeWordDetector(config.get("WAKE-WORD-DETECTOR", "ACCESS_KEY"), chosen_wakewords)
		
		if setUpConfig["interpreter"].lower() == "rasa":
			selectedInterpreter = RasaInterpreter
		elif setUpConfig["interpreter"].lower() == "regex":
			selectedInterpreter = RegexInterpreter
		elif setUpConfig["interpreter"].lower() == "master":
			selectedInterpreter = MasterInterpreter
		else:
			selectedInterpreter = RegexInterpreter

		
		interpreter = selectedInterpreter(config, soundEngine, computerMic())
		logger.info(f"Created {selectedInterpreter.__name__} ")
		main = lambda wakeWordDetector, interpreter, dispatcher  : runAsStandalone(wakeWordDetector, interpreter, dispatcher, receivers)
	
	elif setUpConfig["type"].lower() == "slave":
		main = runAsSlave


	app = App(wakeWordDetector, interpreter, dispatcher)
	app.main = main
	
	
	return app
	