import os
from configparser import ConfigParser
from .config import Config
from copy import deepcopy




class UserPreferences(Config):
			
	@property
	def AI_GENDER(self):
		return self.config.get("AI", "AI_GENDER", fallback = "female")
		
	@property
	def PATH_TO_LOCAL_MUSIC_FOLDER(self):
		return self.config.get("OFFLINE-MUSIC", "PATH_TO_LOCAL_MUSIC_FOLDER")
		
	@property
	def NEWS_WEBSITE(self):
		return self.config.get("NEWS","NEWS_WEBSITE", 
				fallback="https://www.straitstimes.com/")
		
	@property
	def NUM_ARTICLES_PER_NEWS_QUERY(self):
		return self.config.getint("NEWS", "NUM_ARTICLES_PER_NEWS_QUERY", 
				fallback = 5)
				
	@property
	def CONFIG(self):
		return deepcopy(self.config)
				
	def clone(self):
		return deepcopy(self)
	
	def update(self, otherUserPreference):
		if isinstance(otherUserPreference, Options):
			self.config.update(otherUserPreference.config)
		else:
			raise TypeError("You must change user preferences using an Options object")


class Options:
	def __init__(self):
		self.config = ConfigParser()

	def AI_GENDER(self, value):
		if value.lower() in {"male", "female"}:
			if "AI" not in self.config.keys():
				self.config["AI"] = dict()
			self.config["AI"]["AI_GENDER"] = value

'''
[DEFAULT]
AI_GENDER=female
PATH_TO_LOCAL_MUSIC_FOLDER=D:\\\\Music
NEWS_WEBSITE=https://www.straitstimes.com/
NUM_ARTICLES_PER_NEWS_QUERY=5

[AI]
AI_GENDER=female

[OFFLINE-MUSIC]
PATH_TO_LOCAL_MUSIC_FOLDER=D:\\\\Music

[NEWS]
NEWS_WEBSITE=https://www.straitstimes.com/
NUM_ARTICLES_PER_NEWS_QUERY=5
'''