import logging
import warnings

import speech_recognition as sr
from config import readme, engineConfig
from voiceAssistantToolkit import WakeWordDetector, Bot, Engine


def main():
	warnings.filterwarnings("ignore")
	print(readme)
	# logging.basicConfig(level="DEBUG")
	logging.disable(logging.CRITICAL);
	agent = WakeWordDetector()
	engine = Engine(engineConfig)
	bot = Bot("Ajax", sr.Microphone(), engine)
	while True:
		try:
			bot.adjust_for_ambient_noise()
			print("Ready")
			agent.waitForWakeWord()
			bot.listen()
		except KeyboardInterrupt:
			break
		


if __name__ == "__main__":
	main()