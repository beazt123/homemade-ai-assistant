import logging
import pyttsx3
from speech_recognition import Microphone as computerMic

from ..config import config
from ...utils.interpreter import Interpreter
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

speechEngine = pyttsx3.init()

englishDictionary = Dictionary(config, speechEngine)
logging.info(f"Created {Dictionary.__name__} ")

generalReception = GeneralReceiver(config, speechEngine)
logging.info(f"Created {GeneralReceiver.__name__} ")

newsCaster = News(config, speechEngine)
logging.info(f"Created {News.__name__} ")

offlineMusicPlayer = OfflineMusic(config, speechEngine)
logging.info(f"Created {OfflineMusic.__name__} ")

searcher = Searcher(config, speechEngine)
logging.info(f"Created {Searcher.__name__} ")

systemInterface = System(config, speechEngine)
logging.info(f"Created {System.__name__} ")

weatherForecaster = Weather(config, speechEngine)
logging.info(f"Created {Weather.__name__} ")

fallbackReceiver = FallbackReceiver(config)
logging.info(f"Created {FallbackReceiver.__name__} ")

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


configuredInterpreter = Interpreter(config, computerMic())
commandHooks = {command.__class__.__name__: command for command in commandsToUse}
