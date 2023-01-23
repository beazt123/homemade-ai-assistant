from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from lib.receivers.system import System
from .command import Command

class StopProgram(Command):
    def __init__(self, system: System) -> None:
        self.receiver = system

    def __call__(self, arg = None):
        return self.receiver.terminate_programme()
        