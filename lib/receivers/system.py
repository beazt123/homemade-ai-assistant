from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from lib.receivers.receiver import Receiver

if TYPE_CHECKING:
    from lib.runtime_context.mixins.async_std_voice_responses import AsyncStdVoiceResponses
from lib.runtime_context.config import Config
import logging
import os
import platform
from lib.commands.shutDownSystem import ShutdownSystem
from lib.commands.stopProgram import StopProgram


class System(Receiver):
    logger = logging.getLogger(__name__)
    OS = {
        "Windows": {
            "shutdown": "shutdown /s /t 1"
        },
        "Linux": {
            "shutdown": "sudo shutdown now"
        },
        "Darwin": {
            "shutdown": "sudo shutdown now"
        }
    }

    def __init__(self):
        self.platform = platform.system()
        self.async_std_voice_responses: AsyncStdVoiceResponses = None

    def set_config(self, context: Config):
        self.async_std_voice_responses = context.runtime_context.async_std_voice_responses

    @property
    def short_description(self) -> str:
        return "SHUTDOWN COMPUTER:"

    @property
    def user_guide(self) -> Iterable[str]:
        return (
            "Shuts down the computer. Rmb to save your work!",
            "I.e. 'shut down computer!'"
        )

    @property
    def commands(self):
        return StopProgram, ShutdownSystem

    def terminate_programme(self):
        self.__class__.logger.info("Exiting programme")
        self.async_std_voice_responses.say_good_day(block=True)
        self.async_std_voice_responses.switchOffSound(block=True)
        exit()

    def turn_off_computer(self):
        self.__class__.logger.info("Shutting down system")
        self.async_std_voice_responses.acknowledge(block=True)
        self.async_std_voice_responses.say_bye()
        os.system(self.OS[self.platform]["shutdown"])
