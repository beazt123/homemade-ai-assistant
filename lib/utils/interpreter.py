import re
import logging
import speech_recognition as sr
from lib.receivers.soundEffectsMixin import SoundEffectsMixin

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


class Interpreter(SoundEffectsMixin):
	FAILED_TOKEN = "!FAILED"

	def __init__(self, config, mic):
		SoundEffectsMixin.__init__(self, config)
		self.listener = mic
		self.recogniser = sr.Recognizer()
	
	def __del__(self):
		try:
			del self.listener
			del self.recogniser
			# self.engine.tearDown()
		except AttributeError:
			pass
		
	def adjust_for_ambient_noise(self):
		logging.debug("Calibrating Mic")
		with self.listener as source:
			self.recogniser.adjust_for_ambient_noise(source, duration = 0.3)
		
	def listen(self):
		self.readySound()
		try:
			with self.listener as source:
				try:					
					logging.info("Listening...")
					voice = self.recogniser.listen(source, timeout = 2.5, phrase_time_limit = 4)
					
					logging.debug("Voice received")
					command	= self.transcribe(voice)					
					logging.debug("Transcribed voice")
					command = command.strip().lower()
					logging.debug(f"Detected command: {command}")
				except sr.WaitTimeoutError:
					logging.info("User didn't speak")
					command = Interpreter.FAILED_TOKEN
				
		except sr.UnknownValueError:
			logging.info("Couldn't detect voice")
			command = Interpreter.FAILED_TOKEN
			
		event, data = self.interpret(command)
		logging.info(f"Event: {event}, Data: {data}")
		
		return event, data
		
	def transcribe(self, audio):
		try:
			command = self.recogniser.recognize_google(audio)
			logging.debug("Using Google online transcription service")
		except sr.RequestError:
			logging.warning("Internet unavailable. Using offline TTS")
			command = self.recogniser.recognize_sphinx(audio)
			logging.debug("Using Sphinx offline transcription service")

		logging.info(f"Transcription: {command}")
		return command
				
	def interpret(self, command):
		'''Break down the command into Event and data objects'''
		# TODO: if possible NLP, NER should go into here as well
		event = None
		data = None
		if re.search("^shutdown.*(computer$|system$)", command):
			logging.info("Detected shutdown command")
			event = ShutdownSystem.__name__
		elif re.search("(^youtube.*)|(.*(on youtube)$)", command):
			logging.info("Detected 'youtube' in command")
			if re.search("^play.*", command):
				command = re.sub("play", "", command)
			video = re.sub("on youtube", "", command)
			video = re.sub("youtube", "", video)
			logging.debug(f"video: {video}")
			event = PlayYoutubeVideo.__name__
			data = video
		elif re.search("^play.*music$", command):
			logging.info("Detected offline music command: start")
			event = StartOfflineMusic.__name__
		elif re.search("^stop.*music$", command):
			logging.info("Detected offline music command: stop")
			event = StopOfflineMusic.__name__
		elif re.search("((^wiki|^wikipedia).*)|(.*(wiki$|wikipedia$))", command):
			logging.info("Detected wiki search command")
			sub_command = command.replace("wikipedia","").strip()
			search = sub_command.replace("wiki","").strip()
			event = WikiSearch.__name__
			data = search
		elif re.search("^google.*", command):
			logging.info("Detected google search command")
			search = re.sub("google", "", command).strip()
			event = GoogleSearch.__name__
			data = search
		elif re.search("^define", command):
			logging.info("Detected dictionary command")
			statement = re.sub("define", "", command).strip().split()
			lookUpWord = statement[0]
			event = DefineWord.__name__
			data = lookUpWord
		# elif re.search("terminal$|(command prompt)$|(command line)$", command):
		# 	logging.info("Detected terminal command")
		# 	event = "terminal"
		# 	data = None
		elif re.search("^tell.*", command):
			logging.info("Detected 'tell' in command")
			if re.search(".*time$", command):
				logging.info("Detected 'time' in command")
				event = TellTime.__name__
			elif re.search(".*joke$", command) or re.search(".*funny$", command):
				logging.info("Detected 'joke/funny' in command")
				event = TellAJoke.__name__
		elif re.search("(^news.*)|(.*news$)", command):
			logging.info("Detected news command")
			event = GetNews.__name__
		elif "goodbye" in command or "bye" in command or "bye-bye" in command:
			logging.info("Detected 'goodbye' or 'bye' in command")
			event = StopProgram.__name__
		elif re.search("weather", command):
			logging.info("Detected weather command")
			event = GetWeatherForecast.__name__
		else:
			logging.warn("Detected unknown command")
			event = DefaultCommand.__name__
		return event, data
		
		
