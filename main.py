# kivy_dashboard_main.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock

from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')  # or '1' for always fullscreen
Config.set('graphics', 'resizable', False)    # Optional: make window fixed-size

from widgets.weather import WeatherWidget
from widgets.clock import ClockWidget
from widgets.coloredbox import ColoredBox  # ← import the wrapper
from widgets.quote import QuoteWidget
from widgets.finance import FinanceWidget

class Dashboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'

        # LEFT SIDE: big clock
        self.clock_widget = ClockWidget()
        self.clock_container = BoxLayout(size_hint=(0.5, 1))
        self.clock_widget.render(self.clock_container)

        # RIGHT SIDE: 2x2 grid of widgets with colored backgrounds
        self.grid_container = GridLayout(cols=2, rows=2, spacing=5, padding=5, size_hint=(0.5, 1))
        self.grid_widgets = []

        for i in range(2):
            widget = WeatherWidget()
            widget.size_hint = (1, 1)

            # Wrap in a colored box — change color here per widget if you want
            color = (0.2 + 0.2*i, 0.4, 0.6, 1)
            wrapped = ColoredBox(widget, color=color)
            wrapped.size_hint = (1, 1)

            self.grid_container.add_widget(wrapped)
            self.grid_widgets.append(widget)

        widget = QuoteWidget()
        widget.size_hint = (1, 1)
        wrapped = ColoredBox(widget, color=(0.6, 0.5, 0.8, 1))
        self.grid_container.add_widget(wrapped)
        self.grid_widgets.append(widget)

        widget = FinanceWidget("QQQ")  # or "QQQ", "SPY", etc.
        widget.size_hint = (1, 1)
        wrapped = ColoredBox(widget, color=(0.2, 0.3, 0.4, 1))
        self.grid_container.add_widget(wrapped)
        self.grid_widgets.append(widget)
        
        self.add_widget(self.clock_container)
        self.add_widget(self.grid_container)




        Clock.schedule_interval(self.update_widgets, 1)

    def update_widgets(self, dt):
        self.clock_widget.update()
        for widget in self.grid_widgets:
            widget.update()

class DashboardApp(App):
    def build(self):
        return Dashboard()

if __name__ == '__main__':
    DashboardApp().run()
