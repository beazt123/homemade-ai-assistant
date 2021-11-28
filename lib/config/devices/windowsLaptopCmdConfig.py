import logging

from ..config import config
from ...receivers import *
from ...commands import (
    DefineWord,
    # GetNews,
    GetWeatherForecast,
    GoogleSearch,
    PlayYoutubeVideo,
    WikiSearch
)

logger = logging.getLogger(__name__)

englishDictionary = Dictionary(config)
logger.info(f"Created {Dictionary.__name__} ")

# newsCaster = News(config)
# logging.info(f"Created {News.__name__} ")

searcher = Searcher(config)
logger.info(f"Created {Searcher.__name__} ")

weatherForecaster = Weather(config)
logger.info(f"Created {Weather.__name__} ")

commandsToUse = [
    DefineWord(englishDictionary),
    # GetNews(newsCaster),
    GetWeatherForecast(weatherForecaster),
    GoogleSearch(searcher),
    PlayYoutubeVideo(searcher),
    WikiSearch(searcher)
]

commandHooks = {command.__class__.__name__: command for command in commandsToUse}