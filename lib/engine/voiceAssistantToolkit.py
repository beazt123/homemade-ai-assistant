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
import pyglet
import newspaper
from pickle import dump, load
from collections import defaultdict


from datetime import datetime
from playsound import playsound
from ..utils import playOnYoutube, googleSearchFor
from ..constants import UNKNOWN_TOKEN, FAILED_TOKEN

NEWS_FILE = "newsFile"
NEWS_WEBSITE = "https://www.straitstimes.com/"
NUM_ARTICLES = 5


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

class Bot:
	def __init__(self, name, mic, engine):
		self.name = name
		self.listener = mic
		self.recogniser = sr.Recognizer()
		self.engine = engine
	
	def __del__(self):
		del self.name
		del self.listener
		del self.recogniser
		del self.engine
		
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
					logging.debug("User didn't speak")
					command = FAILED_TOKEN
				
		except sr.UnknownValueError:
			logging.info("Couldn't detect voice")
			command = UNKNOWN_TOKEN
			
		self.engine.execute(command)
		
	def transcribe(self, audio):
		try:
			command = self.recogniser.recognize_google(audio)
		except sr.RequestError:
			logging.warning("Internet unavailable. Using offline TTS")
			command = self.recogniser.recognize_sphinx(audio)

		logging.debug(command)
		return command
		
class Engine:	
	def __init__(self, config = dict()):
		self.voice = pyttsx3.init()
		self.voice.setProperty("rate", 170)
		self.config = config
		self.newsRecord = defaultdict(lambda : set())
		# self.newsRecord["newspaper"] = newspaper.build(NEWS_WEBSITE)

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
		elif gender.lower() == "f":
			self.voice.setProperty('voice', voices[1].id)
			
	def readySoundEffect(self):
		playsound(self.config["sounds"]["ready"], block = False) # non-blocking playback not supported for linux

	def execute(self, command):
		if UNKNOWN_TOKEN in command or FAILED_TOKEN in command:
			logging.info("Unknown or failed command detected")
			playsound(self.config["sounds"]["atEase"], block = False)
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
			self.audioPlayer = pyglet.media.Player()
			musicLibrary = self.config["MUSIC_PATH"]
			systemMusic = os.listdir(musicLibrary)
			
			random.shuffle(systemMusic)
			
			self.say("Ok. Playing music from your music library in shuffle mode")
			logging.debug(systemMusic)
			for music in systemMusic:
				try:
					song = pyglet.media.load(os.path.join(musicLibrary, music))
					self.audioPlayer.queue(song)
				except pyglet.media.codecs.wave.WAVEDecodeException:
					pass

			
			self.audioPlayer.eos_action = self.audioPlayer.next_source
			self.audioPlayer.play()
		elif re.search("^stop.*music$", command):
			self.audioPlayer.pause()
			self.audioPlayer.delete()
			del self.audioPlayer
		elif re.search("^google.*", command):
			search = re.sub("google", "", command)
			self.say(f"OK. Searching for {search} on Google")
			googleSearchFor(search)
		elif re.search("^tell.*", command):
			logging.debug("Detected 'tell' in command")
			command = command.replace("?","")
			if re.search(".*time$", command):
				logging.debug("Detected 'time' in command")
				time = datetime.now().strftime('%I:%M %p')
				msg = 'Current time is ' + time
				print(msg)
				self.say(msg)
			elif re.search(".*joke$", command) or re.search(".*funny$", command):
				joke = pyjokes.get_joke()
				print(joke)
				self.say(joke)
		elif re.search("(^news.*)|(.*news$)", command):
			newNews = [article for article in self.newsRecord["newspaper"].articles if article.url not in self.newsRecord["readBefore"]]

			try:
				selectedNews = random.sample(newNews, NUM_ARTICLES)
			except ValueError:
				selectedNews = random.sample(newNews, len(newNews))
				if len(selectedNews) == 0:
					self.say("The online news website may have blocked my request. So I'm unable to query for the latest news. Why catch up with the news if all they have is bad news anyway")
					return


			self.say(f"No problem. Bringing you {NUM_ARTICLES} articles")

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
				dedented_text = textwrap.dedent(article.summary).strip()
				print(textwrap.fill(dedented_text, width=80))

				self.say(article.summary)
				print(f"Source: {article.url}\n")
				print(f"Video links: {article.movies}\n")
				

				self.newsRecord["readBefore"].add(article.url)
			
			self.say("That's all for now. Ping me again if you wanna hear more news of the day")
		elif "female assistant" in command:
			logging.debug("Detected 'a female assistant' in command")
			self.setFemaleAI()
			playsound(self.config["sounds"]["positive"])	
		elif "male assistant" in command:
			logging.debug("Detected 'a male assistant' in command")
			self.setMaleAI()
		elif "goodbye" in command or "bye" in command or "bye-bye" in command:
			logging.debug("Detected 'goodbye' or 'bye' in command")
			logging.info("Exiting programme")
			playsound(self.config["sounds"]["switchOff"])
			del self
			exit()
		else:
			logging.debug("Detected a search command")
			if (queue := "what is") in command or (queue := "what's") in command or \
				(queue := "who is") in command or (queue := "who's") in command:
				sub_command = command.replace(queue,"").strip()
			elif re.search("((^wiki|^wikipedia).*)|(.*(wiki$|wikipedia$))", command):
				sub_command = command.replace("wikipedia","").strip()
				sub_command = sub_command.replace("wiki","").strip()
			else:
				self.say("Sorry, I don't understand that command.")
				return
			try:
				info = wikipedia.summary(sub_command, 2)
				self.say(info)
			except wikipedia.DisambiguationError:
				logging.error("Wikipedia error")
				self.say("Sorry, there were quite many possible searches. \
					Mind if you be more specific in your search terms? Thanks!")
			except wikipedia.exceptions.PageError:
				logging.error("Wikipedia error")
				self.say(f"Sorry, there are no matching searches for {sub_command}")
	

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
		