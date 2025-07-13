from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import openmeteo_requests
import requests_cache
from retry_requests import retry

# Setup Open-Meteo API client
cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
openmeteo = openmeteo_requests.Client(session=retry_session)

url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 42.36,  # Boston
    "longitude": -71.06,
    "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "wind_speed_10m", "precipitation"]
}

class WeatherWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.label = Label(text="Loading weather...", font_size='14sp')
        self.add_widget(self.label)

    def render(self, parent):
        parent.add_widget(self)
        self.update()

    def update(self):
        print("WeatherWidget.update called")
        try:
            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]
            current = response.Current()

            temp = current.Variables(0).Value()*9/5+32
            humidity = current.Variables(1).Value()
            apparent_temp = current.Variables(2).Value()
            wind_speed = current.Variables(3).Value()
            precipitation = current.Variables(4).Value()

            self.label.text = f'{temp:.1f}°F and {humidity}% humidity'

        except Exception as e:
            print("Weather update failed:", e)
            self.label.text = f"Error: {e}"
