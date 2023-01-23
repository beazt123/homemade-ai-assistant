import logging
import requests
from requests.exceptions import Timeout
from lib.dispatchers.iot.IOTClient import IOTClient
from .interpreter import Interpreter
from lib.commands import (
    DefineWord,
    GetNews,
    GetWeatherForecast,
    GoogleSearch,
    PlayYoutubeVideo,
    ShutdownSystem,
    StartOfflineMusic,
    StopOfflineMusic,
    # StopProgram,
    TellAJoke,
    TellTime,
    WikiSearch,
    DefaultCommand
)


class RasaInterpreterException(Exception):
    pass


class RasaInterpreter(Interpreter):
    RASA_NLU_SERVER_BASE_URL = "http://localhost:5005/"
    RASA_NLU_PARSE_URL = f"{RASA_NLU_SERVER_BASE_URL}model/parse"
    HEADERS = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    logger = logging.getLogger(__name__)

    @staticmethod
    def map_intent_to_event(intent):
        event = DefaultCommand.__name__
        if intent == "define_word":
            event = DefineWord.__name__
        elif intent == "play_music":
            event = StartOfflineMusic.__name__
        elif intent == "stop_music":
            event = StopOfflineMusic.__name__
        elif intent == "tell_time":
            event = TellTime.__name__
        elif intent == "tell_joke":
            event = TellAJoke.__name__
        elif intent == "read_news":
            event = GetNews.__name__
        elif intent == "weather_forecast":
            event = GetWeatherForecast.__name__
        elif intent == "shutdown_system":
            event = ShutdownSystem.__name__
        elif intent == "youtube_search":
            event = PlayYoutubeVideo.__name__
        elif intent == "wiki_search":
            event = WikiSearch.__name__
        elif intent == "google_search":
            event = GoogleSearch.__name__

        return event

    @staticmethod
    def extract_entity(response_js):
        entity_indices = list()
        entities = response_js["entities"]
        entity_phrase = None

        if len(entities) > 0:
            for entity in entities:
                entity_indices.append(entity["start"])
                entity_indices.append(entity["end"])

            entity_phrase = response_js["text"][min(entity_indices): max(entity_indices)]

        return entity_phrase

    @staticmethod
    def process_iot_cmd(cmd):
        # Detect for IOT commands 1st
        if cmd == "switch_on_lights":
            event = "lights"
            data = "1"  
        elif cmd == "switch_off_lights":
            event = "lights"
            data = "0"

        return event, data

    @staticmethod
    def is_iot_cmd(cmd):
        return cmd in IOTClient.ALLOWED_COMMANDS

    @classmethod
    def process(cls, command):
        if command == Interpreter.FAILED_TOKEN:
            cls.logger.warning("Failed to interpret command. Reverting to default command")
            return DefaultCommand.__name__, None
        try:
            response = requests.post(cls.RASA_NLU_PARSE_URL,
                                     json={"text": command},
                                     headers=cls.HEADERS,
                                     timeout=0.7)
            cls.logger.info("Rasa Server responded")
        except Timeout:
            cls.logger.warning("Rasa Server timeout")
            raise RasaInterpreterException("Server took too long to respond")

        if response.ok:
            js = response.json()
            intent = js["intent"]["name"]
            cls.logger.info(f"Detected intent: {intent}")

            if RasaInterpreter.is_iot_cmd(intent):
                return RasaInterpreter.process_iot_cmd(intent)
            else:
                event = cls.map_intent_to_event(intent)
                data = cls.extract_entity(js)

                cls.logger.info(f"Event, data: {event}, {data}")
                return event, data

        else:
            raise RasaInterpreterException(f"Response status code: {response.status_code} ({response.reason})")
