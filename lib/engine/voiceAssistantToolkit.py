import re
import os
import pyaudio
import random
import struct
import logging
import textwrap
import pvporcupine
import speech_recognition as sr
import wikipedia
import pyjokes
import pyttsx3
import newspaper
from multiprocessing import Process
from glob import glob
from collections import defaultdict


from datetime import datetime
from playsound import playsound
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
		self.voice = pyttsx3.init()
		self.voice.setProperty("rate", 170)
		
		self.systemConfig = systemConfig
		
		self.newsRecord = defaultdict(lambda : set())
		self.userPreference = userPreference
		self._musicProcess = None
		self.newsRecord["newspaper"] = newspaper.build(self.userPreference.NEWS_WEBSITE)
		
		self.setUp()
		
	def setUp(self):
		logging.debug(f"Loading {self.userPreference.AI_GENDER} AI")
		self.set_gender(self.userPreference.AI_GENDER[0])
		
	def tearDown(self):
		self.userPreference.save()
		logging.info("Saving User Preferences")
		if self._musicProcess != None:
			self._musicProcess.terminate()
			logging.debug("Terminated music process")
		
	def __del__(self):
		self.tearDown()
	
	def formatForPPrint(self, longStr):
		dedented_text = textwrap.dedent(longStr).strip()
		return textwrap.fill(dedented_text, width=self.systemConfig.PRINTED_TEXT_WIDTH)
	
	def setMaleAI(self):
		self.set_gender("m")
	
	def setFemaleAI(self):
		self.set_gender("f")

	def say(self, command):
		self.voice.say(command)
		self.voice.runAndWait()
	
	def set_gender(self, gender):
		voices = self.voice.getProperty('voices')
		if gender.lower() == "m":
			self.voice.setProperty('voice', voices[0].id)
			self.userPreference.AI_GENDER = "male"
		elif gender.lower() == "f":
			self.voice.setProperty('voice', voices[1].id)
			self.userPreference.AI_GENDER = "female"
			
	def readySoundEffect(self):
		playsound(self.systemConfig.ATTENTION_SOUND, block = False) # non-blocking playback not supported for linux

	def execute(self, command):
		if self.systemConfig.UNKNOWN_TOKEN in command or self.systemConfig.FAILED_TOKEN in command:
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
		elif re.search("^google.*", command):
			statement = re.sub("google", "", command)
			self.say(f"OK. Searching for {search} on Google")
			googleSearchFor(statement)
		elif re.search("^tell.*", command):
			logging.debug("Detected 'tell' in command")
			if re.search(".*time$", command):
				logging.debug("Detected 'time' in command")
				time = datetime.now().strftime('%I:%M %p')
				msg = f'Current time is {time}'
				print(msg)
				self.say(msg)
			elif re.search(".*joke$", command) or re.search(".*funny$", command):
				joke = pyjokes.get_joke()
				#TODO: handle network erorr and cache jokes
				print(joke)
				self.say(joke)
		elif re.search("(^news.*)|(.*news$)", command):
			newNews = [article for article in self.newsRecord["newspaper"].articles if article.url not in self.newsRecord["readBefore"]]

			try:
				selectedNews = random.sample(newNews, self.userPreference.NUM_ARTICLES_PER_NEWS_QUERY)
			except ValueError:
				selectedNews = newNews
				if len(selectedNews) == 0:
					self.say("The online news website may have blocked my request. So I'm unable to query for the latest news")
					return


			self.say(f"No problem. Bringing you {len(selectedNews)} articles")

			for article in selectedNews:
				article.download()
				logging.debug("Downloaded article")
				article.parse()
				logging.debug("Parsed article")
				article.nlp()
				logging.debug("NLP article")

				print(f"Title : {article.title}\n")
				print(f"Authors: {', '.join(article.authors)}\n")
				self.say(article.title)
				# print(f"Summary : {article.summary}\n")
				print(self.formatForPPrint(article.summary))

				self.say(article.summary)
				print(f"\nSource: {article.url}\n")
				if len(article.movies) > 0:
					print(f"Video links: {article.movies}\n")
				

				self.newsRecord["readBefore"].add(article.url)
			
			self.say("That's all for now. Ping me again if you wanna hear more news of the day")
		elif "female assistant" in command:
			logging.debug("Detected 'a female assistant' in command")
			self.setFemaleAI()
			playsound(self.systemConfig.ATTENTION_SOUND)	
		elif "male assistant" in command:
			logging.debug("Detected 'a male assistant' in command")
			self.setMaleAI()
			playsound(self.systemConfig.ATTENTION_SOUND)
		elif "goodbye" in command or "bye" in command or "bye-bye" in command:
			logging.debug("Detected 'goodbye' or 'bye' in command")
			logging.info("Exiting programme")
			playsound(self.systemConfig.SWITCH_OFF_SOUND)
			exit()
		else:
			logging.debug("Detected a search command")
			if re.search("((^wiki|^wikipedia).*)|(.*(wiki$|wikipedia$))", command):
				sub_command = command.replace("wikipedia","").strip()
				sub_command = sub_command.replace("wiki","").strip()
			else:
				self.say("Sorry, I don't understand that command.")
				return
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
	



class Bot:
	def __init__(self, 
			systemConfig = None, 
			userPreference = None, 
			mic = sr.Microphone()):
		self.listener = mic
		self.recogniser = sr.Recognizer()
		self.engine = Engine(systemConfig, userPreference)
	
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
		

if __name__ == "__main__":
	from config import engineConfig
	from time import sleep
	from playsound import playsound
	import os
	musicLibrary = engineConfig["MUSIC_PATH"]
	systemMusic = os.listdir(musicLibrary)
	music = systemMusic[0]
	path2song = musicLibrary + "\\" + music
	print(path2song)
	song = pyglet.media.load(path2song)
	player = pyglet.media.Player()
	player.queue(song)
	
	player.play()
	sleep(300)	

		# elif re.search("(^news|news$)|(newspaper)", command):
		# 	url='https://www.straitstimes.com/'
		# 	numArticles = 2
			
		# 	paper = newspaper.build(url)
		# 	logging.debug("Starting articles download")
		# 	for article in paper.articles[:numArticles]:
		# 		article.download()
		# 		logging.debug("Downloaded article")
		# 		article.parse()
		# 		logging.debug("Parsed article")
		# 		article.nlp()
		# 		logging.debug("NLP-ed article")

		# 		print(f"Title : {article.title}\n")
		# 		print(f"Authors: {article.authors}\n")
		# 		print(f"Summary : {article.summary}\n")
		# 		print(f"Video links : {article.movies}\n")
		# 		print(f"Article links : {article.url}")
		# 		# print(f"Keywords : {article.keywords}\n")
		