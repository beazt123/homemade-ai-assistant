from __future__ import annotations
import typing


if typing.TYPE_CHECKING:
    from lib.receivers.search import Searcher
    
from .command import Command

class GoogleSearch(Command):
    def __init__(self, searcher: Searcher, searchStatement: str = None) -> None:
        self.receiver = searcher
        self.arg = searchStatement

    def __call__(self, searchStatement = None):
        if not self.arg:
            return self.receiver.google(searchStatement)
        else:
            return self.receiver.google(self.arg)
        