import argparse
import webbrowser
import pywhatkit
import wikipedia
import pyttsx3

parser = argparse.ArgumentParser(description = "A general assistant as a cmd tool")

# Only 1 of the following arguments can be utlised
group = parser.add_mutually_exclusive_group()
group.add_argument("-y", "--youtube", action = "store_true", dest = "youtube", help = "Play a video on YouTube")
group.add_argument("-g", "--google", action = "store_true", dest = "google", help = "Perform a Google search using the system default browser")
group.add_argument("-w", "--wiki", dest = "wiki", help = "Perform a Wikipedia search", default = 1, type = int, nargs="*")

# Optionl arguments
parser.add_argument("search", action = "extend", help = "What you want to search for", nargs="*")
parser.add_argument("-b", "--bot", action = "store_true", dest = "usebot", help = "Get a bot to answer you verbally along with command line print-outs")

args = parser.parse_args()

def makeBotSay(text):
	bot = pyttsx3.init()
	bot.setProperty("rate", 160)
	bot.say(text)
	bot.runAndWait()


if (searchList := args.search) != None:
	search = " ".join(searchList)
	if args.youtube:
		msg = f"Playing a video of {search} on Youtube"
		print(msg)
		if args.usebot:
			makeBotSay(msg)
		pywhatkit.playonyt(search)
		
	elif args.google:
		msg = f"Ok. Searching for '{search}' on Google"
		print(msg)
		if args.usebot:
			makeBotSay(msg)
		pywhatkit.search(search)
		
	elif (verbosity := args.wiki) != None:
		msg = "Ok. Wiki search results comming out."
		print(msg)
		if args.usebot:
			makeBotSay(msg)
		try:
			info = wikipedia.summary(search, verbosity)
		except wikipedia.DisambiguationError as e:
			print("Wiki disambiguation error")
			print(e.args)
			print(e.message)
			info = "D-Error"
		except wikipedia.exceptions.PageError:
			print(f"Sorry there are no matching searches for {seearch} on wikipedia")
			info = "P-Error"
		print(info)
		if args.usebot:
			makeBotSay(info)
			
		
		