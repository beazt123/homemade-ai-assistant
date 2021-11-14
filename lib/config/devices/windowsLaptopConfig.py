import logging
import warnings

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
generalReception = GeneralReceiver(config, speechEngine)
newsCaster = News(config, speechEngine)
offlineMusicPlayer = OfflineMusic(config, speechEngine)
searcher = Searcher(config, speechEngine)
systemInterface = System(config, speechEngine)
weatherForecaster = Weather(config, speechEngine)
fallbackReceiver = FallbackReceiver(config, speechEngine)

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