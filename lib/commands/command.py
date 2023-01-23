from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def __init__(self, receiver):
        pass

    @abstractmethod
    def __call__(self, arg):
        pass
