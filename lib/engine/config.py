import logging
from configparser import ConfigParser

class Config:
	def __init__(self, fp):
		if isinstance(fp, str):
			self.fp = fp
			self.config = ConfigParser()
			self.config.read(fp)
		else:
			raise TypeError("fp must be a path to the INI file")
			
			
	def save(self):
		configType = type(self)
		logging.debug(f"Saving {configType}")
		
		with open(self.fp, "w") as configFile:
			logging.debug(f"Opened external file to write {configType}")
			self.config.write(configFile)
			logging.debug(f"Successfully written {configType} to external file")
		
		logging.info(f"Saved {configType}")