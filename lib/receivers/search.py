from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from lib.receivers.receiver import Receiver
from lib.runtime_context.engines.web_browser import WebBrowser

if TYPE_CHECKING:
    from requests import Session
    from lib.runtime_context.engines import SpeechEngine
    from lib.runtime_context.mixins.async_std_voice_responses import AsyncStdVoiceResponses
from lib.runtime_context.config import Config
import logging
import textwrap
import wikipedia
from requests.exceptions import ConnectionError
from lib.commands.googleSearch import GoogleSearch
from lib.commands.playYoutubeVid import PlayYoutubeVideo
from lib.commands.wikiSearch import WikiSearch


class Searcher(Receiver):
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.speech_engine: SpeechEngine = None
        self.async_std_voice_responses: AsyncStdVoiceResponses = None
        self.session: Session = None
        self.browser: WebBrowser = None

    def set_config(self, context: Config):
        self.speech_engine = context.runtime_context.speech_engine
        self.async_std_voice_responses = context.runtime_context.async_std_voice_responses
        self.session = context.runtime_context.session
        self.browser = context.runtime_context.browser

    def play_on_youtube(self, topic: str):
        """Play a YouTube Video"""

        url = "https://www.youtube.com/results?q=" + topic
        count = 0
        cont = self.session.get(url)
        data = cont.content
        data = str(data)
        lst = data.split('"')
        for i in lst:
            count += 1
            if i == "WEB_PAGE_TYPE_WATCH":
                break
            if lst[count - 5] == "/results":
                raise Exception("No Video Found for this Topic!")

        self.browser.open("https://www.youtube.com" + lst[count - 5])

    @property
    def short_description(self) -> str:
        return "Search on GOOGLE/YOUTUBE/WIKI:"

    @property
    def user_guide(self) -> Iterable[str]:
        return (
            "Performs a search on your browser for Google & Youtube.",
            "Wiki searches will show here with audio response.",
            "I.e. 'google recommended reed diffuser', 'youtube bloodstream ed sheeran', 'wiki Donald Trump'"
        )

    @property
    def commands(self):
        return GoogleSearch, PlayYoutubeVideo, WikiSearch

    def google(self, search_statement: str):
        self.async_std_voice_responses.acknowledge()
        link = "https://www.google.com/search?q={}".format(search_statement)
        self.__class__.logger.info("Google searching for %s", search_statement)
        self.browser.open(link)

    def youtube(self, search_statement: str):
        self.async_std_voice_responses.acknowledge()
        self.play_on_youtube(search_statement)
        self.__class__.logger.info("Youtube searching for %s", search_statement)

    def wiki(self, search_statement: str):
        self.async_std_voice_responses.acknowledge()
        self.__class__.logger.info("Wiki searching for %s", search_statement)

        try:
            info: str = wikipedia.summary(search_statement, 2)
            self.__class__.logger.info("Wiki search results: %s", info)
            paragraphed = textwrap.fill(info.strip(), width=80)
            print(textwrap.indent(paragraphed, prefix="\t"))
            self.speech_engine.say(info)

        except wikipedia.DisambiguationError:
            self.__class__.logger.exception("Wikipedia DisambiguationError: >1 possible searches")
            self.speech_engine.say("Sorry, there were quite many possible searches. \
				Please be more specific in your search terms")

        except wikipedia.exceptions.PageError:
            self.__class__.logger.exception("%s not found on wikipedia", search_statement)
            self.speech_engine.say(f"Sorry, there are no matching searches for {search_statement}")

        except ConnectionError:
            self.__class__.logger.exception(f"Unable to connect to wikipedia")
            self.async_std_voice_responses.apologise(True)
            self.async_std_voice_responses.try_later()
