from .speechMixin import SpeechMixin
from .soundEffectsMixin import SoundEffectsMixin

class FallbackReceiver(SoundEffectsMixin):
    def __init__(self, config):
        SoundEffectsMixin.__init__(self, config)
    
    def execute(self):
        self.atEaseSound()

