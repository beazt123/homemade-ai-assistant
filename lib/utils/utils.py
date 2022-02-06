import os
import yaml
import webbrowser as web
import logging
import requests
from glob import iglob
from configparser import ConfigParser
from itertools import chain
from playsound import playsound, PlaysoundException

logger = logging.getLogger(__name__)


def playPlaylist(playlist):
	logger.info("Starting playlist")
	for song in playlist:
		logger.info(f"Attempting to play {song}")
		try:
			playsound(song)
			logger.debug(f"Played {song}")
		except PlaysoundException:
			logger.error("MCI error. Skipping current song")
		except:
			logger.exception("Unknown error")
		
	logger.info("Done playing playlist")

def playOnYoutube(topic: str):
	"""Play a YouTube Video"""


	url = "https://www.youtube.com/results?q=" + topic
	count = 0
	cont = requests.get(url)
	data = cont.content
	data = str(data)
	lst = data.split('"')
	for i in lst:
		count += 1
		if i == "WEB_PAGE_TYPE_WATCH":
			break
		if lst[count - 5] == "/results":
			raise Exception("No Video Found for this Topic!")

	web.open("https://www.youtube.com" + lst[count - 5])
	
	
def googleSearchFor(topic: str) -> None:
	"""Searches About the Topic on Google"""

	link = "https://www.google.com/search?q={}".format(topic)
	web.open(link)
	
	
def generateAllMusicFiles(exts = ["mp3"]):
	homeDrive = os.getenv("HOMEDRIVE")
	homePath = os.getenv("HOMEPATH")
	homeFullPath = os.path.join(homeDrive, homePath)
	
	
	generatorList = [iglob(os.path.join(homeFullPath,f"**/*.{ext}"), recursive=True) for ext in exts]
	
	generator = chain(*generatorList)
	
	return generator
		
def getSetUpConfig(filepath):
	with open(filepath, 'r') as stream:
		dictionary = yaml.safe_load(stream)
		
	return dictionary

def getConfig(*filepaths):
	configParser = ConfigParser()
	for filepath in filepaths:
		configParser.read(filepath)
	
	return configParser