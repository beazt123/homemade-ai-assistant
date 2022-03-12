import logging
from .mixins.soundEffectsMixin import SoundEffectsMixin


class FallbackReceiver(SoundEffectsMixin):
    logger = logging.getLogger(__name__)
    def __init__(self, config, soundEngine):
        SoundEffectsMixin.__init__(self, config, soundEngine)
    
    def execute(self):
        FallbackReceiver.logger.info(f"{FallbackReceiver.__name__} called")
        self.atEaseSound()

