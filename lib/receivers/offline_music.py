import logging
import random
import os

from glob import glob
from multiprocessing import Process

from .select_config import SelectConfig
from .speechMixin import SpeechMixin

from ..utils.utils import playPlaylist, generateAllMusicFiles


class OfflineMusic(SelectConfig, SpeechMixin):
    def __init__(self, config, speechEngine):
        SpeechMixin.__init__(self, speechEngine)
        self.config = self.getConfig(config)

        self._musicProcess = None

    def getConfig(self, config):
        localConfig = dict()
        localConfig["local_music_folder"] = config.get("OFFLINE-MUSIC","path_to_local_music_folder")
        localConfig["file_ext"] = config.get("OFFLINE-MUSIC","music_ext")
        return localConfig

    def setup(self):
        if self._musicProcess != None:
            logging.info("Music playing currently. Stopping previous music process")
            self._musicProcess.terminate()
            self._musicProcess = None
            logging.debug("Killed current music process")
        logging.debug("Music setup complete")

    def stop(self):
        self.setup()
    
    def shufflePlay(self):
        self.setup()
        systemMusic = glob(os.path.join(self.config["local_music_folder"], 
                                        f"*.{self.config['file_ext']}"))
                
        random.shuffle(systemMusic)

        self.say("Ok. Playing music from your music library in shuffle mode")
        logging.debug(systemMusic)

        if len(systemMusic) == 0:
            logging.warn("No music found in specified directory. Scanning the computer for music")
            systemMusic = generateAllMusicFiles()

            logging.debug("Scanned music in computer")
            self._musicProcess = Process(target=playPlaylist, args=(systemMusic,))
            self._musicProcess.daemon = True
            logging.debug("Created process to play music")
            self._musicProcess.start()
            logging.debug("Started process to play music")
