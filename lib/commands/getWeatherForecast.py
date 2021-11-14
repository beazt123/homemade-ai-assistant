from .command import Command

class GetWeatherForecast(Command):
    def __init__(self, weather) -> None:
        self.receiver = weather

    def __call__(self):
        return self.receiver.weather()
        