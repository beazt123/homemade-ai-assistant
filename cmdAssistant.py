import argparse
import webbrowser
import pywhatkit
import pyttsx3

parser = argparse.ArgumentParser(description = "A general assistant as a cmd tool")

# Only 1 of the following arguments can be utlised
group = parser.add_mutually_exclusive_group()
group.add_argument("-y", "--youtube", action = "extend", dest = "youtube", help = "Play a video on YouTube", nargs='*')
group.add_argument("-g", "--google", action = "extend", dest = "google", help = "Perform a Google search using the system default browser", nargs='*')
group.add_argument("-w", "--wiki", action = "extend", dest = "wiki", help = "Perform a Wikipedia search", nargs='*')

# Optionl arguments
parser.add_argument("-v", "--verbose", dest = "verbosity", help = "Adjust the verbosity of the answer", type = int, default = 1)
parser.add_argument("-b", "--bot", action = "store_true", dest = "usebot", help = "Get a bot to answer you verbally along with command line print-outs")

args = parser.parse_args()



if (youtubeSearch := args.youtube) != None:
	youtubeSearch = " ".join(youtubeSearch)
	print(f"Playing a video of {youtubeSearch} on Youtube")
	pywhatkit.playonyt(youtubeSearch)
	
elif (googleSearch := args.google) != None:
	googleSearch = " ".join(googleSearch)
	print(f"Ok. Searching for '{googleSearch}' on Google")
	pywhatkit.search(googleSearch)
	
elif (wikiSearch := args.wiki) != None:
	wikiSearch = " ".join(wikiSearch)
	verbosity = 1
	if (v := arg.verbosity) != None:
		verbosity = v
	print("Ok. Wiki search results comming out.")
	
	try:
		info = wikipedia.summary(wikiSearch, verbosity)
	except wikipedia.DisambiguationError as e:
		print("Wiki disambiguation error")
		print(e.args)
		print(e.message)
		info = "Error"
	print(info)
	if args.usebot:
		bot = pyttsx3.init()
		bot.say(info)
		bot.runAndWait()
		
	# except wikipedia.exceptions.PageError:
	