import os
from pvporcupine import KEYWORDS

engineConfig = dict()
engineConfig["MUSIC_PATH"] = os.path.join("D:\\","Music")

newsConfig = dict()
newsConfig["WEBSITE"] = "https://www.straitstimes.com/"
newsConfig["NUM_ARTICLE"] = 5

soundEffects = dict()
soundsFolder = os.path.join("resources", "soundEffects")
soundEffects["ready"] = os.path.join(soundsFolder, "done-trimmed-volboosted.wav")
soundEffects["negative"] = os.path.join(soundsFolder, "failure-01.wav")
soundEffects["atEase"] = os.path.join(soundsFolder, "at-ease.wav")
soundEffects["levelUp"] = os.path.join(soundsFolder, "level-up-03.wav")
soundEffects["positive"] = os.path.join(soundsFolder, "done.wav")
soundEffects["switchOff"] = os.path.join(soundsFolder, "futuristic-door-open-trimmed.mp3")




engineConfig["NEWS"] = newsConfig
engineConfig["sounds"] = soundEffects

readme = \
"""
A.I general assistant
===========================
Wake words:
	Please say any 1 of the following words to wake the assistant:
		{wakewords}
		
Command words:

	GOOGLE/YOUTUBE/WIKI: 
		Performs a search on your browser for Google & Youtube.
		Wiki searches will show here with audio response.
		
		I.e. Say "google most recommended reed diffuser"
			 Say "youtube bloodstream ed sheeran"
			 Say "wiki Donald Trump"
		
	PLAY / STOP...MUSIC:
		Plays a random music on a pre-set directory
		I.e. Say "play some music" or
			say "play the music" or 
			say "stop the music" or
			say "stop playing the music"
			
	GIMME THE LATEST NEWS:
		Brings you summaries of the top 5 articles from a specified news site
		
	TELL...TIME / JOKE:
		Tells you a joke or the time
		I.e. "tell me the time" or "tell time"
			"tell me a joke" or "tell a joke" or even "Tell joke"
		
	...A MALE/FEMALE ASSISTANT:
		Changes the gender of the voice assistant.
		I.e. "can I talk to a female assistant?"
		
	BYE-BYE:
		Closes this program.
		I.e. "goodbye" or "bye" or "bye-bye"
		
	SHUT DOWN COMPUTER:
		Shuts down the computer. Rmb to save your work!
		I.e. "shut down computer!"

""".format(wakewords=", \n\t\t".join(KEYWORDS))