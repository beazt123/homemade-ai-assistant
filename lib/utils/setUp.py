import logging
import pyttsx3
import yaml
import paho.mqtt.client as mqtt

from speech_recognition import Microphone as computerMic

from .WakeWordDetector import WakeWordDetector
from .interpreter import Interpreter
from .dispatcher import Dispatcher
from ..invoker import Invoker
from ..receivers.engines.sound_engine import SoundEngine
from ..receivers import *
from ..commands import (
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

'''
logger

import & read all config

intialise system level objects: speech engine, sound engine

Initialise & configure receivers

create a command hook dictionary -> create & configure invoker

wrap invoker with dispatcher
'''
logger = logging.getLogger(__name__)

class App:
    def __init__(self, 
                 wakeWordDetector = None,
                 interpreter = None,
                 dispatcher = None) -> None:
        self.wakeWordDetector = wakeWordDetector
        self.interpreter = interpreter
        self.dispatcher = dispatcher

def set_up_iot_client(config):
    client = mqtt.Client("P1") #create new instance
    client.connect(config.get("MQTT", "IP_ADDR")) #connect to broker
    # client.publish("topic1","HURRAY IT WORKS") #publish
    return client

def readSetUpConfig(filepath):
    with open(filepath, 'r') as stream:
        dictionary = yaml.load(stream)
        # for key, value in dictionary.items():
        #     print (key + " : " + str(value))
    return dictionary
        
def createApp(config, setUpConfig) -> App:
    wakeWordDetector = WakeWordDetector()
    config = None
    soundEngine = SoundEngine()
    speechEngine = pyttsx3.init()
    
    # setUpConfig["type"] == "standalone"
    
    commandsToUse = list()
    receivers = setUpConfig["receivers"]
    if "Dictionary" in receivers:
        englishDictionary = Dictionary(config, speechEngine)
        logger.info(f"Created {Dictionary.__name__} ")
        commandsToUse.append(DefineWord(englishDictionary))
    if "GeneralReceiver" in receivers:
        generalReception = GeneralReceiver(config, speechEngine)
        logger.info(f"Created {GeneralReceiver.__name__} ")
        commandsToUse.extend([
            TellAJoke(generalReception),
            TellTime(generalReception)
        ])
    if "News" in receivers:
        newsCaster = News(config, speechEngine, soundEngine)
        logger.info(f"Created {News.__name__} ")
        commandsToUse.append(GetNews(newsCaster))
    if "OfflineMusic" in receivers:
        offlineMusicPlayer = OfflineMusic(config, speechEngine)
        logger.info(f"Created {OfflineMusic.__name__} ")
        commandsToUse.extend([
            StartOfflineMusic(offlineMusicPlayer),
            StopOfflineMusic(offlineMusicPlayer)
        ])
    if "Searcher" in receivers:
        searcher = Searcher(config, speechEngine, soundEngine)
        logger.info(f"Created {Searcher.__name__} ")
        commandsToUse.extend([
            GoogleSearch(searcher),
            PlayYoutubeVideo(searcher),
            WikiSearch(searcher)
        ])
    if "System" in receivers:
        systemInterface = System(config, speechEngine, soundEngine)
        logger.info(f"Created {System.__name__} ")
        commandsToUse.extend([
            StopProgram(systemInterface),
            ShutdownSystem(systemInterface)
        ])
    if "Weather" in receivers:
        weatherForecaster = Weather(config, speechEngine)
        logger.info(f"Created {Weather.__name__} ")
        commandsToUse.append(GetWeatherForecast(weatherForecaster))

    fallbackReceiver = FallbackReceiver(config, soundEngine)
    logger.info(f"Created {FallbackReceiver.__name__} ")
    commandsToUse.append(DefaultCommand(fallbackReceiver))
    
    commandHooks = {command.__class__.__name__: command for command in commandsToUse}
    
    invoker = Invoker()
    invoker.registerAll(commandHooks)
    dispatcher = Dispatcher(invoker, set_up_iot_client())
    
    interpreter = Interpreter(config, soundEngine, computerMic())
    logger.info(f"Created {Interpreter.__name__} ")
    
    return App(wakeWordDetector, interpreter, dispatcher)
    