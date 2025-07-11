# kivy_dashboard_main.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from widgets.weather import WeatherWidget
from widgets.clock import ClockWidget

class Dashboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.widgets = [ClockWidget(), WeatherWidget(), ClockWidget()]

        for widget in self.widgets:
            widget.render(self)

        Clock.schedule_interval(self.update_widgets, 60)

    def update_widgets(self, dt):
        for widget in self.widgets:
            widget.update()

class DashboardApp(App):
    def build(self):
        return Dashboard()

if __name__ == '__main__':
    DashboardApp().run()