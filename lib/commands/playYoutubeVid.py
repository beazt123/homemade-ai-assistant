from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from lib.receivers.search import Searcher

from .command import Command


class PlayYoutubeVideo(Command):
    def __init__(self, searcher: Searcher, search_statement: str = None) -> None:
        self.receiver = searcher
        self.arg = search_statement

    def __call__(self, search_statement=None):
        if not self.arg:
            return self.receiver.youtube(search_statement)
        else:
            return self.receiver.youtube(self.arg)
