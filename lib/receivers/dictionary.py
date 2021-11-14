import json
import logging
import os
import re

from PyDictionary import PyDictionary
from nltk import sent_tokenize

from .select_config import SelectConfig
from .speechMixin import SpeechMixin
from ..utils.article_builder import ArticleBuilder


class Dictionary(SpeechMixin, SelectConfig):
	def __init__(self, config, speechEngine):
		SpeechMixin.__init__(self, config, speechEngine)
		
		self.config = self.getConfig(config)
		self._onlineEngDict = PyDictionary()
		self._offlineEngDict = None
		self.articleBuilder = ArticleBuilder()

		

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
		data = lookUpWord.split()[0]
		onlineSearchResult = self._onlineEngDict.meaning(data)
		self.articleBuilder.title(data)
		
		if onlineSearchResult == None:
			logging.warn("Word not found in dictionary or internet connection is down. Reverting to offline dictionary")
			offlineSearchResult = self._offlineEngDict.get(data, None)
			
			if offlineSearchResult == None:
				logging.info("Word not found in offline and online dictionary")
				self.say("Your England very the powderful. Too powderful for me to find")
				
			# script = sent_tokenize(offlineSearchResult)
			offlineSearchResult = re.sub("[0-9].", "\n- ", offlineSearchResult)
			offlineSearchResult = re.sub(";", "\n\t- ", offlineSearchResult)
			self.articleBuilder.content(offlineSearchResult)

		else:
			self.articleBuilder.startSection()
			for category, meanings in onlineSearchResult.items():
				self.articleBuilder.subtitle(f"{category}:")

				counter = 0
				self.articleBuilder.startSection(bullet = "-")
				for meaning in meanings:
					self.articleBuilder.content(meaning)
					
					if counter > 5:
						break
				self.articleBuilder.endSection()
				
			self.articleBuilder.endSection()
		
		for section in self.articleBuilder.getArticleSections():
			for content in section:
				print(content, end="")
				self.say(content)

		self.articleBuilder.clear()