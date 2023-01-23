from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from lib.receivers.fallbackReceiver import FallbackReceiver
from .command import Command
class DefaultCommand(Command):
    def __init__(self, fallbackReceiver: FallbackReceiver) -> None:
        self.receiver = fallbackReceiver

    def __call__(self, arg = None):
        self.receiver.execute()
