import re
import logging
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
	StopProgram,
	TellAJoke,
	TellTime,
	WikiSearch,
	DefaultCommand
)

class RegexInterpreter(Interpreter):
	logger = logging.getLogger(__name__)

	@classmethod
	def process(cls, command):
		event = DefaultCommand.__name__
		data = None
		if re.search("^(shut down).*(computer$|system$)", command):
			cls.logger.info("Detected shutdown command")
			event = ShutdownSystem.__name__
		elif re.search("(^youtube.*)|(.*(on youtube)$)", command):
			cls.logger.info("User command contains Youtube")
			if re.search("^play.*", command):
				command = re.sub("play", "", command)
			video = re.sub("on youtube", "", command)
			video = re.sub("youtube", "", video)
			cls.logger.info(f"video: {video}")
			event = PlayYoutubeVideo.__name__
			data = video
		elif re.search("^play.*music$", command):
			cls.logger.info("Detected offline music command: start")
			event = StartOfflineMusic.__name__
		elif re.search("^stop.*music$", command):
			cls.logger.info("Detected offline music command: stop")
			event = StopOfflineMusic.__name__
		elif re.search("((^wiki|^wikipedia).*)|(.*(wiki$|wikipedia$))", command):
			cls.logger.info(f"Detected wiki search: {command}")
			sub_command = command.replace("wikipedia","").strip()
			search = sub_command.replace("wiki","").strip()
			cls.logger.info(f"Wiki search statement: {search}")
			event = WikiSearch.__name__
			data = search
		elif re.search("^google.*", command):
			cls.logger.info(f"Detected google search")
			search = re.sub("google", "", command).strip()
			cls.logger.info(f"Google search statement: {search}")
			event = GoogleSearch.__name__
			data = search
		elif re.search("^define", command):
			cls.logger.info(f"Detected dictionary command: {command}")
			statement = re.sub("define", "", command).strip().split()
			lookUpWord = statement[0]
			cls.logger.info(f"Look up word: {lookUpWord}")
			event = DefineWord.__name__
			data = lookUpWord
		elif re.search("^tell.*", command):
			if re.search(".*time$", command):
				cls.logger.info("User is asking for time")
				event = TellTime.__name__
			elif re.search(".*joke$", command) or re.search(".*funny$", command):
				cls.logger.info("User is asking for a joke")
				event = TellAJoke.__name__
		elif re.search("(^news.*)|(.*news$)", command):
			cls.logger.info("User is asking for news")
			event = GetNews.__name__
		elif "goodbye" in command or "bye" in command or "bye-bye" in command:
			cls.logger.info("Received command to terminate programme")
			event = StopProgram.__name__
		elif re.search("weather", command):
			cls.logger.info("User is asking for weather forecast")
			event = GetWeatherForecast.__name__
		elif re.search("cool lights", command):
			cls.logger.info("User wants to switch on the cool lights")
			event = "/lights/cool"
			state = command.replace("cool lights", "").strip().lower()
			if state == "off":
				data = "0"
			else:
				data = "1"
		elif re.search("warm lights", command):
			cls.logger.info("User wants to switch on the warm lights")
			event = "/lights/warm"
			state = command.replace("warm lights", "").strip().lower()
			if state == "off":
				data = "0"
			else:
				data = "1"
		else:
			cls.logger.warn("Detected unknown command")
			
		return event, data