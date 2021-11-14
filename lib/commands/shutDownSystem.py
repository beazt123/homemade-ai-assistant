from .command import Command

class ShutdownSystem(Command):
    def __init__(self, system) -> None:
        self.receiver = system

    def __call__(self):
        return self.receiver.turnOffComputer()
        