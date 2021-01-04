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

MUSIC_PATH = r"D:\Music\\"
readme = \
"""
AI powered stupid assistant
===========================
Wake words:
	Please say any 1 of the following words to wake the assistant:
		{wakeWords}
		
Command words:

	GOOGLE: 
		Performs a google search on your browser.
		I.e. Say "google most recommended reed diffuser"
		
	YOUTUBE:
		Plays a youtube video on your browser.
		I.e. Say "youtube bloodstream ed sheeran"
		
	PLAY / STOP...MUSIC:
		Plays a random music on a pre-set directory
		I.e. Say "play some music" or
			say "play the music" or 
			say "stop the music" or
			say "stop playing the music"
		
	WHO'S / WHAT'S:
		Says a 2 linear summary from a wikipedia search.
		I.e. Say "who is Donald trump" or "what is black hole"
		
	TELL...TIME / JOKE:
		Tells you a joke or the time
		I.e. "tell me the time" or "tell time"
			"tell me a joke" or "tell a joke" or even "Tell joke"
		
	...A MALE/FEMALE ASSISTANT:
		Changes the gender of the voice assistant.
		I.e. "can I talk to a female assistant?"
		
	BYE-BYE:
		Closes the programme
		I.e. "goodbye" or "bye" or "bye-bye"
		
	SHUT DOWN COMPUTER:
		Shuts down the computer. Rmb to save your work!
		I.e. "shut down computer"

""".format(wakeWords = ", ".join(pvporcupine.KEYWORDS))

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
	def __init__(self, name, mic):
		self.name = name
		self.listener = mic
		self.recogniser = sr.Recognizer()
		self.alive = True
		self.voice = pyttsx3.init()
		self.audioPlayer = None
		
		self.voice.setProperty("rate", 160)
		
	def is_alive(self):
		return self.alive
		
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
		
	def listen(self):
		try:
			with self.listener as source:
				try:
					logging.info("Listening...")
					self.recogniser.adjust_for_ambient_noise(source, duration = 0.5)
					self.say("Hi") 	
					voice = self.recogniser.listen(source, timeout = 5, phrase_time_limit = 5)#, None, self.listen_duration)
					logging.info("Voice received")
					command = self.recogniser.recognize_google(voice)
					logging.info("Trascribed voice")
					command = command.strip().lower()
					logging.info(f"Detected command: {command}")
				except sr.WaitTimeoutError:
					self.say("I couldn't hear anything. Activate me again and repeat your command")
				
		except sr.UnknownValueError:
			logging.warning("Couldn't detect voice")
			self.say("Sorry I couldn't hear you clearly")
			return
			
		self.process_command(command)
		
	def calibrateMic(self):
		with self.listener as source:
			self.recogniser.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
	
	def process_command(self, command):
		if "shut down computer" in command:
			os.system("shutdown /s /t 1") 
		elif "calibrate microphone" in command:
			self.calibrateMic()
			self.say("I have calibrated the microphone.")
		elif re.search("^youtube.*", command):
			logging.debug("Detected 'youtube' in command")
			video = re.sub("play", "", command)
			logging.debug(video)
			self.say(f"Ok. Playing {video} on YouTube.")
			pywhatkit.playonyt(video)
		elif re.search("^play.*music$", command):
			self.audioPlayer = pyglet.media.Player()
			systemMusic = os.listdir(MUSIC_PATH)
			chosenNumber = random.randint(0,len(systemMusic)-1)
			chosenSong = systemMusic[chosenNumber]
			
			song = pyglet.media.load(MUSIC_PATH + chosenSong)
			self.audioPlayer.queue(song)
			self.say("Ok. Playing a random song from your system")
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
			logging.debug("Detected 'be a male' in command")
			self.setMaleAI()
			self.say("Done! How do I sound?")
		elif "a female assistant" in command:
			logging.debug("Detected 'be a female' in command")
			self.setFemaleAI()
			self.say("Done! How do I sound?")	
		elif "goodbye" in command or "bye" in command or "bye-bye" in command:
			logging.debug("Detected 'goodbye' or 'bye' in command")
			self.alive = False
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
				logging.warning("Wikipedia error")
				self.say("Sorry, there were quite many possible searches. \
					Mind if you be more specific in your search terms? Thanks!")
			# except wikipedia.exceptions.PageError:
				# logging.warning("Wikipedia error")
				# self.say(f"Sorry, there are no matching searches for {sub_command}")
	

def main():
	print("Please say any of the following words to wake the bot:\n" + ", ".join(pvporcupine.KEYWORDS))
	print(readme)
	logging.basicConfig(level= "INFO")
	agent = WakeWordDetector()
	print("Agent on standby")
	bot = Bot("Ajax", sr.Microphone())
	bot.calibrateMic()
	while True:
		try:
			if bot.is_alive():
				agent.waitForWakeWord()
				bot.listen()
			else:
				break
		except KeyboardInterrupt:
			break
		


if __name__ == "__main__":
	main()
