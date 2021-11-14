from .command import Command

class StopProgram(Command):
    def __init__(self, system) -> None:
        self.receiver = system

    def __call__(self, arg):
        return self.receiver.terminateProgramme()
        