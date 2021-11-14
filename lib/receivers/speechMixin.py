import logging

class SpeechMixin:
    def __init__(self, config, speechEngine = None) -> None:
        self.engine = speechEngine
        if self.engine:
            self.engine.setProperty('rate', config.getint("AI", "voice_speed_WPM"))     # setting up new voice rate in words per minute. Default 200
            logging.debug("Set AI talk speed")
            self.engine.setProperty('volume', config.getfloat("AI", "voice_vol")) # 0 - 1
            logging.debug("Set AI volume")
            
            voices = self.engine.getProperty('voices')       #getting details of current voice

            gender = config.get("AI", "ai_gender")
            if gender.lower() == "male":
                voiceIdx = 0
            elif gender.lower() == "female":
                voiceIdx = 1

            self.engine.setProperty('voice', voices[voiceIdx].id)   #changing index, changes voices. 1 for female
            logging.debug("Set AI gender")

        logging.info(f"Using voice speech engine: {bool(self.engine)}")

    

    def say(self, script):
        logging.debug(f"Script: {script}\nEngine: {self.engine}")
        if self.engine:
            self.engine.say(script)
            self.engine.runAndWait()