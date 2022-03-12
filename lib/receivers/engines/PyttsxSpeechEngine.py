import logging
import pyttsx3
from .speech_engine import SpeechEngine

class PyttsxSpeechEngine(SpeechEngine):
    logger = logging.getLogger(__name__)
    
    def __init__(self, config) -> None:
        self.engine = pyttsx3.init()
        
        self.engine.setProperty('rate', config.getint("AI-PYTTSX3", "voice_speed_WPM", fallback=150))     # setting up new voice rate in words per minute. Default 200
        self.engine.setProperty('volume', config.getfloat("AI-PYTTSX3", "voice_vol", fallback=1)) # 0 - 1
        
        voices = self.engine.getProperty('voices')       #getting details of current voice

        gender = config.get("AI-PYTTSX3", "ai_gender", fallback="female")
        if gender.lower() == "male":
            voiceIdx = 0
        elif gender.lower() == "female":
            voiceIdx = 1

        self.engine.setProperty('voice', voices[voiceIdx].id)   #changing index, changes voices. 1 for female


    

    def say(self, script: str) -> None:
        self.engine.say(script)
        self.engine.runAndWait()