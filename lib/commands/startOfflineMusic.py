from .command import Command

class StartOfflineMusic(Command):
    def __init__(self, musicPlayer) -> None:
        self.receiver = musicPlayer

    def __call__(self):
        return self.receiver.shufflePlay()
        