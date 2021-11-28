import logging

logger = logging.getLogger(__name__)

class SpeechMixin:
    def __init__(self, config = None, speechEngine = None) -> None:
        self.engine = speechEngine
        if config and self.engine:
            self.engine.setProperty('rate', config.getint("AI", "voice_speed_WPM"))     # setting up new voice rate in words per minute. Default 200
            logger.debug("Set AI talk speed")
            self.engine.setProperty('volume', config.getfloat("AI", "voice_vol")) # 0 - 1
            logger.debug("Set AI volume")
            
            voices = self.engine.getProperty('voices')       #getting details of current voice

            gender = config.get("AI", "ai_gender")
            if gender.lower() == "male":
                voiceIdx = 0
            elif gender.lower() == "female":
                voiceIdx = 1

            self.engine.setProperty('voice', voices[voiceIdx].id)   #changing index, changes voices. 1 for female
            logger.debug("Set AI gender")

        logger.info(f"Using voice speech engine: {bool(self.engine)}")

    

    def say(self, script):
        if self.engine:
            self.engine.say(script)
            logger.debug(f"Saying: {script}")
            self.engine.runAndWait()
            return
        logger.debug(f"Ignored as no SpeechEngine is provided: {script}")