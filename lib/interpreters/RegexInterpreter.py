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
from pvporcupine import KEYWORDS

README = \
"""
A.I general assistant
===========================
Wake words:
	Please say any 1 of the following words to wake the assistant:
		{wakewords}
		
Command words:

	GOOGLE/YOUTUBE/WIKI: 
		Performs a search on your browser for Google & Youtube.
		Wiki searches will show here with audio response.
		
		I.e. Say "google most recommended reed diffuser"
			 Say "youtube bloodstream ed sheeran"
			 Say "wiki Donald Trump"
		
	PLAY / STOP...MUSIC:
		Plays a random music on a pre-set directory
		I.e. Say "play some music" or
			say "play the music" or 
			say "stop the music" or
			say "stop playing the music"
			
	... WEATHER ...:
		Gives you a 12 hr weather forecast in 3-hr blocks.
		I.e. "Weather forecast" or
			 "How's the weather today?"
			
	... NEWS ...:
		Brings you summaries of the top 5 articles from a specified news site
		
	DEFINE <word>:
		Gives you the dictionary definition of a single word. 
		Works both offline and online.
		I.e. "Define apprehensive"
		
	TELL...TIME / JOKE:
		Tells you a joke or the time
		I.e. "tell me the time" or "tell time"
			"tell me a joke" or "tell a joke" or even "Tell joke"
		
	BYE-BYE:
		Closes this program.
		I.e. "goodbye" or "bye" or "bye-bye"
		
	SHUTDOWN COMPUTER:
		Shuts down the computer. Rmb to save your work!
		I.e. "shut down computer!"

""".format(wakewords=", \n\t\t".join(KEYWORDS))


class RegexInterpreter(Interpreter):
	logger = logging.getLogger(__name__)
	USER_GUIDE = README

	@classmethod
	def getUserGuide(cls):
		return cls.USER_GUIDE

	@classmethod
	def process(cls, command):
		event = DefaultCommand.__name__
		data = None
		if re.search("^shutdown.*(computer$|system$)", command):
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
		else:
			cls.logger.warn("Detected unknown command")
			
		return event, data