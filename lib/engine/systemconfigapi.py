import os
from configparser import ConfigParser
from .config import Config




class SystemConfig(Config):
	def __init__(self, fp):
		super().__init__(fp)
		self.path_to_sound_effects = os.path.join(
				self.config["CONSTANTS"]["RESOURCE_FOLDER_NAME"], 
				self.config["CONSTANTS"]["SOUND_EFFECTS_FOLDER_NAME"])
		self.path_to_dictionaries = os.path.join(
				self.config["CONSTANTS"]["RESOURCE_FOLDER_NAME"], 
				self.config["CONSTANTS"]["ENGLISH_DICTIONARY_FOLDER"])
		

	@property
	def UNKNOWN_TOKEN(self):
		return self.config["CONSTANTS"]["UNKNOWN_TOKEN"]
		
	@property
	def FAILED_TOKEN(self):
		return self.config["CONSTANTS"]["FAILED_TOKEN"]
		
	@property
	def MODE(self):
		mode = self.config.get("DEVELOPMENT","DEPLOYMENT_MODE", fallback="production")
		if mode != "production":
			return "development"
		else:
			return mode
		
	@property
	def ATTENTION_SOUND(self):
		return os.path.join(
				self.path_to_sound_effects, 
				self.config["SOUND-EFFECTS"]["ATTENTION"])
	
	@property
	def AT_EASE_SOUND(self):
		return os.path.join(
				self.path_to_sound_effects, 
				self.config["SOUND-EFFECTS"]["AT_EASE"])
	
	@property
	def SWITCH_OFF_SOUND(self):
		return os.path.join(
				self.path_to_sound_effects, 
				self.config["SOUND-EFFECTS"]["SWITCH_OFF"])
	
	@property
	def QUICK_PROCESSING_SOUND(self):
		return os.path.join(
				self.path_to_sound_effects, 
				self.config["SOUND-EFFECTS"]["QUICK_PROCESSING"])
				
	@property
	def LEVEL_UP_SOUND(self):
		return os.path.join(
				self.path_to_sound_effects, 
				self.config["SOUND-EFFECTS"]["LEVEL_UP"])
	
	@property
	def DONE_SOUND(self):
		return os.path.join(
				self.path_to_sound_effects, 
				self.config["SOUND-EFFECTS"]["DONE"])
	
	@property	
	def PRINTED_TEXT_WIDTH(self):
		return self.config.getint("DEVELOPMENT", 
								"PRINTED_TEXT_WIDTH", 
								fallback = 80)
		
	@property
	def JSON_DICTIONARY_NAME(self):
		return os.path.join(
				self.path_to_dictionaries, 
				self.config["RESOURCES"]["JSON_DICTIONARY_NAME"])
		