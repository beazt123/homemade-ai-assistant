from datetime import datetime
import logging
import pyjokes
from pytz import timezone

from .select_config import SelectConfig
from .mixins.speechMixin import SpeechMixin


class GeneralReceiver(SelectConfig, SpeechMixin):
    logger = logging.getLogger(__name__)
    def __init__(self, config, speechEngine = None):
        SpeechMixin.__init__(self, speechEngine)
        self.config = self.getConfig(config)
        self.timezone = timezone(self.config["timezone"])
        GeneralReceiver.logger.debug("Obtained Config")

    def getConfig(self, config):
        localConfig = dict()
        localConfig["timezone"] = config.get("LOCATION", "TIMEZONE")
        GeneralReceiver.logger.debug(f"{self.__class__.__name__} fetched timezone from config: {localConfig['timezone']}")
        return localConfig

    def time(self):
        timeNow = self.timezone.localize(datetime.now()).strftime('%I:%M %p')
        msg = f'Current time is {timeNow}'
        GeneralReceiver.logger.info(msg)
        print(msg)
        self.say(msg)

    def joke(self):    
        joke = pyjokes.get_joke()
        GeneralReceiver.logger.info(f"Requested joke: {joke}")
        print(joke)
        self.say(joke)