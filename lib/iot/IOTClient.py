
from abc import ABC, abstractmethod
from ..utils.utils import getSetUpConfig
from os.path import join

class IOTClient(ABC):
    ALLOWED_COMMANDS = getSetUpConfig(join("lib",
                                            "commands",
                                            "iotCommands.yaml"))

    def __init__(self, chosen_commands) -> None:
        chosen_commands = set(chosen_commands)
        allowed_cmds = set(IOTClient.ALLOWED_COMMANDS.keys())
        if not chosen_commands.issubset(allowed_cmds):
            raise ValueError(f"{chosen_commands.difference(allowed_cmds)} are not allowed")
        else:
            self.chosen_commands = chosen_commands

    @abstractmethod
    def publish(self, topic, msg):
        pass

    @abstractmethod
    def subscribe(self, topic):
        pass


