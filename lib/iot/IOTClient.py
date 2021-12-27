
from abc import ABC, abstractmethod

class IOTClient(ABC):
    @abstractmethod
    def publish(self, topic, msg):
        pass

    @abstractmethod
    def subscribe(self, topic):
        pass


