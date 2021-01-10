import re
import os
import pyaudio
import random
import struct
import logging
import pvporcupine
import speech_recognition as sr
import pywhatkit
import wikipedia
import pyjokes
import pyttsx3
import pyglet
from datetime import datetime
from playsound import playsound
from constants import UNKNOWN_TOKEN, FAILED_TOKEN


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
		
	def listen(self):
		self.engine.loadAndPlayReadySoundEffect()
		try:
			with self.listener as source:
				try:
					self.recogniser.adjust_for_ambient_noise(source, duration = 0.3)
					logging.debug("Calibrating Mic")
					logging.info("Listening...")
					voice = self.recogniser.listen(source, timeout = 3, phrase_time_limit = 5)
					logging.debug("Actually listening")
					
					logging.info("Voice received")
					command	= self.transcribe(voice)					
					logging.info("Trascribed voice")
					command = command.strip().lower()
					logging.info(f"Detected command: {command}")
				except sr.WaitTimeoutError:
					logging.warn("User didn't speak")
					command = FAILED_TOKEN
				
				
				
				
		except sr.UnknownValueError:
			logging.warning("Couldn't detect voice")
			command = UNKNOWN_TOKEN
			
		self.engine.execute(command)
		
	def transcribe(self, audio):
		try:
			command = self.recogniser.recognize_google(audio)
		except sr.RequestError:
			logging.warning("Internet unavailable. Using offline TTS")
			command = self.recogniser.recognize_sphinx(audio)
		return command
		
class Engine:	
	def __init__(self, config = dict()):
		self.voice = pyttsx3.init()
		self.voice.setProperty("rate", 170)
		self.config = config
	
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
			
	def loadAndPlayReadySoundEffect(self):
		playsound(self.config["sounds"]["ready sound"])
	
	def execute(self, command):
		if UNKNOWN_TOKEN in command or FAILED_TOKEN in command:
			logging.info("Unknown or failed command detected")
			playsound(self.config["sounds"]["negative sound"])
		elif re.search("^shut.down.*(computer$|system$)", command):
			logging.info("Shutting down system")
			os.system("shutdown /s /t 1") 
		elif re.search("^youtube.*", command):
			logging.debug("Detected 'youtube' in command")
			video = re.sub("youtube", "", command)
			logging.debug(video)
			self.say(f"Ok. Playing {video} on YouTube.")
			pywhatkit.playonyt(video)
		elif re.search("^play.*music$", command):
			self.audioPlayer = pyglet.media.Player()
			musicLibrary = self.config["MUSIC_PATH"]
			systemMusic = os.listdir(musicLibrary)			
			
			self.say("Ok. Playing music from your music library")
			for music in systemMusic:
				try:
					song = pyglet.media.load(musicLibrary + "\\" + music)
					self.audioPlayer.queue(song)
				except:
					break
			self.audioPlayer.play()
		elif re.search("^stop.*music$", command):
			self.audioPlayer.pause()
			self.audioPlayer.delete()
			del self.audioPlayer
		elif re.search("^google.*", command):
			search = re.sub("google", "", command)
			self.say(f"OK. Searching for {search} on Google")
			pywhatkit.search(search)
		elif re.search("^tell.*", command):
			logging.debug("Detected 'tell' in command")
			command = command.replace("?","")
			if re.search(".*time$", command):
				logging.debug("Detected 'time' in command")
				time = datetime.now().strftime('%I:%M %p')
				msg = 'Current time is ' + time
				logging.info(msg)
				self.say(msg)
			elif re.search(".*joke$", command) or re.search(".*funny$", command):
				self.say(pyjokes.get_joke())
			else:
				self.say("You can ask me to tell you a joke or the time")
		elif "a male assistant" in command:
			logging.debug("Detected 'a male assistant' in command")
			self.setMaleAI()
			playsound(self.config["sounds"]["positive sound"])
		elif "a female assistant" in command:
			logging.debug("Detected 'a female assistant' in command")
			self.setFemaleAI()
			playsound(self.config["sounds"]["positive sound"])
		elif "goodbye" in command or "bye" in command or "bye-bye" in command:
			logging.debug("Detected 'goodbye' or 'bye' in command")
			logging.info("Exiting programme")
			exit()
		else:
			logging.debug("Detected a search command")
			if (queue := "what is") in command or (queue := "what's") in command or \
				(queue := "who is") in command or (queue := "who's") in command:
				sub_command = command.replace(queue,"").strip()
			else:
				self.say("I can't hear you clearly.")
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

