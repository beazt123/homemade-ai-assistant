import logging
import random
import os

from glob import glob
from multiprocessing import Process

from .select_config import SelectConfig
from .mixins.speechMixin import SpeechMixin

from ..utils.utils import playPlaylist, generateAllMusicFiles


class OfflineMusic(SelectConfig, SpeechMixin):
    logger = logging.getLogger(__name__)
    def __init__(self, config, speechEngine = None):
        SpeechMixin.__init__(self, speechEngine)
        self.config = self.getConfig(config)

        self._musicProcess = None

    def getConfig(self, config):
        localConfig = dict()
        localConfig["local_music_folder"] = config.get("OFFLINE-MUSIC","path_to_local_music_folder")
        localConfig["file_ext"] = config.get("OFFLINE-MUSIC","music_ext")
        OfflineMusic.logger.debug(f"Loaded config localMusicFolder: {localConfig['local_music_folder']}, File ext: {localConfig['file_ext']}")
        return localConfig

    def setup(self):
        if self._musicProcess != None:
            OfflineMusic.logger.info("Music playing currently. Stopping music process")
            self._musicProcess.terminate()
            self._musicProcess = None
            OfflineMusic.logger.info("Killed current music process")

    def stop(self):
        self.setup()
    
    def shufflePlay(self):
        self.setup()
        musicPath = os.path.join(self.config["local_music_folder"], 
								f"*.{self.config['file_ext']}")
        systemMusic = glob(musicPath)
        OfflineMusic.logger.info(f"Searching for music at: {musicPath}")
        random.shuffle(systemMusic)

        self.say("Ok. Playing music from your music library in shuffle mode")
        OfflineMusic.logger.debug(systemMusic)

        if len(systemMusic) == 0:
            OfflineMusic.logger.warn("No music found in specified directory. Scanning the computer for music")
            systemMusic = generateAllMusicFiles()
            OfflineMusic.logger.info("Scanned music in computer")
        
        OfflineMusic.logger.info("Starting music player")
        self._musicProcess = Process(target=playPlaylist, args=(systemMusic,))
        self._musicProcess.daemon = True
        OfflineMusic.logger.debug("Created process to play music")
        self._musicProcess.start()
        OfflineMusic.logger.info("Started process to play music")
