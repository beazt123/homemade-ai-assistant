from abc import ABC, abstractmethod

class SelectConfig(ABC):
  @abstractmethod
  def getConfig(self, config):
      return
