from pvporcupine import KEYWORDS

README = \
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
			
	... WEATHER ...:
		Gives you a 12 hr weather forecast in 3-hr blocks.
		I.e. "Weather forecast" or
			 "How's the weather today?"
			
	... NEWS ...:
		Brings you summaries of the top 5 articles from a specified news site
		
	DEFINE <word>:
		Gives you the dictionary definition of a single word. 
		Works both offline and online.
		I.e. "Define apprehensive"
		
	TELL...TIME / JOKE:
		Tells you a joke or the time
		I.e. "tell me the time" or "tell time"
			"tell me a joke" or "tell a joke" or even "Tell joke"
		
	BYE-BYE:
		Closes this program.
		I.e. "goodbye" or "bye" or "bye-bye"
		
	SHUTDOWN COMPUTER:
		Shuts down the computer. Rmb to save your work!
		I.e. "shut down computer!"

""".format(wakewords=", \n\t\t".join(KEYWORDS))




