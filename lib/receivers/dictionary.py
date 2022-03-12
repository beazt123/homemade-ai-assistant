from pprint import pprint
import json
import logging
import os
import re

from PyDictionary import PyDictionary

from .select_config import SelectConfig
from .mixins.speechMixin import SpeechMixin
from ..utils.article_builder import ArticleBuilder


class Dictionary(SpeechMixin, SelectConfig):
	logger = logging.getLogger(__name__)
	SPLIT_TOKEN = "<split-token>"

	def __init__(self, config, speechEngine = None):
		SpeechMixin.__init__(self, speechEngine)
		
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
		Dictionary.logger.debug(f"Fetched path to dict from file: {localConfig['dict']}")
		return localConfig

	def define(self, lookUpWord):
		data = lookUpWord.split()[0]
		Dictionary.logger.info(f"Lookup word: {data}")
		onlineSearchResult = self._onlineEngDict.meaning(data)
		self.articleBuilder.title(data)
		
		if onlineSearchResult == None:
			Dictionary.logger.warn("Not found in online dictionary/internet connection down. Reverting to offline dictionary")
			offlineSearchResult = self._offlineEngDict.get(data, None)
			
			if offlineSearchResult == None:
				Dictionary.logger.warn("Word not found in offline and online dictionary")
				print(f"Sorry, '{lookUpWord}' not found in dictionary")
				self.say("Your England very the powderful. Too powderful for me to find")
				return
				
			Dictionary.logger.debug(f"Offline Search Result: {offlineSearchResult}")
			offlineSearchResult = re.sub("[0-9].", Dictionary.SPLIT_TOKEN, offlineSearchResult)
			cleansedOfflineSearchResult = [sentence.strip() for sentence in offlineSearchResult.split(Dictionary.SPLIT_TOKEN) if sentence != ""]
			Dictionary.logger.info(f"Cleansed OfflineSearchResult: {cleansedOfflineSearchResult}")

			for sentence in cleansedOfflineSearchResult:
				self.articleBuilder.content(sentence)
				Dictionary.logger.debug(f"Added: {sentence}")

		else:
			Dictionary.logger.info(f"Word found in online search: {onlineSearchResult}")
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
		
		Dictionary.logger.info(self.articleBuilder.getArticleInSections())

		for section in self.articleBuilder.getArticleInSections():
			for content in section:
				print(content, end="")
				script = content.replace("\n", " ")
				self.say(script)
			# logging.debug(f"content: {content}")
			# print(content, end="")
			# self.say(content.strip("\n"))
			# logging.debug(f"Said content: {content}")

		self.articleBuilder.clear()