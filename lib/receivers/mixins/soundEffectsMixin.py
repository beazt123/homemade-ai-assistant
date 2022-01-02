import os
import logging

logger = logging.getLogger(__name__)

class SoundEffectsMixin:
    def __init__(self, config = None, soundEngine = None) -> None:
        configProvided = bool(config)
        self.soundEffectsEngine = soundEngine
        self.soundEffectsConfig = None
        self.isUsed = configProvided and self.soundEffectsEngine
		
        logger.info(f"configProvided: {configProvided}, sound engine: {self.soundEffectsEngine}")
		
        if self.isUsed:
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

            self.soundEffectsConfig = localConfig
            logger.info("Class sound effects enabled")
            return
			
        logger.info("Class sound effects disabled")       


    def readySound(self, block = False):
        logger.debug(f"Calling ready sound: {self.isUsed}")
        if self.isUsed:
            self.soundEffectsEngine.play(self.soundEffectsConfig["ready"], block)
            logger.info("Played ready sound")

    def atEaseSound(self, block = False):
        logger.debug(f"Calling atEase sound: {self.isUsed}")
        if self.isUsed:
            self.soundEffectsEngine.play(self.soundEffectsConfig["at-ease"], block)
            logger.info("Played at-ease sound")
        
    def switchOnSound(self, block = False):
        logger.debug(f"Calling switchOnsound: {self.isUsed}")
        if self.isUsed:
            self.soundEffectsEngine.play(self.soundEffectsConfig["switch-on"], block)
            logger.info("Played switch-on sound")
    
    def switchOffSound(self, block = False):
        logger.debug(f"Calling switchOff sound: {self.isUsed}")
        if self.isUsed:
            self.soundEffectsEngine.play(self.soundEffectsConfig["switch-off"], block)
            logger.info("Played switch-off sound")

    def quickProcessingSound(self, block = False):
        logger.debug(f"Calling quickProcessing sound: {self.isUsed}")
        if self.isUsed:
            self.soundEffectsEngine.play(self.soundEffectsConfig["switch-off"], block)
            logger.info("Played quickProcessing sound")

    

    

