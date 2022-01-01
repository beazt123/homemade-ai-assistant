import logging
import requests
from requests.exceptions import Timeout
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
	RASA_NLU_SERVER_BASE_URL = "localhost:5005/"
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


	def interpret(self, command):
		try:
			response = requests.post(RasaInterpreter.RASA_NLU_PARSE_URL, 
					json = { "text": command }, 
					headers = RasaInterpreter.HEADERS,
					timeout = 2)
		except Timeout:
			raise RasaInterpreterException("Server took too long to respond")
			
		if response.status_code == 200:
			js = response.json()
			intent = js["intent"]["name"]			
			event = RasaInterpreter.mapIntentToEvent(intent)
			data = RasaInterpreter.extractEntity(js)

			return event, data

		else:
			raise RasaInterpreterException(f"Response status code: {response.status_code} ({response.reason})")