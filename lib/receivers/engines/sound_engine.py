# TODO: Make this class OS-aware
import logging
from playsound import playsound

logger = logging.getLogger(__name__)

class SoundEngine:
    def __init__(self) -> None:
        self.soundPlayer = playsound

    def playSync(self, fullFileName):
        logger.debug(f"Playing synchronously: {fullFileName}")
        self.soundPlayer(fullFileName, block=True)

    def playAsync(self, fullFileName):
        logger.debug(f"Playing asynchronously: {fullFileName}")
        self.soundPlayer(fullFileName, block=False)

    def play(self, fullFilename, block):
        if block:
            self.playSync(fullFilename)
        else:
            self.playAsync(fullFilename)

