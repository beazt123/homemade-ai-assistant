import logging

class SpeechMixin:
    logger = logging.getLogger(__name__)
    def __init__(self, speechEngine = None) -> None:
        if speechEngine:
            self.engine = speechEngine
        SpeechMixin.logger.info(f"Using voice speech engine: {bool(self.engine)}")

    def say(self, script):
        if self.engine:
            self.engine.say(script)
            SpeechMixin.logger.debug(f"Saying: {script}")
            return
        SpeechMixin.logger.debug(f"Ignored as no SpeechEngine is provided: {script}")