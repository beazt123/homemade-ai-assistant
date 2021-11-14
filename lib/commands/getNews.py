from .command import Command

class GetNews(Command):
    def __init__(self, news) -> None:
        self.receiver = news

    def __call__(self, numArticles):
        if not numArticles:
            numArticles = 5
        return self.receiver.getNews(numArticles)
        