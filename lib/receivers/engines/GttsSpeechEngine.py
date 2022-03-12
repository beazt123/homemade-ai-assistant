import os
from gtts import gTTS
from io import BytesIO
from .speech_engine import SpeechEngine
from playsound import playsound
import logging


class GttsSpeechEngine(SpeechEngine):
    logger = logging.getLogger(__name__)
    def __init__(self, config) -> None:
        self.lang = config.get("AI-GTTS", "lang")
        self.tld = config.get("AI-GTTS", "tld", fallback="co.uk")

    def say(self, script: str) -> None:
        GttsSpeechEngine.logger.info(f"Saying: {script}")
        mp3_fp = "temp.mp3"
        try:
            tts = gTTS(script, lang=self.lang, tld=self.tld, slow=False)
            tts.save(mp3_fp)

            playsound(mp3_fp, block=True)
            GttsSpeechEngine.logger.info(f"Played: {script}")
            os.remove(mp3_fp)
        except AssertionError:
            GttsSpeechEngine.logger.warn("No text to speak")





    

    
    