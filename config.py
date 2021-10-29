import os
from pvporcupine import KEYWORDS

engineConfig = dict()
engineConfig["MUSIC_PATH"] = os.path.join("D:\\","Music")

soundEffects = dict()
soundsFolder = os.path.join("resources", "soundEffects")
soundEffects["ready sound"] = os.path.join(soundsFolder, "done-trimmed.wav")
soundEffects["negative sound"] = os.path.join(soundsFolder, "failure-01.wav")
soundEffects["level up sound"] = os.path.join(soundsFolder, "level-up-03.wav")
soundEffects["positive sound"] = os.path.join(soundsFolder, "done.wav")

engineConfig["sounds"] = soundEffects

readme = \
"""
A.I general assistant
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

""".format(wakeWords = ", \n\t\t".join(KEYWORDS))