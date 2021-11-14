from .command import Command

class WikiSearch(Command):
    def __init__(self, searcher, searchStatement = None) -> None:
        self.receiver = searcher
        self.arg = searchStatement

    def __call__(self, searchStatement = None):
        if not self.arg:
            return self.receiver.wiki(searchStatement)
        else:
            return self.receiver.wiki(self.arg)
        