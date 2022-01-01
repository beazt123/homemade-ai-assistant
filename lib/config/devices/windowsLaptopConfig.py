import logging
import pyttsx3
from speech_recognition import Microphone as computerMic


from ..config import config
from ...interpreters.RasaInterpreter import RasaInterpreter
from ...receivers.engines.sound_engine import SoundEngine
from ...receivers import *
from ...commands import (
    DefineWord,
    GetNews,
    DefaultCommand,
    GetWeatherForecast,
    GoogleSearch,
    PlayYoutubeVideo,
    ShutdownSystem,
    StartOfflineMusic,
    StopOfflineMusic,
    StopProgram,
    TellAJoke,
    TellTime,
    WikiSearch
)

logger = logging.getLogger(__name__)

speechEngine = pyttsx3.init()
soundEngine = SoundEngine()


englishDictionary = Dictionary(config, speechEngine)
logger.info(f"Created {Dictionary.__name__} ")

generalReception = GeneralReceiver(config, speechEngine)
logger.info(f"Created {GeneralReceiver.__name__} ")

newsCaster = News(config, speechEngine, soundEngine)
logger.info(f"Created {News.__name__} ")

offlineMusicPlayer = OfflineMusic(config, speechEngine)
logger.info(f"Created {OfflineMusic.__name__} ")

searcher = Searcher(config, speechEngine, soundEngine)
logger.info(f"Created {Searcher.__name__} ")

systemInterface = System(config, speechEngine, soundEngine)
logger.info(f"Created {System.__name__} ")

weatherForecaster = Weather(config, speechEngine)
logger.info(f"Created {Weather.__name__} ")

fallbackReceiver = FallbackReceiver(config, soundEngine)
logger.info(f"Created {FallbackReceiver.__name__} ")

commandsToUse = [
    DefineWord(englishDictionary),
    GetNews(newsCaster),
    GetWeatherForecast(weatherForecaster),
    GoogleSearch(searcher),
    PlayYoutubeVideo(searcher),
    ShutdownSystem(systemInterface),
    StartOfflineMusic(offlineMusicPlayer),
    StopOfflineMusic(offlineMusicPlayer),
    StopProgram(systemInterface),
    TellAJoke(generalReception),
    TellTime(generalReception),
    WikiSearch(searcher),
    DefaultCommand(fallbackReceiver)
]


configuredInterpreter = RasaInterpreter(config, soundEngine, computerMic())
logger.info(f"Created {Interpreter.__name__} ")
commandHooks = {command.__class__.__name__: command for command in commandsToUse}
