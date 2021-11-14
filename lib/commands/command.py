from abc import ABC, abstractmethod

class Command(ABC):

  @abstractmethod
  def __call__(self, arg = None):
      return