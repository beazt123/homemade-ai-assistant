import logging
import newspaper
import random
import textwrap
from collections import defaultdict

from .select_config import SelectConfig
from .speechMixin import SpeechMixin


class News(SelectConfig, SpeechMixin):
    def __init__(self, config, speechEngine):
        SpeechMixin.__init__(self, speechEngine)
        self.config = self.getConfig(config)
        self.newsRecord = defaultdict(lambda : set())

    def getConfig(self, config):
        localConfig = dict()
        localConfig["news_website"] = config.get("NEWS", "news_website")
        return localConfig

    def getNews(self, numArticles):
        if self.newsRecord["newspaper"] == set():
            logging.info("Lazy loading newspaper articles")
            self.newsRecord["newspaper"] = newspaper.build(self.config["news_website"])
        if len(self.newsRecord["newspaper"].articles) == 0:
            logging.error("Could not load the newspaper articles")
            self.say("The online news website may have blocked my request. So I'm unable to query for the latest news")
            self.newsRecord["newspaper"] = set()
            return

        newNews = [article for article in self.newsRecord["newspaper"].articles if article.url not in self.newsRecord["readBefore"]]

        try:
            selectedNews = random.sample(newNews, numArticles)
        except ValueError:
            selectedNews = newNews
            if len(selectedNews) == 0:
                self.say("I have no more news for today")
                return			

        self.say(f"No problem. Bringing you {len(selectedNews)} articles")

        for article in selectedNews:
            article.download()
            logging.debug("Downloaded article")
            article.parse()
            logging.debug("Parsed article")
            article.nlp()
            logging.debug("NLP article")

            title = f"Title : {article.title}"
            print(title)
            print("=" * len(title))

            if len(article.authors) > 0:
                authors = article.authors
                authors = ', '.join(authors)
            else:
                authors = "UNKNOWN"
                print(f"Authors: {authors}\n")

            self.say(article.title)
            # print(f"Summary : {article.summary}\n")
            print(self.formatForPPrint(article.summary, indent="\t"))

            self.say(article.summary)
            print(f"\nSource: {article.url}\n")

            if len(article.movies) > 0:
                print(f"Video links: {article.movies}\n")


            self.newsRecord["readBefore"].add(article.url)

        self.say("That's all for now. Ping me again if you wanna hear more news of the day")

