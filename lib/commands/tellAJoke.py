from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from lib.receivers.general_receiver import GeneralReceiver
from .command import Command

class TellAJoke(Command):
    def __init__(self, receiver: GeneralReceiver) -> None:
        self.receiver = receiver

    def __call__(self, arg = None):
        return self.receiver.joke()
        