from datetime import datetime, timedelta
import logging
import requests
import textwrap
from pytz import timezone

from .select_config import SelectConfig
from .speechMixin import SpeechMixin
from ..utils.article_builder import ArticleBuilder


class Weather(SelectConfig, SpeechMixin):
    title = "Weather Forecast"

    def __init__(self, config, speechEngine):
        SpeechMixin.__init__(self, config, speechEngine)
        self.config = self.getConfig(config)
        self.timezone = timezone(self.config["TIMEZONE"])
        self.articleBuilder = ArticleBuilder()

    def getConfig(self, config):
        localConfig = dict()
        localConfig["BASE_URL"] = config.get("WEATHER", "WEATHER_API_BASE_URL")
        localConfig["URL_PARAMS"] = {
			'lat': config.getfloat("LOCATION", "LAT"), 
			'lon': config.getfloat("LOCATION", "LON"), 
			"appid": config.get("WEATHER", "API_KEY"),
			"units": config.get("WEATHER", "UNITS", fallback="metric"),
			}
        localConfig["TIMEZONE"] = config.get("LOCATION", "TIMEZONE")
        return localConfig

    def weather(self):
        r = requests.get(self.config["BASE_URL"], 
                        params = self.config["URL_PARAMS"])

        if r.status_code == 200:
            data = r.json()
            hourlyWeather = data['hourly']
            now = self.timezone.localize(datetime.now())
            
            self.articleBuilder.title(self.title)
            for hoursLater in range(0, 13, 3):
                later = now + timedelta(hours=hoursLater)
                laterWeather = list(filter(lambda x : x["dt"] > later.timestamp(), hourlyWeather))[0]
                formattedTimeLater = later.strftime('%I:%M %p')

                self.articleBuilder.content(f"At {formattedTimeLater}")
                self.articleBuilder.startSection()

                apparentTemperature = round(laterWeather["feels_like"], 1)
                desc = laterWeather["weather"][0]["description"].title()
                humidity = laterWeather['humidity']
                logging.debug(f"apparentTemperature: {apparentTemperature}")          

                announcementScript = [
                f'{desc}',
                f"Apparent temperature at {apparentTemperature} degrees Celsius",
                f"Humidity at {humidity} percent"				
                ]
                announcementPrintStmt = list(map(lambda s : s.replace("Celsius", "C").replace(" degrees", "").replace("percent", "%").replace(" at", ":"), announcementScript))

                self.articleBuilder.content(announcementPrintStmt[0])
                self.articleBuilder.content(announcementPrintStmt[1])
                self.articleBuilder.content(announcementPrintStmt[2])
                self.articleBuilder.endSection()
                self.articleBuilder.br()

                logging.debug(f"announcementPrintStmt: {announcementPrintStmt}")

            for section in self.articleBuilder.getArticleSections():
                for content in section:
                    print(content, end="")
                    self.say(content)

            self.articleBuilder.clear()

        elif r.status_code == 401:
            self.say("No authentication provided. I couldn't log in to the weather server.")
        else:
            self.say("Why don't stick your head out the window?")
