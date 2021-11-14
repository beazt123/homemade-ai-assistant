import logging

class SpeechMixin:
    def __init__(self, speechEngine = None) -> None:
        self.engine = speechEngine

    def say(self, script):
        logging.debug(f"Script: {script}\nEngine: {self.engine}")
        if self.engine:
            self.engine.say(script)
            self.engine.runAndWait()