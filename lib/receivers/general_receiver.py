from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from configparser import ConfigParser
    from lib.runtime_context.engines import SpeechEngine

from lib.runtime_context.config import Config
from datetime import datetime
import logging
from dadjokes import Dadjoke
from pytz import timezone
from lib.commands.tellAJoke import TellAJoke
from lib.commands.tellTime import TellTime
from lib.receivers.receiver import Receiver


class GeneralReceiver(Receiver):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.timezone = None
        self.speech_engine: SpeechEngine = None

    def set_config(self, context: Config):
        self.configure(context.static_config)
        self.speech_engine = context.runtime_context.speech_engine

    @property
    def short_description(self) -> str:
        return "TELL you the TIME / a JOKE:"

    @property
    def user_guide(self) -> Iterable[str]:
        return (
            "Tells you a joke or the time",
            "I.e. 'tell me the time', 'tell me a joke'"
        )

    @property
    def commands(self):
        return TellTime, TellAJoke

    def configure(self, config: ConfigParser):
        self.timezone = timezone(config.get("LOCATION", "TIMEZONE"))
        self.__class__.logger.debug("%s fetched timezone from config: %s", self.__class__.__name__, self.timezone)

    def time(self):
        time_now = self.timezone.localize(datetime.now()).strftime('%I:%M %p')
        msg = f'Current time is {time_now}'
        self.__class__.logger.info(msg)
        print(msg)
        self.speech_engine.say(msg)

    def joke(self):
        dad_joke = Dadjoke()

        self.__class__.logger.info(f"Requested joke: {dad_joke.joke}")
        print(dad_joke.joke)
        self.speech_engine.say(dad_joke.joke)
