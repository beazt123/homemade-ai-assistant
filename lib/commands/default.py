from .command import Command

class DefaultCommand(Command):
    def __init__(self, fallbackReceiver) -> None:
        self.receiver = fallbackReceiver

    def __call__(self, arg):
        self.receiver.execute()
