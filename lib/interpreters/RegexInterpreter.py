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


	def interpret(self, command):
		event = DefaultCommand.__name__
		data = None
		if re.search("^shutdown.*(computer$|system$)", command):
			RegexInterpreter.logger.info("Detected shutdown command")
			event = ShutdownSystem.__name__
		elif re.search("(^youtube.*)|(.*(on youtube)$)", command):
			RegexInterpreter.logger.info("User command contains Youtube")
			if re.search("^play.*", command):
				command = re.sub("play", "", command)
			video = re.sub("on youtube", "", command)
			video = re.sub("youtube", "", video)
			RegexInterpreter.logger.info(f"video: {video}")
			event = PlayYoutubeVideo.__name__
			data = video
		elif re.search("^play.*music$", command):
			RegexInterpreter.logger.info("Detected offline music command: start")
			event = StartOfflineMusic.__name__
		elif re.search("^stop.*music$", command):
			RegexInterpreter.logger.info("Detected offline music command: stop")
			event = StopOfflineMusic.__name__
		elif re.search("((^wiki|^wikipedia).*)|(.*(wiki$|wikipedia$))", command):
			RegexInterpreter.logger.info(f"Detected wiki search: {command}")
			sub_command = command.replace("wikipedia","").strip()
			search = sub_command.replace("wiki","").strip()
			RegexInterpreter.logger.info(f"Wiki search statement: {search}")
			event = WikiSearch.__name__
			data = search
		elif re.search("^google.*", command):
			RegexInterpreter.logger.info(f"Detected google search")
			search = re.sub("google", "", command).strip()
			RegexInterpreter.logger.info(f"Google search statement: {search}")
			event = GoogleSearch.__name__
			data = search
		elif re.search("^define", command):
			RegexInterpreter.logger.info(f"Detected dictionary command: {command}")
			statement = re.sub("define", "", command).strip().split()
			lookUpWord = statement[0]
			RegexInterpreter.logger.info(f"Look up word: {lookUpWord}")
			event = DefineWord.__name__
			data = lookUpWord
		elif re.search("^tell.*", command):
			if re.search(".*time$", command):
				RegexInterpreter.logger.info("User is asking for time")
				event = TellTime.__name__
			elif re.search(".*joke$", command) or re.search(".*funny$", command):
				RegexInterpreter.logger.info("User is asking for a joke")
				event = TellAJoke.__name__
		elif re.search("(^news.*)|(.*news$)", command):
			RegexInterpreter.logger.info("User is asking for news")
			event = GetNews.__name__
		elif "goodbye" in command or "bye" in command or "bye-bye" in command:
			RegexInterpreter.logger.info("Received command to terminate programme")
			event = StopProgram.__name__
		elif re.search("weather", command):
			RegexInterpreter.logger.info("User is asking for weather forecast")
			event = GetWeatherForecast.__name__
		else:
			RegexInterpreter.logger.warn("Detected unknown command")
			
		return event, data