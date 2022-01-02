import logging
from .mixins.soundEffectsMixin import SoundEffectsMixin

logger = logging.getLogger(__name__)

class FallbackReceiver(SoundEffectsMixin):
    def __init__(self, config, soundEngine):
        SoundEffectsMixin.__init__(self, config, soundEngine)
    
    def execute(self):
        logger.info(f"{FallbackReceiver.__name__} called")
        self.atEaseSound()

