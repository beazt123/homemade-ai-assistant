import logging
import newspaper
import random
from collections import defaultdict

from .select_config import SelectConfig
from .speechMixin import SpeechMixin
from ..utils.article_builder import ArticleBuilder


class News(SelectConfig, SpeechMixin):
    def __init__(self, config, speechEngine):
        SpeechMixin.__init__(self, config, speechEngine)
        self.config = self.getConfig(config)
        self.newsRecord = defaultdict(lambda : set())
        self.articleBuilder = ArticleBuilder()

    def getConfig(self, config):
        localConfig = dict()
        localConfig["news_website"] = config.get("NEWS", "news_website")
        return localConfig

    def lazyLoadStatus(self):
        if self.newsRecord["newspaper"] == set():
            logging.info("Lazy loading newspaper articles")
            self.newsRecord["newspaper"] = newspaper.build(self.config["news_website"])
            return True
        if len(self.newsRecord["newspaper"].articles) == 0:
            logging.error("Could not load the newspaper articles")
            self.say("The online news website may have blocked my request. So I'm unable to query for the latest news")
            self.newsRecord["newspaper"] = set()
            return False

    def getNews(self, numArticles):
        if not self.lazyLoadStatus():
            return

        newNews = [article for article in self.newsRecord["newspaper"].articles if article.url not in self.newsRecord["readBefore"]]

        try:
            selectedNews = random.sample(newNews, numArticles)
        except ValueError:
            selectedNews = newNews
            if len(selectedNews) == 0:
                self.say("I have no more news for today")
                return			

        self.say(f"No problem. Bringing you {len(selectedNews)} new articles from today")

        for article in selectedNews:
            article.download()
            logging.debug("Downloaded article")
            article.parse()
            logging.debug("Parsed article")
            article.nlp()
            logging.debug("NLP article")

            if len(article.authors) > 0:
                authors = article.authors
                authors = ', '.join(authors)
            else:
                authors = "UNKNOWN"

            self.articleBuilder.title(f"Title : {article.title}")
            self.articleBuilder.content(f"by {authors}")
            self.articleBuilder.startSection()
            self.articleBuilder.content("Summary :")
            self.articleBuilder.content(article.summary)
            self.articleBuilder.content(f"SOURCE: {article.url}")

            if len(article.movies) > 0:
                self.articleBuilder.content(f"Video links: {article.movies}")

            self.articleBuilder.endSection()
            self.newsRecord["readBefore"].add(article.url)

        for section in self.articleBuilder.getArticleSections():
            for content in section:
                print(content, end="")
                self.say(content)

        self.say("That's all for now. Ping me again if you wanna hear more news of the day")

