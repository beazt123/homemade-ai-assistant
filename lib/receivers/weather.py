from datetime import datetime, timedelta
import logging
import requests
from pytz import timezone

from .select_config import SelectConfig
from .mixins.speechMixin import SpeechMixin
from ..utils.article_builder import ArticleBuilder

logger = logging.getLogger(__name__)

class Weather(SelectConfig, SpeechMixin):
    title = "Weather Forecast"

    def __init__(self, config, speechEngine = None):
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
		
        logger.info(f"Weather query status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            hourlyWeather = data['hourly']
            now = self.timezone.localize(datetime.now())
			
            logger.debug(f"len(response.json): {len(hourlyWeather)}")
            logger.debug(f"Time of query: {now.strftime('%I:%M %p')}")
            
            self.articleBuilder.title(Weather.title)
            for hoursLater in range(0, 13, 3):
                later = now + timedelta(hours=hoursLater)
                laterWeather = list(filter(lambda x : x["dt"] > later.timestamp(), hourlyWeather))[0]
                formattedTimeLater = later.strftime('%I:%M %p')

                self.articleBuilder.content(f"At {formattedTimeLater}")
                self.articleBuilder.startSection()

                apparentTemperature = round(laterWeather["feels_like"], 1)
                desc = laterWeather["weather"][0]["description"].title()
                humidity = laterWeather['humidity']
                logger.debug(f"apparentTemperature: {apparentTemperature}")          

                announcementScript = [
					f'{desc}',
					f"Apparent temperature at {apparentTemperature} degrees Celsius",
					f"Humidity at {humidity} percent"				
                ]
                logger.debug(f"Weather announcement script: {announcementScript}")
                announcementPrintStmt = list(map(lambda s : s.replace("Celsius", "C").replace(" degrees", "").replace("percent", "%").replace(" at", ":"), announcementScript))
				
                logger.debug(f"Weather announcement script: {announcementPrintStmt}")

                self.articleBuilder.content(announcementPrintStmt[0])
                self.articleBuilder.content(announcementPrintStmt[1])
                self.articleBuilder.content(announcementPrintStmt[2])
                self.articleBuilder.endSection()
                self.articleBuilder.br()

                

            for section in self.articleBuilder.getArticleInSections():
                for content in section:
                    print(content, end="")
                    logger.info(content)
                    self.say(content)

            self.articleBuilder.clear()

        elif r.status_code == 401:
            logger.error("Could not fetch weather info")
            self.say("No authentication provided. I couldn't log in to the weather server.")
        else:
            logger.error("Unknown error")
            self.say("Why don't stick your head out the window?")
