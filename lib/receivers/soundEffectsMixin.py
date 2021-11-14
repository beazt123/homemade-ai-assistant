import os
import logging
from playsound import playsound

class SoundEffectsMixin:
    def __init__(self, config) -> None:

    
        localConfig = dict()
        resourcesFolder = config.get("RESOURCES", "PARENT_FOLDER_NAME")
        soundsFolder = config.get("SOUND-EFFECTS", "FOLDER_NAME")
        path_to_sounds_folder = os.path.join(resourcesFolder, soundsFolder)


        localConfig["ready"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "ATTENTION"))
        localConfig["at-ease"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "AT_EASE"))
        localConfig["switch-off"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "SWITCH_OFF"))
        localConfig["switch-on"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "LEVEL_UP"))
        localConfig["quick-processing"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "QUICK_PROCESSING"))
        # localConfig["done"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "DONE"))

        self.config = localConfig

        

    def readySound(self, block = False):    
        playsound(self.config["ready"], block)
        logging.debug("Played ready sound")

    def atEaseSound(self, block = False):    
        playsound(self.config["at-ease"], block)
        logging.debug("Played at-ease sound")
        
    def switchOnSound(self, block = False):    
        playsound(self.config["switch-on"], block)
        logging.debug("Played switch-on sound")
    
    def switchOffSound(self, block = False):    
        playsound(self.config["switch-off"], block)
        logging.debug("Played switch-off sound")

    def quickProcessingSound(self, block = False):    
        playsound(self.config["switch-off"], block)
        logging.debug("Played switch-off sound")

    

    

