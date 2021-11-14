from .command import Command

class TellTime(Command):
    def __init__(self, receiver) -> None:
        self.receiver = receiver

    def __call__(self):
        return self.receiver.time()
        