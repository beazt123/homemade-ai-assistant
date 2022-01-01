import logging
import speech_recognition as sr
from lib.receivers.soundEffectsMixin import SoundEffectsMixin
from lib.receivers.asyncStdVoiceResponseMixin import AsyncStdVoiceResponseMixin
from abc import ABC, abstractmethod




logger = logging.getLogger(__name__)

class Interpreter(SoundEffectsMixin, AsyncStdVoiceResponseMixin, ABC):
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

	@abstractmethod			
	def interpret(self, command):
		'''Break down the command into Event and data objects'''
		pass
		
		
		
