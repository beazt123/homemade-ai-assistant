import re
import os
import json
import pyaudio
import random
import struct
import requests
import logging
import textwrap
import pvporcupine
import speech_recognition as sr
import wikipedia
import pyjokes
import pyttsx3
import newspaper
import subprocess
import time
from PyDictionary import PyDictionary
from nltk import sent_tokenize

from multiprocessing import Process
from glob import glob
from collections import defaultdict
from datetime import datetime
from playsound import playsound

from ..constants import FAILED_TOKEN, UNKNOWN_TOKEN
from ..utils import playOnYoutube, googleSearchFor, playPlaylist, generateAllMusicFiles


class WakeWordDetector:
	def __init__(self):
		pa = pyaudio.PyAudio()
		self.wake_words = pvporcupine.KEYWORDS
		
		self.porcupine = pvporcupine.create(keywords = self.wake_words)
		self.audio_stream = pa.open(
			rate = self.porcupine.sample_rate,
			channels = 1,
			format = pyaudio.paInt16,
			input = True,
			frames_per_buffer = self.porcupine.frame_length)
	
	def show_wake_words(self):
		return self.wake_words
		
	def waitForWakeWord(self):
		while True:
			pcm = self.audio_stream.read(self.porcupine.frame_length)
			pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

			result = self.porcupine.process(pcm)	
			if result >= 0:
				logging.info('[%s] Detected %s' % (str(datetime.now()), list(pvporcupine.KEYWORDS)[result]))
				break

		# self.porcupine.delete()
		# print("Resources deleted")

