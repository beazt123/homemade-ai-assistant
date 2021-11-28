import logging
import newspaper
import random
import re
from collections import defaultdict

from .select_config import SelectConfig
from .speechMixin import SpeechMixin
from .asyncStdVoiceResponseMixin import AsyncStdVoiceResponseMixin
from ..utils.article_builder import ArticleBuilder

logger = logging.getLogger(__name__)

class News(SelectConfig, SpeechMixin, AsyncStdVoiceResponseMixin):
    URL_REGEX = r'(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])'

    def __init__(self, 
                config, 
                speechEngine = None,
                soundEngine = None):
        SpeechMixin.__init__(self, config, speechEngine)
        AsyncStdVoiceResponseMixin.__init__(self, config, soundEngine)
        self.config = self.getConfig(config)
        self.newsRecord = defaultdict(lambda : set())
        self.articleBuilder = ArticleBuilder()

    def getConfig(self, config):
        localConfig = dict()
        localConfig["news_website"] = config.get("NEWS", "news_website")
        logger.debug(f"Loaded selected news website from config: {localConfig['news_website']}")
        return localConfig

    def lazyLoadStatus(self):
        if self.newsRecord["newspaper"] == set():
            logger.info("Lazy loading newspaper articles")
            self.acknowledge()
            self.newsRecord["newspaper"] = newspaper.build(self.config["news_website"])

            if len(self.newsRecord["newspaper"].articles) == 0:
                logger.error("Could not load the newspaper articles")
                self.apologise(block=True)
                self.say("The online news website may have blocked my request. So I can't query for the latest news")
                self.tryLater()
                self.newsRecord["newspaper"] = set()
                return False

        return True

    def getNews(self, numArticles):
        if not self.lazyLoadStatus():
            return

        newNews = [article for article in self.newsRecord["newspaper"].articles if article.url not in self.newsRecord["readBefore"]]
        logger.info(f"Number of new news: {len(newNews)}")
        # TODO: filter not working for articles already read. Maybe don't check the URL

        try:
            selectedNews = random.sample(newNews, numArticles)
        except ValueError:
            selectedNews = newNews
            if len(selectedNews) == 0:
                self.say("I have no more news for today")
                return			

        self.say(f"Bringing you {len(selectedNews)} new articles from today")

        for article in selectedNews:
            article.download()
            logger.debug(f"Downloaded: {article.url}")
            article.parse()
            logger.debug(f"Parsed :{article.url}")
            article.nlp()
            logger.debug(f"NLP: {article.url}")
            
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
            self.newsRecord["readBefore"].add(article.url)

        for section in self.articleBuilder.getArticleInSections():
            for content in section:
                logger.debug(f"Showing user: {content}")
                print(content, end="")
                
                if re.search(News.URL_REGEX, content):
                    logger.debug(f"Detected a URL in: {content}")
                    continue
                
                script = content.replace("\n", " ")
                self.say(script)

        self.say("That's all for now. Ping me again if you wanna hear more")

