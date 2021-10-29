import logging
import speech_recognition as sr
from config import readme, engineConfig
from voiceAssistantToolkit import WakeWordDetector, Bot, Engine


def main():
	print(readme)
	logging.basicConfig(level="INFO")
	agent = WakeWordDetector()
	engine = Engine(engineConfig)
	print("Agent on standby")
	bot = Bot("Ajax", sr.Microphone(), engine)
	while True:
		try:
			bot.adjust_for_ambient_noise()
			agent.waitForWakeWord()
			bot.listen()
		except KeyboardInterrupt:
			break
		


if __name__ == "__main__":
	main()