class Engine:	
	def __init__(self, systemConfig, userPreference = None):
		self.newsRecord = defaultdict(lambda : set())
		
		
		self.systemConfig = systemConfig
		self.userPreference = userPreference
		
		
		self._onlineEngDict = PyDictionary()
		self._offlineEngDict = None
		self._musicProcess = None
		self._voice = pyttsx3.init()
		self._voice.setProperty("rate", 170)
		
		
		self.setUp()
		playsound(self.systemConfig.LEVEL_UP_SOUND, block = False)
		
	def setUp(self):
		logging.debug(f"Loading {self.userPreference.AI_GENDER} AI")
		self.set_gender(self.userPreference.AI_GENDER[0])
		
		
		# self.newsRecord["newspaper"] = newspaper.build(self.userPreference.NEWS_WEBSITE)
		
		with open(self.systemConfig.JSON_DICTIONARY_NAME) as f:
			self._offlineEngDict = json.load(f)
		
	def tearDown(self):
		self.userPreference.save()
		logging.info("Saving User Preferences")
		if self._musicProcess != None:
			self._musicProcess.terminate()
			logging.debug("Terminated music process")
		
	def __del__(self):
		self.tearDown()
		
	def formatForPPrint(self, printStatements, indent = ""):
		paragraphed = textwrap.fill(printStatements.strip(), 
									width=self.systemConfig.PRINTED_TEXT_WIDTH)
		return textwrap.indent(paragraphed, prefix=indent)
	
	def setMaleAI(self):
		self.set_gender("m")
	
	def setFemaleAI(self):
		self.set_gender("f")

	def say(self, command):
		self._voice.say(command)
		self._voice.runAndWait()
	
	def set_gender(self, gender):
		voices = self._voice.getProperty('voices')
		if gender.lower() == "m":
			self._voice.setProperty('voice', voices[0].id)
			self.userPreference.AI_GENDER = "male"
		elif gender.lower() == "f":
			self._voice.setProperty('voice', voices[1].id)
			self.userPreference.AI_GENDER = "female"
			
	def readySoundEffect(self):
		playsound(self.systemConfig.ATTENTION_SOUND, block = False) # non-blocking playback not supported for linux

	def execute(self, command):
		if UNKNOWN_TOKEN in command or FAILED_TOKEN in command:
			logging.info("Unknown or failed command detected")
			playsound(self.systemConfig.AT_EASE_SOUND, block = False)
		elif re.search("^shutdown.*(computer$|system$)", command):
			logging.info("Shutting down system")
			self.say("Alright. Shutting down your computer right now.")
			os.system("shutdown /s /t 1") 
		elif re.search("(^youtube.*)|(.*(on youtube)$)", command):
			if re.search("^play.*", command):
				command = re.sub("play", "", command)
			logging.debug("Detected 'youtube' in command")
			video = re.sub("on youtube", "", command)
			video = re.sub("youtube", "", video)
			logging.debug(video)
			self.say(f"Ok. Playing {video} on YouTube.")
			playOnYoutube(video)
		elif re.search("^play.*music$", command):
			musicLibrary = self.userPreference.PATH_TO_LOCAL_MUSIC_FOLDER
			systemMusic = glob(os.path.join(musicLibrary, "*.mp3"))#os.listdir(musicLibrary)
			
			
			random.shuffle(systemMusic)
			
			self.say("Ok. Playing music from your music library in shuffle mode")
			logging.debug(systemMusic)
			playlist = systemMusic
			# playlist = [os.path.join(musicLibrary, music) for music in systemMusic]
			if len(playlist) == 0:
				logging.warn("No music found in specified directory. Scanning the computer for music")
				playlist = generateAllMusicFiles()
				
				
			logging.debug("Playing first song")
			self._musicProcess = Process(target=playPlaylist, args=(playlist,))
			self._musicProcess.daemon = True
			logging.debug("Created process to play music")
			self._musicProcess.start()
			logging.debug("Started process to play music")
		elif re.search("^stop.*music$", command):
			self._musicProcess.terminate()
			del self._musicProcess
			logging.debug("Terminated music process")
		elif re.search("((^wiki|^wikipedia).*)|(.*(wiki$|wikipedia$))", command):
			sub_command = command.replace("wikipedia","").strip()
			sub_command = sub_command.replace("wiki","").strip()
			try:
				info = wikipedia.summary(sub_command, 2)
				print(self.formatForPPrint(info))
				self.say(info)
			except wikipedia.DisambiguationError:
				logging.error("Wikipedia error")
				self.say("Sorry, there were quite many possible searches. \
					Mind if you be more specific in your search terms? Thanks!")
			except wikipedia.exceptions.PageError:
				logging.error("Wikipedia error")
				self.say(f"Sorry, there are no matching searches for {sub_command}")
		elif re.search("^google.*", command):
			statement = re.sub("google", "", command).strip()
			self.say(f"OK. Searching for {statement} on Google")
			googleSearchFor(statement)
		elif re.search("^define", command):
			statement = re.sub("define", "", command).strip().split()
			lookUpWord = statement[0]
			onlineSearchResult = self._onlineEngDict.meaning(lookUpWord)
			wordToPrint = f"WORD: {lookUpWord}"
			print(wordToPrint)
			print("=" * len(f"WORD: {lookUpWord}\n"))
			self.say(lookUpWord)
			
			if onlineSearchResult == None:
				logging.warn("Word not found in dictionary or internet connection is down. Reverting to offline dictionary")
				offlineSearchResult = self._offlineEngDict.get(lookUpWord, None)
				
				if offlineSearchResult == None:
					logging.info("Word not found in offline and online dictionary")
					self.say("Your England very the powderful. Too powderful for me to find")
					
				script = sent_tokenize(offlineSearchResult)
				offlineSearchResult = re.sub("[0-9].", "\n- ", offlineSearchResult)
				offlineSearchResult = re.sub(";", "\n\t- ", offlineSearchResult)
				print(offlineSearchResult)
				self.say(script)
			
			for category, meanings in onlineSearchResult.items():
				print(f"{category}:")
				self.say(category)
				
				counter = 0
				
				for meaning in meanings:
					print(self.formatForPPrint(f"- {meaning}", indent="\t"))
					self.say(meaning)
					
					if counter > 5:
						break
				
				print()
		elif re.search("terminal$|(command prompt)$|(command line)$", command):
			self.say("Right away")
			logging.info("Launching terminal")
			subprocess.call(f'start {self.systemConfig.PATH_TO_POWERSHELL}', shell=True)
			logging.debug("Launched terminal")
		elif re.search("^tell.*", command):
			logging.debug("Detected 'tell' in command")
			if re.search(".*time$", command):
				logging.debug("Detected 'time' in command")
				timeNow = datetime.now().strftime('%I:%M %p')
				msg = f'Current time is {timeNow}'
				print(msg)
				self.say(msg)
			elif re.search(".*joke$", command) or re.search(".*funny$", command):
				joke = pyjokes.get_joke()
				#TODO: handle network erorr and cache jokes
				print(joke)
				self.say(joke)
		elif re.search("(^news.*)|(.*news$)", command):
			if self.newsRecord["newspaper"] == set():
				logging.info("Lazy loading newspaper articles")
				self.newsRecord["newspaper"] = newspaper.build(self.userPreference.NEWS_WEBSITE)
				if len(self.newsRecord["newspaper"].articles) == 0:
					logging.error("Could not load the newspaper articles")
					self.say("The online news website may have blocked my request. So I'm unable to query for the latest news")
					return
					
			newNews = [article for article in self.newsRecord["newspaper"].articles if article.url not in self.newsRecord["readBefore"]]

			try:
				selectedNews = random.sample(newNews, self.userPreference.NUM_ARTICLES_PER_NEWS_QUERY)
			except ValueError:
				selectedNews = newNews
				if len(selectedNews) == 0:
					self.say("I have no more news for today")
					return			

			self.say(f"No problem. Bringing you {len(selectedNews)} articles")

			for article in selectedNews:
				article.download()
				logging.debug("Downloaded article")
				article.parse()
				logging.debug("Parsed article")
				article.nlp()
				logging.debug("NLP article")

				title = f"Title : {article.title}"
				print(title)
				print("=" * len(title))
				
				if len(article.authors) > 0:
					authors = article.authors
					authors = ', '.join(authors)
				else:
					authors = "UNKNOWN"
				print(f"Authors: {authors}\n")
				
				self.say(article.title)
				# print(f"Summary : {article.summary}\n")
				print(self.formatForPPrint(article.summary, indent="\t"))

				self.say(article.summary)
				print(f"\nSource: {article.url}\n")
				if len(article.movies) > 0:
					print(f"Video links: {article.movies}\n")
				

				self.newsRecord["readBefore"].add(article.url)
			
			self.say("That's all for now. Ping me again if you wanna hear more news of the day")
		elif "female assistant" in command:
			logging.debug("Detected 'a female assistant' in command")
			self.setFemaleAI()
			playsound(self.systemConfig.QUICK_PROCESSING_SOUND)	
		elif "male assistant" in command:
			logging.debug("Detected 'a male assistant' in command")
			self.setMaleAI()
			playsound(self.systemConfig.QUICK_PROCESSING_SOUND)
		elif "goodbye" in command or "bye" in command or "bye-bye" in command:
			logging.debug("Detected 'goodbye' or 'bye' in command")
			logging.info("Exiting programme")
			playsound(self.systemConfig.SWITCH_OFF_SOUND)
			exit()
		elif re.search("weather", command):
			r = requests.get(self.systemConfig.WEATHER_API_BASE_URL, 
					params = self.systemConfig.WEATHER_QUERY_PARAMS)
			
			# getting the main dict block
			if r.status_code == 200:
				data = r.json()
				hourlyWeather = data['hourly']
				now = time.time()
				hr = 3600
				title = "Weather Forecast"
				print(title)
				print("=" * len(title))
				for hoursLater in range(0, 13, 3):
					laterTimeStamp = now + hoursLater * hr
					later = list(filter(lambda x : x["dt"] > laterTimeStamp, hourlyWeather))[0]
					formattedTimeLater = datetime.fromtimestamp(laterTimeStamp).strftime('%I:%M %p')
					
					print(formattedTimeLater)
					self.say(f"Weather at {formattedTimeLater}")
					
					apparentTemperature = round(later["feels_like"], 1)
					desc = later["weather"][0]["description"].title()
					humidity = later['humidity']
					
					logging.debug(f"apparentTemperature: {apparentTemperature}")
					
					announcementScript = "\n".join([
							f'{desc}',
							f"Apparent temperature at {apparentTemperature} degrees Celsius",
							f"Humidity at {humidity} percent"				
							])
					announcementPrintStmt = announcementScript.replace("Celsius", "C").replace(" degrees", "").replace("percent", "%").replace(" at", ":")
					
					logging.debug(f"announcementPrintStmt: {announcementPrintStmt}")
					
					print(textwrap.indent(announcementPrintStmt, prefix="\t"))		
					self.say(announcementScript)
					
			elif r.status_code == 401:
				self.say("Sorry, no authentication provided. I couldn't log in.")
			else:
				self.say("Why don't stick your head out the window?")
		else:
			self.say("Sorry, I don't understand that command.")
			return



