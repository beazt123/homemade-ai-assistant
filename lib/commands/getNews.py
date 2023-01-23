from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from lib.receivers.news import News
from .command import Command

class GetNews(Command):
    def __init__(self, news: News) -> None:
        self.receiver = news

    def __call__(self, numArticles):
        if not numArticles:
            numArticles = 5
        return self.receiver.get_news(numArticles)
        