import logging
import os
import platform

from .mixins.speechMixin import SpeechMixin
from .mixins.soundEffectsMixin import SoundEffectsMixin
from .mixins.asyncStdVoiceResponseMixin import AsyncStdVoiceResponseMixin

logger = logging.getLogger(__name__)

class System(SpeechMixin, SoundEffectsMixin, AsyncStdVoiceResponseMixin):
    OS = {
        "Windows" : {
            "shutdown": "shutdown /s /t 1"
            },
        "Linux" : {
            "shutdown": "sudo shutdown now"
            },
        "Darwin" : {
            "shutdown": "sudo shutdown now"
            }
    }
    def __init__(self, 
                config, 
                speechEngine = None, 
                soundEngine = None):
        SpeechMixin.__init__(self, config, speechEngine)
        SoundEffectsMixin.__init__(self, config, soundEngine)
        AsyncStdVoiceResponseMixin.__init__(self, config, soundEngine)
        self.platform = platform.system()

    def terminateProgramme(self):        
        logger.info("Exiting programme")
        self.sayGoodDay(block = True)
        self.switchOffSound(block = True)
        exit()

    def turnOffComputer(self):
        logger.info("Shutting down system")
        self.acknowledge(block = True)
        self.sayBye()
        os.system(self.OS[self.platform]["shutdown"])

    # def openTerminal(self):
    #     self.say("Right away")
    #     logging.info("Launching terminal")
    #     subprocess.call(f'start {self.systemConfig.PATH_TO_POWERSHELL}', shell=True)
    #     logging.debug("Launched terminal")