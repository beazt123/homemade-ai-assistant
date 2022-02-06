import logging
from .interpreter import Interpreter
from .RasaInterpreter import RasaInterpreterException, RasaInterpreter
from .RegexInterpreter import RegexInterpreter

class MasterInterpreter(Interpreter):
    USER_GUIDE = "Using Master Interpreter"
    logger = logging.getLogger(__name__)
    rasaInterpreter = RasaInterpreter
    regexInterpreter = RegexInterpreter

    @classmethod
    def process(cls, command):
        try:
            cls.logger.info("Attempting to use RasaInterpreter")
            event, data = cls.rasaInterpreter.process(command)
            cls.logger.info(f"Command processed successfully with RasaInterpreter: {event}({data})")
        except RasaInterpreterException:
            cls.logger.warn("Rasa server unreachable. Reverting to RegexInterpreter")
            event, data = cls.regexInterpreter.process(command)
            cls.logger.info(f"Command processed successfully with RegexInterpreter: {event}({data})")
            print("Rasa server down. Here's how to talk to the backup bot:\n")
            print(cls.regexInterpreter.getUserGuide())
        
        return event, data