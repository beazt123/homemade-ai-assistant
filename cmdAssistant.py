import os.path
import logging
# logging.basicConfig(level=logging.INFO)
# logging.disable(level=logging.CRITICAL)

import argparse
from pathlib import Path
from lib.invoker import Invoker
from lib.config.devices.windowsLaptopCmdConfig import commandHooks
from lib.commands import (
    DefineWord,
    GetWeatherForecast,
    GoogleSearch,
    PlayYoutubeVideo,
    WikiSearch
)

parser = argparse.ArgumentParser(description = "A general assistant as a cmd tool")

# Only 1 of the following arguments can be utlised
group = parser.add_mutually_exclusive_group()
group.add_argument("-y", "--youtube", action = "store_true", dest = "youtube", help = "Play a video on YouTube")
group.add_argument("-g", "--google", action = "store_true", dest = "google", help = "Perform a Google search using the system default browser")
group.add_argument("-w", "--wiki", action = "store_true", dest = "wiki", help = "Perform a wikipedia search and print the results")
group.add_argument("-d", "--define", action = "store_true", dest = "requestDictDefinition", help = "Define an English word")
group.add_argument("-W", "--weather", action = "store_true", dest = "weatherForecast", help = "Forecast the weather for the next 12 hrs")
group.add_argument("-f", "--file", action = "store_true", dest = "file", help = "Find files using pattern matching")
# group.add_argument("-w", "--wiki", dest = "wiki", help = "Perform a Wikipedia search", default = 1, type = int, nargs="*")

# Optionl arguments
# parser.add_argument("search", action = "extend", help = "What you want to search for", nargs="*")
parser.add_argument('action', metavar='action', type=str, nargs='+',
                    help='What action you want to perform')
# parser.add_argument("-b", "--bot", action = "store_true", dest = "usebot", help = "Get a bot to answer you verbally along with command line print-outs")

args = parser.parse_args()

invoker = Invoker()
invoker.registerAll(commandHooks)
from configparser import ConfigParser

pathToUserConfig = os.path.join("lib", "config", "files", "userconfig.ini")

config = ConfigParser()
config.read(pathToUserConfig)

searchList = args.action

if searchList != [] and searchList[0] == "search":
	search = " ".join(searchList[1:])
	if args.youtube:
		msg = f"Playing a video of {search} on Youtube"
		print(msg)
		# if args.usebot:
		# 	makeBotSay(msg)
		event = PlayYoutubeVideo.__name__
		data = search
		
	elif args.google:
		msg = f"Ok. Searching for '{search}' on Google"
		print(msg)
		# if args.usebot:
		# 	makeBotSay(msg)
		event = GoogleSearch.__name__
		data = search
	
	elif args.wiki:
		# if args.usebot:
		# 	makeBotSay(msg)
		event = WikiSearch.__name__
		data = search
	
	elif args.requestDictDefinition:
		event = DefineWord.__name__
		data = search.split()[0]
		
	elif args.weatherForecast:
		logging.info("Weather forecast selected")
		event = GetWeatherForecast.__name__
		data = None	

	elif args.file:
		path = searchList[1]
		file = searchList[2]
		glob_path = Path(path)
		print("Searching for files...")
		for pp in glob_path.glob(f"**/*{file}"):
		    print(str(pp))
		print("=== END ===")
		exit()
	
if searchList != [] and searchList[0] == "config":
	if searchList[1].lower() == "show":
		with open(pathToUserConfig, "r") as f:
			conf = f.read()
		print(conf)
		exit()

	elif searchList[1].lower() == "get":
		try:
			print(config.get(*searchList[2:]))
		except TypeError:
			print("Please specify the section you wanna view")
		exit()

	elif searchList[1].lower() == "set":
		config[searchList[2].upper()][searchList[3]] = searchList[4]
		with open(pathToUserConfig, 'w') as f:
			config.write(f)
		exit()


	


invoker.execute(event, data)