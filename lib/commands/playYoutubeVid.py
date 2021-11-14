from .command import Command

class PlayYoutubeVideo(Command):
    def __init__(self, searcher, searchStatement = None) -> None:
        self.receiver = searcher
        self.arg = searchStatement

    def __call__(self, searchStatement = None):
        if not self.arg:
            return self.receiver.youtube(self.arg)
        else:
            return self.receiver.youtube(searchStatement)
        