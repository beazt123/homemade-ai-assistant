from .command import Command

class StopOfflineMusic(Command):
    def __init__(self, musicPlayer) -> None:
        self.receiver = musicPlayer

    def __call__(self, arg):
        return self.receiver.stop()
        