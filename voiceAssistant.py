import logging
import speech_recognition as sr
from config import readme, MUSIC_PATH
from voiceAssistantToolkit import WakeWordDetector, Bot


def main():
	print(readme)
	logging.basicConfig(level="INFO")
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