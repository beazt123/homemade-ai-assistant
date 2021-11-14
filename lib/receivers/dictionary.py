import json
import logging
import os
import re

from PyDictionary import PyDictionary
from nltk import sent_tokenize

from .select_config import SelectConfig
from .speechMixin import SpeechMixin


class Dictionary(SpeechMixin, SelectConfig):
	def __init__(self, config, speechEngine):
		SpeechMixin.__init__(self, speechEngine)
		
		self.config = self.getConfig(config)
		self._onlineEngDict = PyDictionary()
		self._offlineEngDict = None

		

		with open(self.config["dict"], "r") as f:
			self._offlineEngDict = json.load(f)


	def getConfig(self, config):
		path_to_dict = os.path.join(config.get("RESOURCES", "PARENT_FOLDER_NAME"),
									config.get("DICTIONARY", "FOLDER_NAME"),
									config.get("DICTIONARY", "FILE_NAME"))
		localConfig = dict()
		localConfig["dict"] = path_to_dict
		return localConfig

	def define(self, lookUpWord):
		data = lookUpWord[0]
		onlineSearchResult = self._onlineEngDict.meaning(data)
		wordToPrint = f"WORD: {data}"
		print(wordToPrint)
		print("=" * len(f"WORD: {data}\n"))
		self.say(data)
		
		if onlineSearchResult == None:
			logging.warn("Word not found in dictionary or internet connection is down. Reverting to offline dictionary")
			offlineSearchResult = self._offlineEngDict.get(data, None)
			
			if offlineSearchResult == None:
				logging.info("Word not found in offline and online dictionary")
				self.say("Your England very the powderful. Too powderful for me to find")
				
			script = sent_tokenize(offlineSearchResult)
			offlineSearchResult = re.sub("[0-9].", "\n- ", offlineSearchResult)
			offlineSearchResult = re.sub(";", "\n\t- ", offlineSearchResult)
			print(offlineSearchResult)
			self.say(script)
		
		for category, meanings in onlineSearchResult.items():
			print(f"{category}:")
			self.say(category)
			
			counter = 0
			
			for meaning in meanings:
				print(self.formatForPPrint(f"- {meaning}", indent="\t"))
				self.say(meaning)
				
				if counter > 5:
					break
			
			print()