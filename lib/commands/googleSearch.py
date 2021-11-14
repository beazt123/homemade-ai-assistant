from .command import Command

class GoogleSearch(Command):
    def __init__(self, searcher, searchStatement = None) -> None:
        self.receiver = searcher
        self.arg = searchStatement

    def __call__(self, searchStatement = None):
        if not self.arg:
            return self.receiver.google(self.arg)
        else:
            return self.receiver.google(searchStatement)
        