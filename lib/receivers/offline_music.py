from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from lib.receivers.receiver import Receiver

if TYPE_CHECKING:
    from lib.runtime_context.engines import SpeechEngine

from lib.runtime_context.config import Config
from itertools import chain
import logging
import random
import os

from glob import glob, iglob
from multiprocessing import Process
from lib.commands.startOfflineMusic import StartOfflineMusic
from lib.commands.stopOfflineMusic import StopOfflineMusic


from playsound import playsound, PlaysoundException


class OfflineMusic(Receiver):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.speech_engine: SpeechEngine = None
        self.local_music_folder = None
        self.music_file_extension = None

        self._music_process = None

    def set_config(self, context: Config):
        self.configure(context.static_config)
        self.speech_engine = context.runtime_context.speech_engine

    @property
    def short_description(self) -> str:
        return "PLAY / STOP the MUSIC:"

    @property
    def user_guide(self) -> Iterable[str]:
        return (
            "Plays a random music on a pre-set directory",
            "I.e. 'play some music', 'stop the music'"
        )

    @property
    def commands(self):
        return StartOfflineMusic, StopOfflineMusic

    @staticmethod
    def play_playlist(playlist):
        for song in playlist:
            try:
                playsound(song)
            except PlaysoundException:
                pass

    @staticmethod
    def generate_all_music_files(exts=["mp3"]):
        home_drive = os.getenv("HOMEDRIVE")
        home_path = os.getenv("HOMEPATH")
        home_full_path = os.path.join(home_drive, home_path)

        generator_list = [iglob(os.path.join(home_full_path, f"**/*.{ext}"), recursive=True) for ext in exts]

        generator = chain(*generator_list)

        return generator

    def configure(self, config):
        self.local_music_folder = config.get("OFFLINE-MUSIC", "path_to_local_music_folder")
        self.music_file_extension = config.get("OFFLINE-MUSIC", "music_ext")
        self.__class__.logger.debug("Loaded config localMusicFolder: %s, File ext: %s", self.local_music_folder,
                                    self.music_file_extension)

    def setup(self):
        if self._music_process is not None:
            self.__class__.logger.info("Music playing currently. Stopping music process")
            self._music_process.terminate()
            self._music_process = None
            self.__class__.logger.info("Killed current music process")

    def stop(self):
        self.setup()

    def shuffle_play(self):
        self.setup()
        music_path = os.path.join(self.local_music_folder,
                                  f"*.{self.music_file_extension}")
        system_music = glob(music_path)
        self.__class__.logger.info("Searching for music at: %s", music_path)
        random.shuffle(system_music)

        self.speech_engine.say("Ok. Playing music from your music library in shuffle mode")
        self.__class__.logger.debug(system_music)

        if len(system_music) == 0:
            self.__class__.logger.warn("No music found in specified directory. Scanning the computer for music")
            system_music = self.__class__.generate_all_music_files()
            self.__class__.logger.info("Scanned music in computer")

        self.__class__.logger.info("Starting music player")
        self._music_process = Process(target=self.__class__.play_playlist, args=(system_music,))
        self._music_process.daemon = True
        self.__class__.logger.debug("Created process to play music")
        self._music_process.start()
        self.__class__.logger.info("Started process to play music")
