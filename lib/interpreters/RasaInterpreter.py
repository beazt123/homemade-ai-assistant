import logging
import requests
from requests.exceptions import Timeout
from ..iot.IOTClient import IOTClient
from .interpreter import Interpreter
from lib.commands import (
	DefineWord,
	GetNews,
	GetWeatherForecast,
	GoogleSearch,
	PlayYoutubeVideo,
	ShutdownSystem,
	StartOfflineMusic,
	StopOfflineMusic,
	# StopProgram,
	TellAJoke,
	TellTime,
	WikiSearch,
	DefaultCommand
)

class RasaInterpreterException(Exception):
	pass



class RasaInterpreter(Interpreter):
	RASA_NLU_SERVER_BASE_URL = "http://localhost:5005/"
	RASA_NLU_PARSE_URL = f"{RASA_NLU_SERVER_BASE_URL}model/parse"
	HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	logger = logging.getLogger(__name__)

	@staticmethod
	def mapIntentToEvent(intent):
		event = DefaultCommand.__name__
		if intent == "define_word":
			event = DefineWord.__name__
		elif intent == "play_music":
			event = StartOfflineMusic.__name__
		elif intent == "stop_music":
			event = StopOfflineMusic.__name__
		elif intent == "tell_time":
			event = TellTime.__name__
		elif intent == "tell_joke":
			event = TellAJoke.__name__
		elif intent == "read_news":
			event = GetNews.__name__
		elif intent == "weather_forecast":
			event = GetWeatherForecast.__name__
		elif intent == "shutdown_system":
			event = ShutdownSystem.__name__
		elif intent == "youtube_search":
			event = PlayYoutubeVideo.__name__
		elif intent == "wiki_search":
			event = WikiSearch.__name__
		elif intent == "google_search":
			event = GoogleSearch.__name__
		
		return event
		
	
	@staticmethod
	def extractEntity(responseJs):
		entityIndices = list()
		entities = responseJs["entities"]
		entityPhrase = None

		if len(entities) > 0:
			for entity in entities:
				entityIndices.append(entity["start"])
				entityIndices.append(entity["end"])

			entityPhrase = responseJs["text"][min(entityIndices): max(entityIndices)]

		return entityPhrase

	@staticmethod
	def processIOTcmd(cmd):
		# Detect for IOT commands 1st
		if cmd == "switch_on_lights":
			event = "lights"
			data = "1"
		elif cmd == "switch_off_lights":
			event = "lights"
			data = "0"
		
		return event, data
	
	@staticmethod
	def isIOTcmd(cmd):
		return cmd in IOTClient.ALLOWED_COMMANDS

	@classmethod
	def process(cls, command):
		if command == Interpreter.FAILED_TOKEN:
			cls.logger.warn("Failed to interpret command. Reverting to default command")
			return DefaultCommand.__name__, None
		try:
			response = requests.post(cls.RASA_NLU_PARSE_URL, 
					json = { "text": command }, 
					headers = cls.HEADERS,
					timeout = 0.7)
			cls.logger.info("Rasa Server responded")
		except Timeout:
			cls.logger.warn("Rasa Server timeout")
			raise RasaInterpreterException("Server took too long to respond")
			
		if response.status_code == 200:
			js = response.json()
			intent = js["intent"]["name"]
			cls.logger.info(f"Detected intent: {intent}")

			if RasaInterpreter.isIOTcmd(intent):
				return RasaInterpreter.processIOTcmd(intent)
			else:
				event = cls.mapIntentToEvent(intent)
				data = cls.extractEntity(js)

				cls.logger.info(f"Event, data: {event}, {data}")
				return event, data

		else:
			raise RasaInterpreterException(f"Response status code: {response.status_code} ({response.reason})")