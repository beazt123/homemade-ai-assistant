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

from ..constants import FAILED_TOKEN
from .utils import playOnYoutube, googleSearchFor, playPlaylist, generateAllMusicFiles

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
