from .receivers import *

 

SEARCHER_GUIDE = {
	"title": "Search on GOOGLE/YOUTUBE/WIKI:",
	"content": [
			"Performs a search on your browser for Google & Youtube.",
			"Wiki searches will show here with audio response.",
			"I.e. 'google recommended reed diffuser', 'youtube bloodstream ed sheeran', 'wiki Donald Trump'"
	]
}



OFFLINE_MUSIC_GUIDE = {
	"title": "PLAY / STOP the MUSIC:",
	"content": [
		"Plays a random music on a pre-set directory",
		"I.e. 'play some music', 'stop the music'"
	]
}

WEATHER_FORECAST_GUIDE = {
	"title": "WEATHER forecast:",
	"content": [
		"Gives you the next 12 hr weather forecast in 3-hr blocks.",
		"I.e. 'Weather forecast'"
	]
}


NEWS_FLASH_GUIDE = {
	"title": "LOCAL NEWS:",
	"content": [
		"Brings you summaries of the top 5 articles from a specified news site",
		"I.e. 'New flash'"
	]
}

DICTIONARY_GUIDE = {
	"title": "DEFINE a word in the dictionary:",
	"content": [
		"Gives you the dictionary definition of a single word.",
		"I.e. 'Define apprehensive'"
	]
}

GENERAL_RECEIVER_GUIDE = {
	"title": "TELL you the TIME / a JOKE:",
	"content": [
		"Tells you a joke or the time",
		"I.e. 'tell me the time', 'tell me a joke'"
	]
}

SHUTDOWN_GUIDE = {
	"title": "SHUTDOWN COMPUTER:",
	"content": [
		"Shuts down the computer. Rmb to save your work!",
		"I.e. 'shut down computer!'"
	]
}

LIGHTS_GUIDE = {
	"title": "WAMR/COOL LIGHTS:",
	"content": [
		"Switches on the warm/cool lights according to your command",
		"I.e. 'Cool lights on', 'Warm lights off'"
	]
}

USER_GUIDES = {
	GeneralReceiver.__name__ : GENERAL_RECEIVER_GUIDE,
	News.__name__ : NEWS_FLASH_GUIDE,
	Searcher.__name__ : SEARCHER_GUIDE,
	System.__name__ : SHUTDOWN_GUIDE,
	Weather.__name__ : WEATHER_FORECAST_GUIDE,
	Dictionary.__name__ : DICTIONARY_GUIDE,
	OfflineMusic.__name__ : OFFLINE_MUSIC_GUIDE
}



