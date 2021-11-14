import logging
from .speechMixin import SpeechMixin
from .soundEffectsMixin import SoundEffectsMixin

class FallbackReceiver(SpeechMixin, SoundEffectsMixin):
    def __init__(self, config, speechEngine):
        SpeechMixin.__init__(self, speechEngine)
        SoundEffectsMixin.__init__(self, config)
    
    def execute(self):
        self.atEaseSound()

