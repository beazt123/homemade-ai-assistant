import pyaudio
import struct
import logging
import pvporcupine
from datetime import datetime

logger = logging.getLogger(__name__)

class WakeWordDetector:
	def __init__(self, access_key, wakewords = pvporcupine.KEYWORDS):
		pa = pyaudio.PyAudio()
		
		if set(wakewords).issubset(set(pvporcupine.KEYWORDS)):
			self.wake_words = wakewords
		else:
			raise ValueError(f"Current wakewords are {wakewords}. Wakewords chosen must be one of {pvporcupine.KEYWORDS}")
		
		self.porcupine = pvporcupine.create(access_key=access_key, 
											keywords=self.wake_words)
		self.audio_stream = pa.open(
			rate = self.porcupine.sample_rate,
			channels = 1,
			format = pyaudio.paInt16,
			input = True,
			frames_per_buffer = self.porcupine.frame_length)
			
		logger.info("Initialised Wake word detector")
		
	def waitForWakeWord(self):
		while True:
			# logger.debug("Reading next frame")
			pcm = self.audio_stream.read(self.porcupine.frame_length)
			pcm = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

			result = self.porcupine.process(pcm)	
			if result >= 0:
				logger.info(f'Detected {self.wake_words[result]}')
				break
