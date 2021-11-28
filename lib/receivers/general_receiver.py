import datetime
import logging
import pyjokes
from pytz import timezone

from .select_config import SelectConfig
from .speechMixin import SpeechMixin

logger = logging.getLogger(__name__)

class GeneralReceiver(SelectConfig, SpeechMixin):
    def __init__(self, config, speechEngine = None):
        SpeechMixin.__init__(self, config, speechEngine)
        self.config = self.getConfig(config)
        self.timezone = timezone(self.config["timezone"])
        logger.debug("Obtained Config")

    def getConfig(self, config):
        localConfig = dict()
        localConfig["timezone"] = config.get("LOCATION", "TIMEZONE")
        logger.debug(f"{self.__class__.__name__} fetched timezone from config: {localConfig['timezone']}")
        return localConfig

    def time(self):
        timeNow = self.timezone.localize(datetime.now()).strftime('%I:%M %p')
        msg = f'Current time is {timeNow}'
        logger.info(msg)
        print(msg)
        self.say(msg)

    def joke(self):    
        joke = pyjokes.get_joke()
        logger.info(f"Requested joke: {joke}")
        print(joke)
        self.say(joke)