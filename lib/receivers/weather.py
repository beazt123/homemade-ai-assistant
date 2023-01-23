from __future__ import annotations
from typing import TYPE_CHECKING, Iterable

from lib.receivers.receiver import Receiver

if TYPE_CHECKING:
    from lib.runtime_context.engines import SpeechEngine
from lib.runtime_context.config import Config
from datetime import datetime, timedelta
import logging
import requests
from pytz import timezone
from lib.commands.getWeatherForecast import GetWeatherForecast

from lib.utils.article_builder import ArticleBuilder


class Weather(Receiver):
    logger = logging.getLogger(__name__)

    title = "Weather Forecast"

    def __init__(self):
        self.config: dict = None
        self.timezone: timezone = None
        self.speech_engine: SpeechEngine = None
        self.articleBuilder = ArticleBuilder()

    def set_config(self, context: Config):
        self.configure(context.static_config)
        self.timezone = timezone(self.config["TIMEZONE"])
        self.speech_engine = context.runtime_context.speech_engine

    @property
    def short_description(self) -> str:
        return "WEATHER forecast:"

    @property
    def user_guide(self) -> Iterable[str]:
        return (
            "Gives you the next 12 hr weather forecast in 3-hr blocks.",
            "I.e. 'Weather forecast'"
        )

    @property
    def commands(self):
        return GetWeatherForecast,

    def configure(self, config):
        local_config = dict()
        local_config["BASE_URL"] = config.get("WEATHER", "WEATHER_API_BASE_URL")
        local_config["URL_PARAMS"] = {
            'lat': config.getfloat("LOCATION", "LAT", fallback=0),
            'lon': config.getfloat("LOCATION", "LON", fallback=0),
            "appid": config.get("WEATHER", "API_KEY", fallback=""),
            "units": config.get("WEATHER", "UNITS", fallback="metric"),
        }
        local_config["TIMEZONE"] = config.get("LOCATION", "TIMEZONE", fallback="Asia/Singapore")
        self.config = local_config

    def weather(self):
        r = requests.get(self.config["BASE_URL"],
                         params=self.config["URL_PARAMS"])

        self.__class__.logger.info(f"Weather query status: {r.status_code}")
        if r.ok:
            data = r.json()
            hourly_weather = data['hourly']
            now = self.timezone.localize(datetime.now())

            self.__class__.logger.debug(f"len(response.json): {len(hourly_weather)}")
            self.__class__.logger.debug(f"Time of query: {now.strftime('%I:%M %p')}")

            self.articleBuilder.title(self.__class__.title)
            for hoursLater in range(0, 13, 3):
                later = now + timedelta(hours=hoursLater)
                later_weather = list(filter(lambda x: x["dt"] > later.timestamp(), hourly_weather))[0]
                formatted_time_later = later.strftime('%I:%M %p')

                self.articleBuilder.content(f"At {formatted_time_later}")
                self.articleBuilder.startSection()

                apparent_temperature = round(later_weather["feels_like"], 1)
                desc = later_weather["weather"][0]["description"].title()
                humidity = later_weather['humidity']
                self.__class__.logger.debug(f"apparent_temperature: {apparent_temperature}")

                announcement_script = [
                    f'{desc}',
                    f"Apparent temperature at {apparent_temperature} degrees Celsius",
                    f"Humidity at {humidity} percent"
                ]
                self.__class__.logger.debug(f"Weather announcement script: {announcement_script}")
                announcement_print_stmt = tuple(
                    map(lambda s: s.replace("Celsius", "C").replace(" degrees", "").replace("percent", "%").replace(
                        " at", ":"), announcement_script))

                self.__class__.logger.debug(f"Weather announcement script: {announcement_print_stmt}")

                self.articleBuilder.content(announcement_print_stmt[0])
                self.articleBuilder.content(announcement_print_stmt[1])
                self.articleBuilder.content(announcement_print_stmt[2])
                self.articleBuilder.endSection()
                self.articleBuilder.br()

            for section in self.articleBuilder.getArticleInSections():
                for content in section:
                    print(content, end="")
                    self.__class__.logger.info(content)
                    self.speech_engine.say(content)

            self.articleBuilder.clear()

        elif r.status_code == 401:
            self.__class__.logger.error("Could not fetch weather info")
            self.speech_engine.say("No authentication provided. I couldn't log in to the weather server.")
        else:
            self.__class__.logger.error("Unknown error")
            self.speech_engine.say("Why don't stick your head out the window?")
