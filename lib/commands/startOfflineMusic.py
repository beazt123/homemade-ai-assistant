from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from lib.receivers.offline_music import OfflineMusic
from .command import Command

class StartOfflineMusic(Command):
    def __init__(self, musicPlayer: OfflineMusic) -> None:
        self.receiver = musicPlayer

    def __call__(self, arg):
        return self.receiver.shuffle_play()
        