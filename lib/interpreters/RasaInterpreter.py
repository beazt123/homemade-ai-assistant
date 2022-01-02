import logging
import requests
from pvporcupine import KEYWORDS
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


README = \
"""
J.A.R.V.I.S Intelligence Systems
================================
Wake words:
	Please say any 1 of the following words to wake J.A.R.V.I.S:
		{wakewords}
		
Things you can do with it:
	1) Search things on Google/Youtube/Wikipedia
		- For wikipedia, a written response will be shown and read aloud
		- For Google & Youtube, it will open a browser tab

	2) Play offline music (& stop it after you're done)
		- Set the music library file path in the config file
	
	3) Weather forecast in your area
		- Set the locale in the config file

	4) News flash

	5) Ask for time

	6) Get it to tell you a programming joke

	7) Define a word
	
	8) Shut down the entire computer

""".format(wakewords=", \n\t\t".join(KEYWORDS))

class RasaInterpreterException(Exception):
	pass



class RasaInterpreter(Interpreter):
	RASA_NLU_SERVER_BASE_URL = "http://localhost:5005/"
	RASA_NLU_PARSE_URL = f"{RASA_NLU_SERVER_BASE_URL}model/parse"
	HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	USER_GUIDE = README
	logger = logging.getLogger(__name__)

	@classmethod
	def getUserGuide(cls):
		return RasaInterpreter.USER_GUIDE

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

	@classmethod
	def process(cls, command):
		if command == Interpreter.FAILED_TOKEN:
			return DefaultCommand.__name__, None
		try:
			response = requests.post(cls.RASA_NLU_PARSE_URL, 
					json = { "text": command }, 
					headers = cls.HEADERS,
					timeout = 0.7)
		except Timeout:
			raise RasaInterpreterException("Server took too long to respond")
			
		if response.status_code == 200:
			js = response.json()
			intent = js["intent"]["name"]			
			event = cls.mapIntentToEvent(intent)
			data = cls.extractEntity(js)

			return event, data

		else:
			raise RasaInterpreterException(f"Response status code: {response.status_code} ({response.reason})")