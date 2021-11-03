import os
from configparser import ConfigParser
from .config import Config




class UserPreferences(Config):
			
	@property
	def AI_GENDER(self):
		return self.config.get("AI", "AI_GENDER", fallback = "female")
		
	@AI_GENDER.setter
	def AI_GENDER(self, value):
		if value.lower() in {"male", "female"}:
			self.config["AI"]["AI_GENDER"] = value

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