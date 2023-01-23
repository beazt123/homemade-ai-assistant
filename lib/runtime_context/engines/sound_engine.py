# TODO: Make this class OS-aware
import logging
from playsound import playsound


class SoundEngine:
    logger = logging.getLogger(__name__)
    
    def __init__(self) -> None:
        self.soundPlayer = playsound

    def playSync(self, fullFileName):
        SoundEngine.logger.debug(f"Playing synchronously: {fullFileName}")
        self.soundPlayer(fullFileName, block=True)

    def playAsync(self, fullFileName):
        SoundEngine.logger.debug(f"Playing asynchronously: {fullFileName}")
        self.soundPlayer(fullFileName, block=False)

    def play(self, fullFilename, block):
        if block:
            self.playSync(fullFilename)
        else:
            self.playAsync(fullFilename)

