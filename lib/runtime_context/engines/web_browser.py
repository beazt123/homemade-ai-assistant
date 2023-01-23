from abc import ABC, abstractmethod


class WebBrowser(ABC):
    @abstractmethod
    def open(self, url: str):
        pass
