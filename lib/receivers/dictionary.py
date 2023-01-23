from __future__ import annotations

from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from configparser import ConfigParser
    from lib.runtime_context.engines import SpeechEngine

from lib.runtime_context.config import Config
import json
import logging
import os
import re

from PyDictionary import PyDictionary
from lib.commands.defineWord import DefineWord

from lib.receivers.receiver import Receiver

from lib.utils.article_builder import ArticleBuilder


class Dictionary(Receiver):
    logger = logging.getLogger(__name__)
    SPLIT_TOKEN = "<split-token>"

    def __init__(self):

        self._onlineEngDict = PyDictionary()
        self.articleBuilder = ArticleBuilder()
        self.speech_engine: SpeechEngine = None
        self._offlineEngDict: dict = None

    def set_config(self, context: Config):
        self.configure(context.static_config)
        self.speech_engine = context.runtime_context.speech_engine

    @property
    def commands(self):
        return DefineWord,

    @property
    def user_guide(self) -> Iterable[str]:
        return (
            "Gives you the dictionary definition of a single word.",
            "I.e. 'Define apprehensive'"
        )

    @property
    def short_description(self) -> str:
        return "DEFINE a word in the dictionary:"

    def configure(self, config: ConfigParser):
        path_to_dict = os.path.join(config.get("RESOURCES", "PARENT_FOLDER_NAME"),
                                    config.get("DICTIONARY", "FOLDER_NAME"),
                                    config.get("DICTIONARY", "FILE_NAME"))
        self.__class__.logger.debug("Fetched path to dict from file: %s", path_to_dict)

        with open(path_to_dict, "r") as f:
            self._offlineEngDict = json.load(f)

    def define(self, look_up_word: str):
        data = look_up_word.split()[0]
        self.__class__.logger.info(f"Lookup word: {data}")
        onlineSearchResult = self._onlineEngDict.meaning(data)
        self.articleBuilder.title(data)

        if onlineSearchResult == None:
            self.__class__.logger.warning(
                "Not found in online dictionary/internet connection down. Reverting to offline dictionary")
            offlineSearchResult = self._offlineEngDict.get(data, None)

            if offlineSearchResult == None:
                Dictionary.logger.warning("Word not found in offline and online dictionary")
                print(f"Sorry, '{look_up_word}' not found in dictionary")
                self.speech_engine.say("Your England very the powderful. Too powderful for me to find")
                return

            self.__class__.logger.debug(f"Offline Search Result: {offlineSearchResult}")
            offlineSearchResult = re.sub("[0-9].", self.__class__.SPLIT_TOKEN, offlineSearchResult)
            cleansedOfflineSearchResult = [sentence.strip() for sentence in
                                           offlineSearchResult.split(self.__class__.SPLIT_TOKEN) if sentence != ""]
            self.__class__.logger.info(f"Cleansed OfflineSearchResult: {cleansedOfflineSearchResult}")

            for sentence in cleansedOfflineSearchResult:
                self.articleBuilder.content(sentence)
                Dictionary.logger.debug(f"Added: {sentence}")

        else:
            self.__class__.logger.info(f"Word found in online search: {onlineSearchResult}")
            self.articleBuilder.startSection()
            for category, meanings in onlineSearchResult.items():
                self.articleBuilder.subtitle(f"{category}:")

                counter = 0
                self.articleBuilder.startSection(bullet="-")
                for meaning in meanings:
                    self.articleBuilder.content(meaning)

                    if counter > 5:
                        break
                self.articleBuilder.endSection()

            self.articleBuilder.endSection()

        self.__class__.logger.info(self.articleBuilder.getArticleInSections())

        for section in self.articleBuilder.getArticleInSections():
            for content in section:
                print(content, end="")
                script = content.replace("\n", " ")
                self.speech_engine.say(script)

        self.articleBuilder.clear()
