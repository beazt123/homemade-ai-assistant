import pvporcupine

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