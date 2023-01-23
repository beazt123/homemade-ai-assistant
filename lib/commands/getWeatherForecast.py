from __future__ import annotations
import typing

if typing.TYPE_CHECKING:
    from lib.receivers.weather import Weather
    
from .command import Command

class GetWeatherForecast(Command):
    def __init__(self, weather: Weather) -> None:
        self.receiver = weather

    def __call__(self, arg):
        return self.receiver.weather()
        