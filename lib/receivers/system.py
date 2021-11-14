import logging
import os
import platform
# import subprocess


from .speechMixin import SpeechMixin
from .soundEffectsMixin import SoundEffectsMixin


class System(SpeechMixin, SoundEffectsMixin):
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
    def __init__(self, config, speechEngine):
        SpeechMixin.__init__(self, speechEngine)
        SoundEffectsMixin.__init__(self, config)
        self.platform = platform.system()

    def terminateProgramme(self):        
        logging.info("Exiting programme")
        self.switchOffSound(block = True)
        exit()

    def turnOffComputer(self):
        logging.info("Shutting down system")
        self.say("Alright. Shutting down your computer right now.")
        os.system(self.OS[self.platform]["shutdown"])

    # def openTerminal(self):
    #     self.say("Right away")
    #     logging.info("Launching terminal")
    #     subprocess.call(f'start {self.systemConfig.PATH_TO_POWERSHELL}', shell=True)
    #     logging.debug("Launched terminal")