class Bot:
	def __init__(self, mic, engine):
		self.listener = mic
		self.recogniser = sr.Recognizer()
		self.engine = engine
	
	def __del__(self):
		try:
			del self.listener
			del self.recogniser
			self.engine.tearDown()
		except AttributeError:
			pass
		
	def adjust_for_ambient_noise(self):
		logging.debug("Calibrating Mic")
		with self.listener as source:
			self.recogniser.adjust_for_ambient_noise(source, duration = 0.3)
		
	def listen(self):
		self.engine.readySoundEffect()
		try:
			with self.listener as source:
				try:					
					logging.info("Listening...")
					voice = self.recogniser.listen(source, timeout = 2.5, phrase_time_limit = 4)
					logging.debug("Actually listening")
					
					logging.debug("Voice received")
					command	= self.transcribe(voice)					
					logging.debug("Transcribed voice")
					command = command.strip().lower()
					logging.debug(f"Detected command: {command}")
				except sr.WaitTimeoutError:
					logging.info("User didn't speak")
					command = FAILED_TOKEN
				
		except sr.UnknownValueError:
			logging.info("Couldn't detect voice")
			command = UNKNOWN_TOKEN
			
		self.engine.execute(command)
		
	def transcribe(self, audio):
		try:
			command = self.recogniser.recognize_google(audio)
			logging.debug("Using Google online transcription service")
		except sr.RequestError:
			logging.warning("Internet unavailable. Using offline TTS")
			command = self.recogniser.recognize_sphinx(audio)
			logging.debug("Using Sphinx offline transcription service")

		logging.info(command)
		return command
		

		