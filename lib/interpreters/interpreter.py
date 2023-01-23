from __future__ import annotations
import logging
from typing import Any, Tuple
import speech_recognition as sr
from abc import abstractmethod
from lib.runtime_context.config import Config

from lib.commands.meta_command import MetaCommand

from typing import TYPE_CHECKING

from lib.runtime_context.configurable import Configurable
from lib.runtime_context.mixins.async_std_voice_responses import AsyncStdVoiceResponses
from lib.runtime_context.mixins.sound_effects import SoundEffects

if TYPE_CHECKING:
    from lib.commands.command import Command


class Interpreter(Configurable):
    logger = logging.getLogger(__name__)
    FAILED_TOKEN = "!FAILED"

    def __init__(self):
        self.__class__.logger.info(f"Creating Sound effects mixin for {self.__class__.__name__}")
        self.sound_effects: SoundEffects = None

        self.__class__.logger.info(f"Creating Async standard AI voice response mixin for {self.__class__.__name__}")
        self.async_std_voice_responses: AsyncStdVoiceResponses = None
        self.__class__.logger.info(f"Created Async standard AI voice response mixin for {self.__class__.__name__}")

        self.recogniser = sr.Recognizer()
        self.listener = None
        self.__class__.logger.debug(f"Created speech recongizer object for {self.__class__.__name__}")

    def set_config(self, config: Config):
        self.async_std_voice_responses = config.runtime_context.async_std_voice_responses
        self.listener = config.runtime_context.mic
        self.sound_effects = config.runtime_context.sound_effects_engine

    def __del__(self):
        try:
            del self.listener
            del self.recogniser
        # self.engine.tearDown()
        except AttributeError:
            pass

    def adjust_for_ambient_noise(self):
        self.__class__.logger.debug("Calibrating Mic")
        with self.listener as source:
            self.recogniser.adjust_for_ambient_noise(source, duration=0.3)

    def listen_and_transcribe(self):
        try:
            with self.listener as source:
                try:
                    self.__class__.logger.info("Listening...")
                    voice = self.recogniser.listen(source, timeout=2.5, phrase_time_limit=4)

                    self.__class__.logger.debug("Voice received")
                    command = self.transcribe(voice)
                    self.__class__.logger.debug("Transcribed voice")
                    command = command.strip().lower()
                    self.__class__.logger.info(f"Detected command: {command}")
                except sr.WaitTimeoutError:
                    self.__class__.logger.info("User didn't speak")
                    command = self.__class__.FAILED_TOKEN
        except sr.UnknownValueError:
            self.__class__.logger.debug("No voice detected")
            command = self.__class__.FAILED_TOKEN

        return command

    def interpret(self) -> MetaCommand:
        if self.async_std_voice_responses.greeted_user():
            self.sound_effects.ready_sound()
        else:
            self.async_std_voice_responses.greet(block=True)
            self.async_std_voice_responses.offer_help(block=True)

        transcription = self.listen_and_transcribe()
        command, args = self.process(transcription)
        self.__class__.logger.info(f"Event: {command}, Data: {args}")

        return MetaCommand(command, args)

    def transcribe(self, audio):
        try:
            command = self.recogniser.recognize_google(audio)
            self.__class__.logger.info("Used Google online transcription service")
        except sr.RequestError:
            self.__class__.logger.warning("Internet unavailable. Using offline TTS")
            command = self.recogniser.recognize_sphinx(audio)
            self.__class__.logger.info("Used Sphinx offline transcription service")

        self.__class__.logger.info(f"Transcription: {command}")
        return command

    @classmethod
    @abstractmethod
    def process(cls, command: Command) -> Tuple[Command, Any]:
        '''Break down the command into Event and data objects'''
        pass
