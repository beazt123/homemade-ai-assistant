import logging
import speech_recognition as sr
from lib.receivers.mixins.soundEffectsMixin import SoundEffectsMixin
from lib.receivers.mixins.asyncStdVoiceResponseMixin import AsyncStdVoiceResponseMixin
from abc import ABC, abstractmethod





class Interpreter(SoundEffectsMixin, AsyncStdVoiceResponseMixin, ABC):
	logger = logging.getLogger(__name__)
	FAILED_TOKEN = "!FAILED"

	def __init__(self, config, soundEngine, mic):
		Interpreter.logger.info(f"Creating Sound effects mixin for {Interpreter.__name__}")
		SoundEffectsMixin.__init__(self, config, soundEngine)
		Interpreter.logger.info(f"Created effects mixin for {Interpreter.__name__}")

		Interpreter.logger.info(f"Creating Async standard AI voice response mixin for {Interpreter.__name__}")
		AsyncStdVoiceResponseMixin.__init__(self, config, soundEngine)
		Interpreter.logger.info(f"Created Async standard AI voice response mixin for {Interpreter.__name__}")

		self.listener = mic
		self.recogniser = sr.Recognizer()
		Interpreter.logger.debug(f"Created speech recongizer object for {Interpreter.__name__}")
		
	
	def __del__(self):
		try:
			del self.listener
			del self.recogniser
			# self.engine.tearDown()
		except AttributeError:
			pass
		
	def adjust_for_ambient_noise(self):
		Interpreter.logger.debug("Calibrating Mic")
		with self.listener as source:
			self.recogniser.adjust_for_ambient_noise(source, duration = 0.3)
		
	def listenAndTranscribe(self):
		try:
			with self.listener as source:
				try:					
					Interpreter.logger.info("Listening...")
					voice = self.recogniser.listen(source, timeout = 2.5, phrase_time_limit = 4)
					
					Interpreter.logger.debug("Voice received")
					command	= self.transcribe(voice)				
					Interpreter.logger.debug("Transcribed voice")
					command = command.strip().lower()
					Interpreter.logger.info(f"Detected command: {command}")
				except sr.WaitTimeoutError:
					Interpreter.logger.info("User didn't speak")
					command = Interpreter.FAILED_TOKEN
		except sr.UnknownValueError:
			Interpreter.logger.debug("No voice detected")
			command = Interpreter.FAILED_TOKEN
		
		return command

	def interpret(self):
		if self.greetedUser():
			self.readySound()
		else:
			self.greet(block = True)
			self.offerHelp(block = True)

		command = self.listenAndTranscribe()
		event, data = self.process(command)
		Interpreter.logger.info(f"Event: {event}, Data: {data}")
		
		return event, data
		
	def transcribe(self, audio):
		try:
			command = self.recogniser.recognize_google(audio)
			Interpreter.logger.info("Used Google online transcription service")
		except sr.RequestError:
			Interpreter.logger.warning("Internet unavailable. Using offline TTS")
			command = self.recogniser.recognize_sphinx(audio)
			Interpreter.logger.info("Used Sphinx offline transcription service")

		Interpreter.logger.info(f"Transcription: {command}")
		return command

	@classmethod
	@abstractmethod			
	def process(cls, command):
		'''Break down the command into Event and data objects'''
		pass		
