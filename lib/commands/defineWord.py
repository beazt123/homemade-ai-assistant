from .command import Command

class DefineWord(Command):
    def __init__(self, dictionary, wordToDefine = None) -> None:
        self.receiver = dictionary
        self.arg = wordToDefine

    def __call__(self, arg = None):
        if not self.arg:
            return self.receiver.define(arg)
        else:
            return self.receiver.define(self.arg)
