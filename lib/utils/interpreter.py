import re
import logging
import speech_recognition as sr
from lib.receivers.soundEffectsMixin import SoundEffectsMixin
from lib.receivers.asyncStdVoiceResponseMixin import AsyncStdVoiceResponseMixin


from lib.commands import (
    DefineWord,
    GetNews,
    GetWeatherForecast,
    GoogleSearch,
    PlayYoutubeVideo,
    ShutdownSystem,
    StartOfflineMusic,
    StopOfflineMusic,
    StopProgram,
    TellAJoke,
    TellTime,
    WikiSearch,
	DefaultCommand
)

logger = logging.getLogger(__name__)

class Interpreter(SoundEffectsMixin, AsyncStdVoiceResponseMixin):
	FAILED_TOKEN = "!FAILED"

	def __init__(self, config, soundEngine, mic):
		logger.info(f"Creating Sound effects mixin for {Interpreter.__name__}")
		SoundEffectsMixin.__init__(self, config, soundEngine)
		logger.info(f"Created effects mixin for {Interpreter.__name__}")

		logger.info(f"Creating Async standard AI voice response mixin for {Interpreter.__name__}")
		AsyncStdVoiceResponseMixin.__init__(self, config, soundEngine)
		logger.info(f"Created Async standard AI voice response mixin for {Interpreter.__name__}")

		self.listener = mic
		self.recogniser = sr.Recognizer()
		logger.debug(f"Created speech recongizer object for {Interpreter.__name__}")
	
	def __del__(self):
		try:
			del self.listener
			del self.recogniser
			# self.engine.tearDown()
		except AttributeError:
			pass
		
	def adjust_for_ambient_noise(self):
		logger.debug("Calibrating Mic")
		with self.listener as source:
			self.recogniser.adjust_for_ambient_noise(source, duration = 0.3)
		
	def listen(self):
		if self.greetedUser():
			self.readySound()
		else:
			self.greet(block = True)
			self.offerHelp(block = True)

		try:
			with self.listener as source:
				try:					
					logger.info("Listening...")
					voice = self.recogniser.listen(source, timeout = 2.5, phrase_time_limit = 4)
					
					logger.debug("Voice received")
					command	= self.transcribe(voice)					
					logger.debug("Transcribed voice")
					command = command.strip().lower()
					logger.info(f"Detected command: {command}")
				except sr.WaitTimeoutError:
					logger.info("User didn't speak")
					command = Interpreter.FAILED_TOKEN
				
		except sr.UnknownValueError:
			logger.debug("Couldn't detect voice")
			command = Interpreter.FAILED_TOKEN
			
		event, data = self.interpret(command)
		logger.info(f"Event: {event}, Data: {data}")
		
		return event, data
		
	def transcribe(self, audio):
		try:
			command = self.recogniser.recognize_google(audio)
			logger.info("Used Google online transcription service")
		except sr.RequestError:
			logger.warning("Internet unavailable. Using offline TTS")
			command = self.recogniser.recognize_sphinx(audio)
			logger.info("Used Sphinx offline transcription service")

		logger.info(f"Transcription: {command}")
		return command
				
	def interpret(self, command):
		'''Break down the command into Event and data objects'''
		event = DefaultCommand.__name__
		data = None
		if re.search("^shutdown.*(computer$|system$)", command):
			logger.info("Detected shutdown command")
			event = ShutdownSystem.__name__
		elif re.search("(^youtube.*)|(.*(on youtube)$)", command):
			logger.info("User command contains Youtube")
			if re.search("^play.*", command):
				command = re.sub("play", "", command)
			video = re.sub("on youtube", "", command)
			video = re.sub("youtube", "", video)
			logger.info(f"video: {video}")
			event = PlayYoutubeVideo.__name__
			data = video
		elif re.search("^play.*music$", command):
			logger.info("Detected offline music command: start")
			event = StartOfflineMusic.__name__
		elif re.search("^stop.*music$", command):
			logger.info("Detected offline music command: stop")
			event = StopOfflineMusic.__name__
		elif re.search("((^wiki|^wikipedia).*)|(.*(wiki$|wikipedia$))", command):
			logger.info(f"Detected wiki search: {command}")
			sub_command = command.replace("wikipedia","").strip()
			search = sub_command.replace("wiki","").strip()
			logger.info(f"Wiki search statement: {search}")
			event = WikiSearch.__name__
			data = search
		elif re.search("^google.*", command):
			logger.info(f"Detected google search")
			search = re.sub("google", "", command).strip()
			logger.info(f"Google search statement: {search}")
			event = GoogleSearch.__name__
			data = search
		elif re.search("^define", command):
			logger.info(f"Detected dictionary command: {command}")
			statement = re.sub("define", "", command).strip().split()
			lookUpWord = statement[0]
			logger.info(f"Look up word: {lookUpWord}")
			event = DefineWord.__name__
			data = lookUpWord
		elif re.search("^tell.*", command):
			if re.search(".*time$", command):
				logger.info("User is asking for time")
				event = TellTime.__name__
			elif re.search(".*joke$", command) or re.search(".*funny$", command):
				logger.info("User is asking for a joke")
				event = TellAJoke.__name__
		elif re.search("(^news.*)|(.*news$)", command):
			logger.info("User is asking for news")
			event = GetNews.__name__
		elif "goodbye" in command or "bye" in command or "bye-bye" in command:
			logger.info("Received command to terminate programme")
			event = StopProgram.__name__
		elif re.search("weather", command):
			logger.info("User is asking for weather forecast")
			event = GetWeatherForecast.__name__
		elif re.search("^lights", command):
			arg = command.replace("lights", "").strip().lower()
			if arg == "on":
				data = "1"
			elif arg == "off":
				data = "0"
			event = "lights"
		else:
			logger.warn("Detected unknown command")
			
		return event, data
		
		
