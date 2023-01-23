from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from lib.receivers.dictionary import Dictionary

from .command import Command

class DefineWord(Command):
    def __init__(self, dictionary: Dictionary, wordToDefine = None) -> None:
        self.receiver = dictionary
        self.arg = wordToDefine

    def __call__(self, arg):
        if not self.arg:
            return self.receiver.define(arg)
        else:
            return self.receiver.define(self.arg)
