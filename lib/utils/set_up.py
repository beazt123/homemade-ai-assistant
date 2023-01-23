import logging
from typing import Iterable, List, Type
from speech_recognition import Microphone as computerMic

from lib.interpreters import Interpreter
from lib.dispatchers.invokers.remote_invoker_proxy import RemoteInvokerProxy
from lib.dispatchers.iot.IOTClient import IOTClient
from lib.runtime_context.engines import GttsSpeechEngine

from lib.runtime_context.engines.PyttsxSpeechEngine import PyttsxSpeechEngine
from lib.runtime_context.engines.speech_engine import SpeechEngine
from lib.receivers.receiver import Receiver
from lib.runtime_context.config import Config

from .article_builder import ArticleBuilder
from ..dispatchers.iot.MQTTClient import MQTTClient
from .WakeWordDetector import WakeWordDetector
from ..interpreters import RasaInterpreter, RegexInterpreter, MasterInterpreter
from ..dispatchers.dispatcher import Dispatcher
from ..dispatchers.invokers.invoker import InvokerImpl
from lib.runtime_context.engines.sound_engine import SoundEngine
from .. import receivers
from .. import commands

logger = logging.getLogger(__name__)


class App:
    def __init__(self,
                 wake_word_detector=None,
                 interpreter=None,
                 dispatcher=None):
        self.wakeWordDetector = wake_word_detector
        self.interpreter = interpreter
        self.dispatcher = dispatcher
        self.main = None

    def run(self):
        if self.main:
            self.main(self.wakeWordDetector,
                      self.interpreter,
                      self.dispatcher)
        else:
            raise ValueError("Main attribute of app object must be set before app.run() can be called.")


def set_up_iot_client(config, iot_topics, logger) -> IOTClient:
    iot_client = None
    client_type = config.get("IOT", "TYPE")
    logger.info(f"Retrieved client type: {client_type}")
    logger.info(f"Topics to subscribe to: {iot_topics}")
    if client_type.lower() == "mqtt":
        iot_client = MQTTClient(iot_topics, config.get("MQTT", "IP_ADDR"))
        logger.info(f"Created {MQTTClient.__name__}: {iot_client}")
        logger.info(f"{iot_client} subscribed to {iot_topics}")
    else:
        raise ValueError("No IOT client setting provided in system configuration")
    return iot_client


def create_help_msg(wake_word_detector: WakeWordDetector, receivers: Iterable[Receiver]):
    user_guide_builder = ArticleBuilder()
    user_guide_builder.title("A.I general assistant")
    user_guide_builder.subtitle("Wake words")
    user_guide_builder.startSection()
    user_guide_builder.content(f"Please say any 1 of the following words to wake me up:")
    user_guide_builder.startSection()
    user_guide_builder.content(', '.join(wake_word_detector.wake_words))
    user_guide_builder.endSection()
    user_guide_builder.br()

    user_guide_builder.endSection()
    user_guide_builder.subtitle("What I can do:")
    user_guide_builder.startSection()

    for receiver in receivers:
        logger.info("Adding user guide for %s", receiver.__class__.__name__)
        user_guide_builder.subtitle(receiver.short_description)
        user_guide_builder.startSection()
        for line in receiver.user_guide:
            user_guide_builder.content(line)
        user_guide_builder.endSection()
        user_guide_builder.br(2)
    user_guide_builder.endSection()

    return user_guide_builder.getArticleInPlainText()


def run_as_standalone(
        wake_word_detector: WakeWordDetector,
        interpreter: Interpreter,
        dispatcher: Dispatcher,
        receivers: List[Receiver]):
    print(create_help_msg(wake_word_detector, receivers))
    # interpreter.switch_on_sound()

    while True:
        try:
            # interpreter.adjust_for_ambient_noise()
            print("\nReady")
            wake_word_detector.waitForWakeWord()
            meta_command = interpreter.interpret()
            dispatcher.dispatch(meta_command)
        except KeyboardInterrupt:
            break


def run_as_slave(wake_word_detector, interpreter, dispatcher):
    dispatcher.standBy()


class AppFactory:
    @staticmethod
    def determine_speech_engine_class(set_up_config: dict) -> Type[SpeechEngine]:
        if set_up_config["tts"].lower() == "pyttsx3":
            speech_engine_class = PyttsxSpeechEngine
        elif set_up_config["tts"].lower() == "gtts":
            speech_engine_class = GttsSpeechEngine
        else:
            speech_engine_class = PyttsxSpeechEngine

        return speech_engine_class

    @staticmethod
    def create_app(config, run_profile) -> App:
        wake_word_detector = None
        interpreter = None
        dispatcher = None
        main = None

        speech_engine_class = AppFactory.determine_speech_engine_class(run_profile)

        app_config = Config(config)
        app_config.runtime_context.speech_engine = speech_engine_class(config)
        app_config.runtime_context.mic = computerMic()

        commands_to_use = list()
        selected_receivers_names: List[str] = run_profile["receivers"]
        selected_receivers: List[Receiver] = []
        for receiver in selected_receivers_names:
            try:
                cls = getattr(receivers, receiver)
                receiver_obj: Receiver = cls()
                receiver_obj.set_config(app_config)
                selected_receivers.append(receiver_obj)
                for command in receiver_obj.commands:
                    commands_to_use.append(command(receiver_obj))
            except AttributeError:
                logger.warning("Receiver not found")

        fallback_receiver_class = getattr(receivers, "FallbackReceiver")
        fallback_receiver: Receiver = fallback_receiver_class()
        fallback_receiver.set_config(app_config)
        logger.info(f"Created {fallback_receiver_class.__name__} ")
        default_command_class = getattr(commands, "DefaultCommand")
        commands_to_use.append(default_command_class(fallback_receiver))

        command_hooks = {command.__class__.__name__: command for command in commands_to_use}
        invoker = InvokerImpl()
        invoker.registerAll(command_hooks)
        logger.info("Added command hooks to invoker")
        iot_topics = run_profile.get("iot_topics")
        if iot_topics:
            iot_client = set_up_iot_client(config, iot_topics, logger)
            remote_invoker = RemoteInvokerProxy(iot_client)
            logger.info("Set up IOT client")
        else:
            remote_invoker = None
        dispatcher = Dispatcher(invoker, remote_invoker)

        if run_profile["type"].lower() == "standalone" or run_profile["type"].lower() == "master":
            chosen_wakewords = run_profile["wakewords"]
            wake_word_detector = WakeWordDetector(config.get("WAKE-WORD-DETECTOR", "ACCESS_KEY"), chosen_wakewords)

            if run_profile["interpreter"].lower() == "rasa":
                selected_interpreter = RasaInterpreter
            elif run_profile["interpreter"].lower() == "regex":
                selected_interpreter = RegexInterpreter
            elif run_profile["interpreter"].lower() == "master":
                selected_interpreter = MasterInterpreter
            else:
                selected_interpreter = RegexInterpreter

            interpreter = selected_interpreter()
            interpreter.set_config(app_config)
            logger.info(f"Created {selected_interpreter.__name__} ")
            main = lambda wake_word_detector, interpreter, dispatcher: run_as_standalone(wake_word_detector,
                                                                                         interpreter,
                                                                                         dispatcher, selected_receivers)

        elif run_profile["type"].lower() == "slave":
            main = run_as_slave

        app = App(wake_word_detector, interpreter, dispatcher)
        app.main = main

        return app
