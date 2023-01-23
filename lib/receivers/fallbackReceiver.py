from __future__ import annotations
from typing import TYPE_CHECKING, Iterable


if TYPE_CHECKING:
    from lib.runtime_context.mixins.sound_effects import SoundEffects
from lib.runtime_context.config import Config
import logging
from lib.commands.default import DefaultCommand
from lib.receivers.receiver import Receiver


class FallbackReceiver(Receiver):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.sound_effects_engine: SoundEffects = None

    def set_config(self, context: Config):
        self.sound_effects_engine = context.runtime_context.sound_effects_engine

    @property
    def commands(self):
        return DefaultCommand,

    @property
    def user_guide(self) -> Iterable[str]:
        return ()

    @property
    def short_description(self) -> str:
        return ""

    def execute(self):
        self.__class__.logger.info(f"{self.__class__.__name__} called")
        self.sound_effects_engine.at_ease_sound()
