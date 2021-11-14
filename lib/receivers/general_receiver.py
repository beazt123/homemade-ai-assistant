import datetime
import logging
import pyjokes
from pytz import timezone

from .select_config import SelectConfig
from .speechMixin import SpeechMixin

class GeneralReceiver(SelectConfig, SpeechMixin):
    def __init__(self, config, speechEngine):
        SpeechMixin.__init__(self, speechEngine)
        self.config = self.getConfig(config)
        self.timezone = timezone(self.config["timezone"])
        logging.info("Obtained Config")

    def getConfig(self, config):
        logging.debug(f"{self.__class__.__name__} fetching config.")
        localConfig = dict()
        localConfig["timezone"] = config.get("LOCATION", "TIMEZONE")
        logging.debug(f"{self.__class__.__name__} fetched config.")
        return localConfig

    def time(self):
        timeNow = self.timezone.localize(datetime.now()).strftime('%I:%M %p')
        msg = f'Current time is {timeNow}'
        print(msg)
        self.say(msg)

    def joke(self):    
        joke = pyjokes.get_joke()
        print(joke)
        self.say(joke)