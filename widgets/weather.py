from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import openmeteo_requests
import requests_cache
from retry_requests import retry
import time

# Setup Open-Meteo API client with longer cache
cache_session = requests_cache.CachedSession('.cache', expire_after=1800)  # 30 minutes cache
retry_session = retry(cache_session, retries=3, backoff_factor=0.2)
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
        
        # Cache for weather data
        self.last_update = 0
        self.cached_data = None
        self.update_interval = 300  # 5 minutes
        self.first_update = True  # Flag for first update

    def render(self, parent):
        parent.add_widget(self)
        self.update()

    def update(self):
        current_time = time.time()
        
        # Skip cache check on first update or if forced
        if self.first_update:
            self.first_update = False
            self.last_update = 0  # Force update
        
        # Only update if enough time has passed
        if current_time - self.last_update < self.update_interval and self.cached_data and not self.first_update:
            return
        
        try:
            responses = openmeteo.weather_api(url, params=params)
            response = responses[0]
            current = response.Current()

            temp = current.Variables(0).Value()*9/5+32
            humidity = current.Variables(1).Value()
            apparent_temp = current.Variables(2).Value()
            wind_speed = current.Variables(3).Value()
            precipitation = current.Variables(4).Value()

            # Cache the data
            self.cached_data = {
                'temp': temp,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'precipitation': precipitation
            }
            self.last_update = current_time

            self.label.text = f'{temp:.1f}°F and {humidity}% humidity'

        except Exception as e:
            print("Weather update failed:", e)
            # Use cached data if available
            if self.cached_data:
                self.label.text = f'{self.cached_data["temp"]:.1f}°F and {self.cached_data["humidity"]}% humidity'
            else:
                self.label.text = f"Error: {e}"
