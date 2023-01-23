from __future__ import annotations

from typing import TYPE_CHECKING, Iterable


if TYPE_CHECKING:
    from configparser import ConfigParser
    from lib.runtime_context.mixins.async_std_voice_responses import AsyncStdVoiceResponses
    from lib.runtime_context.engines import SpeechEngine

from lib.runtime_context.config import Config
import logging
import newspaper
import random
import re
from collections import defaultdict
from lib.commands.getNews import GetNews

from lib.receivers.receiver import Receiver

from lib.utils.article_builder import ArticleBuilder


class News(Receiver):
    logger = logging.getLogger(__name__)
    URL_REGEX = r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])'

    def __init__(self):
        self.news_website = None
        self.news_record = defaultdict(lambda: set())
        self.articleBuilder = ArticleBuilder()
        self.speech_engine: SpeechEngine = None
        self.async_std_voice_responses: AsyncStdVoiceResponses = None

    def set_config(self, context: Config):
        self.configure(context.static_config)
        self.speech_engine = context.runtime_context.speech_engine
        self.async_std_voice_responses = context.runtime_context.async_std_voice_responses

    @property
    def short_description(self) -> str:
        return "LOCAL NEWS:"

    @property
    def user_guide(self) -> Iterable[str]:
        return (
            "Brings you summaries of the top 5 articles from a specified news site",
            "I.e. 'New flash'"
        )

    @property
    def commands(self):
        return GetNews,

    def configure(self, config: ConfigParser):
        self.news_website = config.get("NEWS", "news_website")
        self.__class__.logger.debug("Loaded selected news website from config: %s", self.news_website)

    def lazy_load_status(self):
        if self.news_record["newspaper"] == set():
            self.__class__.logger.info("Lazy loading newspaper articles")
            self.async_std_voice_responses.acknowledge()
            self.news_record["newspaper"] = newspaper.build(self.news_website)

            if len(self.news_record["newspaper"].articles) == 0:
                self.__class__.logger.error("Could not load the newspaper articles")
                self.async_std_voice_responses.apologise(block=True)
                self.speech_engine.say(
                    "The online news website may have blocked my request. So I can't query for the latest news")
                self.async_std_voice_responses.try_later()
                self.news_record["newspaper"] = set()
                return False

        return True

    def get_news(self, num_articles: int):
        if not self.lazy_load_status():
            return

        new_news = [article for article in self.news_record["newspaper"].articles if
                    article not in self.news_record["readBefore"]]
        self.__class__.logger.info(f"Number of new news: {len(new_news)}")

        try:
            selected_news = random.sample(new_news, num_articles)
        except ValueError:
            self.__class__.logger.warning("Insufficient news")
            selected_news = new_news
            if len(selected_news) == 0:
                self.__class__.logger.warning("No more news")
                self.speech_engine.say("I have no more news for today")
                return

        self.speech_engine.say(f"Bringing you {len(selected_news)} new articles from today")

        for article in selected_news:
            article.download()
            self.__class__.logger.debug(f"Downloaded: {article.url}")
            article.parse()
            self.__class__.logger.debug(f"Parsed :{article.url}")
            article.nlp()
            self.__class__.logger.debug(f"NLP: {article.url}")

            if len(article.authors) > 0:
                authors = article.authors
                authors = ', '.join(authors)
            else:
                authors = "UNKNOWN"

            self.articleBuilder.title(f"Title : {article.title}")
            self.articleBuilder.content(f"by {authors}")
            self.articleBuilder.startSection()
            self.articleBuilder.content("Summary :")
            self.articleBuilder.startSection()
            self.articleBuilder.content(article.summary)
            self.articleBuilder.endSection()
            self.articleBuilder.content("SOURCE:")
            self.articleBuilder.startSection()
            self.articleBuilder.content(article.url)
            self.articleBuilder.endSection()

            if len(article.movies) > 0:
                self.articleBuilder.content(f"Video links: {article.movies}")

            self.articleBuilder.endSection()
            self.articleBuilder.br()
            self.news_record["readBefore"].add(article)

        self.__class__.logger.debug(self.news_record["readBefore"])

        for section in self.articleBuilder.getArticleInSections():
            for content in section:
                self.__class__.logger.debug(f"Showing user: {content}")
                print(content, end="")

                if re.search(self.__class__.URL_REGEX, content):
                    self.__class__.logger.debug(f"Detected a URL in: {content}")
                    continue

                script = content.replace("\n", " ")
                self.speech_engine.say(script)

        self.articleBuilder.clear()

        self.speech_engine.say("That's all for now. Ping me again if you wanna hear more")
