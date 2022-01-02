import os
import logging
import random
from pytz import timezone
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)

class AsyncStdVoiceResponseMixin:
    def __init__(self, config = None, soundEngine = None) -> None:
        configProvided = bool(config)
        self.voiceResponseSoundEngine = soundEngine
        self.aiVoiceResponseConfig = defaultdict(lambda : None)
        self.greetingCheck = {
			"GOOD_MORNING": False,
			"GOOD_AFTNN": False,
			"GOOD_EVENING": False
		}
        self.isUsed = configProvided and self.voiceResponseSoundEngine
		
        logger.info(f"configProvided: {bool(configProvided)}, soundEngine provided: {bool(self.voiceResponseSoundEngine)}")
        
        if self.isUsed:
            resourcesFolder = config.get("RESOURCES", "PARENT_FOLDER_NAME")
            soundsFolder = config.get("SOUND-EFFECTS", "FOLDER_NAME")
            path_to_sounds_folder = os.path.join(resourcesFolder, soundsFolder)
            self.aiVoiceResponseConfig["timezone"] = timezone(config.get("LOCATION", "TIMEZONE"))
            self.aiVoiceResponseConfig["GOOD_MORNING"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "GOOD_MORNING"))
            self.aiVoiceResponseConfig["GOOD_AFTNN"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "GOOD_AFTNN"))
            self.aiVoiceResponseConfig["GOOD_EVENING"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "GOOD_EVENING"))
            self.aiVoiceResponseConfig["GOOD_BYE"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "GOOD_BYE"))
            self.aiVoiceResponseConfig["CYA_AGAIN"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "CYA_AGAIN"))
            self.aiVoiceResponseConfig["IM_SORRY"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "IM_SORRY"))
            self.aiVoiceResponseConfig["SORRY"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "SORRY"))
            self.aiVoiceResponseConfig["TRY_AGAIN_LATER"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "TRY_AGAIN_LATER"))
            self.aiVoiceResponseConfig["LEMME_TRY_AGAIN"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "LEMME_TRY_AGAIN"))
            self.aiVoiceResponseConfig["ALLOW_ME_TO_ENTERTAIN_YOU"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "ALLOW_ME_TO_ENTERTAIN_YOU"))
            self.aiVoiceResponseConfig["OFFER_HELP"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "OFFER_HELP"))
            self.aiVoiceResponseConfig["NO_PROBLEM"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "NO_PROBLEM"))
            self.aiVoiceResponseConfig["OK"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "OK"))
            self.aiVoiceResponseConfig["ALRIGHT"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "ALRIGHT"))
            self.aiVoiceResponseConfig["HAVE_A_NICE_DAY"] = os.path.join(path_to_sounds_folder, config.get("SOUND-EFFECTS", "HAVE_A_NICE_DAY"))
            
            logger.info(f"Configured {AsyncStdVoiceResponseMixin.__name__}")
            return
			
		
        logger.info("AsyncStdVoiceResponseMixin disabled")

    def checkTime(self):
        currentTime = self.aiVoiceResponseConfig["timezone"].localize(datetime.now())
        logger.debug(f"current time: {currentTime}")
        currentHour = currentTime.hour
        if currentHour >= 0 and currentHour < 12:
            key = "GOOD_MORNING"
        elif currentHour >= 12 and currentHour < 18:
            key = "GOOD_AFTNN"
        elif currentHour >= 18 and currentHour <= 23:
            key = "GOOD_EVENING"

        return key

    def greetedUser(self):
        time = self.checkTime()
        return self.greetingCheck[time]

    def greet(self, block = False):
        logger.debug(f"greet called. Enabled: {self.isUsed}")
        if self.isUsed:
            time = self.checkTime()
            self.voiceResponseSoundEngine.play(self.aiVoiceResponseConfig[time], block)
            self.greetingCheck[time] = True

    def offerHelp(self, block = False):
        logger.debug(f"offerHelp called. Enabled: {self.isUsed}")
        if self.isUsed:
            self.voiceResponseSoundEngine.play(self.aiVoiceResponseConfig["OFFER_HELP"], block)

    def tryLater(self, block = False):
        logger.debug(f"tryLater called. Enabled: {self.isUsed}")
        if self.isUsed:
            self.voiceResponseSoundEngine.play(self.aiVoiceResponseConfig["TRY_AGAIN_LATER"], block)

    def entertainUser(self, block = False):
        logger.debug(f"entertainUser called. Enabled: {self.isUsed}")
        if self.isUsed:
            self.voiceResponseSoundEngine.play(self.aiVoiceResponseConfig["ALLOW_ME_TO_ENTERTAIN_YOU"], block)
 
    def apologise(self, block = False):
        logger.debug(f"apologise called. Enabled: {self.isUsed}")
        if self.isUsed:
            apologies = [self.aiVoiceResponseConfig["IM_SORRY"], self.aiVoiceResponseConfig["SORRY"]]
            selectedApology = random.randint(0,1)
            self.voiceResponseSoundEngine.play(apologies[selectedApology], block)

    def sayBye(self, block = False):
        logger.debug(f"sayBye called. Enabled: {self.isUsed}")
        if self.isUsed:
            self.voiceResponseSoundEngine.play(self.aiVoiceResponseConfig["CYA_AGAIN"], block)
    
    def sayCya(self, block = False):
        logger.debug(f"sayCya called. Enabled: {self.isUsed}")
        if self.isUsed:
            self.voiceResponseSoundEngine.play(self.aiVoiceResponseConfig["GOOD_BYE"], block)
    
    def sayGoodDay(self, block = False):
        logger.debug(f"sayGoodDay called. Enabled: {self.isUsed}")
        if self.isUsed:
            self.voiceResponseSoundEngine.play(self.aiVoiceResponseConfig["HAVE_A_NICE_DAY"], block)



    def acknowledge(self, block = False):
        logger.debug(f"acknowledge called. Enabled: {self.isUsed}")
        if self.isUsed:
            acknowledgements = [
                self.aiVoiceResponseConfig["ALRIGHT"], 
                self.aiVoiceResponseConfig["NO_PROBLEM"],
                self.aiVoiceResponseConfig["OK"]
                ]
            selectedAcknowledgement = random.randint(0,2)
            logger.debug(f"Selected acknowledgement: {acknowledgements[selectedAcknowledgement]}")
            self.voiceResponseSoundEngine.play(acknowledgements[selectedAcknowledgement], block)

   