
from abc import ABC, abstractmethod

class SpeechEngine(ABC):
    @abstractmethod
    def say(self, something: str) -> None:
        pass