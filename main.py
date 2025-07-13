# kivy_dashboard_main.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.config import Config

Config.set('graphics', 'fullscreen', 'auto')  # or '1' for always fullscreen
Config.set('graphics', 'resizable', False)    # Optional: make window fixed-size

from widgets.weather import WeatherWidget
from widgets.clock import ClockWidget
from widgets.coloredbox import ColoredBox  # ← import the wrapper
from widgets.quote import QuoteWidget
from widgets.finance import FinanceWidget
from widgets.system_monitor import SystemMonitorWidget
from widgets.news import NewsWidget
from widgets.calendar_widget import CalendarWidget
from widgets.config_manager import ConfigManager

class Dashboard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        
        # Initialize configuration manager
        self.config_manager = ConfigManager(self)
        
        # LEFT SIDE: big clock
        self.clock_widget = ClockWidget()
        self.clock_container = BoxLayout(size_hint=(0.5, 1))
        self.clock_widget.render(self.clock_container)

        # RIGHT SIDE: 2x2 grid of widgets with colored backgrounds
        self.grid_container = GridLayout(cols=2, rows=2, spacing=5, padding=5, size_hint=(0.5, 1))
        self.grid_widgets = []
        
        # Add configuration button (small, in corner)
        self.config_button = Button(
            text="⚙",
            size_hint=(None, None),
            size=(50, 50),
            pos_hint={'right': 1, 'top': 1},
            background_color=(0.3, 0.3, 0.3, 0.8)
        )
        self.config_button.bind(on_press=self.show_config)
        
        # Build dashboard from configuration
        self.build_from_config()
        
        self.add_widget(self.clock_container)
        self.add_widget(self.grid_container)
        self.add_widget(self.config_button)

        # Optimized update scheduling
        self.setup_update_schedule()
        
        # Trigger immediate updates for all widgets
        self.trigger_initial_updates()

    def setup_update_schedule(self):
        """Setup different update intervals for different widgets"""
        # Clock updates every second
        Clock.schedule_interval(self.update_clock, 1)
        
        # Weather updates every 5 minutes (300 seconds)
        Clock.schedule_interval(self.update_weather, 300)
        
        # Finance updates every 2 minutes (120 seconds)
        Clock.schedule_interval(self.update_finance, 120)
        
        # System monitor updates every 10 seconds
        Clock.schedule_interval(self.update_system, 10)
        
        # News updates every 10 minutes (600 seconds)
        Clock.schedule_interval(self.update_news, 600)
        
        # Calendar updates every 5 minutes
        Clock.schedule_interval(self.update_calendar, 300)
        
        # Quote updates every 30 minutes (1800 seconds)
        Clock.schedule_interval(self.update_quote, 1800)

    def trigger_initial_updates(self):
        """Trigger immediate updates for all widgets on startup"""
        print("🚀 Triggering initial widget updates...")
        
        # Update clock immediately
        self.clock_widget.update()
        
        # Update all grid widgets immediately
        for widget in self.grid_widgets:
            if hasattr(widget, 'update'):
                # Force update by resetting last_update time
                if hasattr(widget, 'last_update'):
                    widget.last_update = 0
                widget.update()

    def update_clock(self, dt):
        """Update clock widget"""
        self.clock_widget.update()

    def update_weather(self, dt):
        """Update weather widgets"""
        for widget in self.grid_widgets:
            if isinstance(widget, WeatherWidget):
                widget.update()

    def update_finance(self, dt):
        """Update finance widgets"""
        for widget in self.grid_widgets:
            if isinstance(widget, FinanceWidget):
                widget.update()

    def update_system(self, dt):
        """Update system monitor widgets"""
        for widget in self.grid_widgets:
            if isinstance(widget, SystemMonitorWidget):
                widget.update()

    def update_news(self, dt):
        """Update news widgets"""
        for widget in self.grid_widgets:
            if isinstance(widget, NewsWidget):
                widget.update()

    def update_calendar(self, dt):
        """Update calendar widgets"""
        for widget in self.grid_widgets:
            if isinstance(widget, CalendarWidget):
                widget.update()

    def update_quote(self, dt):
        """Update quote widgets"""
        for widget in self.grid_widgets:
            if isinstance(widget, QuoteWidget):
                widget.update()

    def build_from_config(self):
        """Build dashboard based on configuration"""
        # Clear existing widgets
        self.grid_container.clear_widgets()
        self.grid_widgets = []
        
        # Get enabled widgets from config
        enabled_widgets = self.config_manager.get_enabled_widgets()
        
        # Sort by position
        enabled_widgets.sort(key=lambda x: x['position'])
        
        # Create widgets for the first 4 positions
        for i in range(4):
            if i < len(enabled_widgets):
                widget_config = enabled_widgets[i]
                widget = self._create_widget(widget_config['type'])
                if widget:
                    widget.size_hint = (1, 1)
                    
                    # Wrap in colored box
                    color = tuple(widget_config['color'])
                    wrapped = ColoredBox(widget, color=color)
                    wrapped.size_hint = (1, 1)
                    
                    self.grid_container.add_widget(wrapped)
                    self.grid_widgets.append(widget)
            else:
                # Add placeholder for empty slots
                placeholder = BoxLayout()
                placeholder.size_hint = (1, 1)
                self.grid_container.add_widget(placeholder)

    def _create_widget(self, widget_type):
        """Create widget based on type"""
        widget_creators = {
            'weather': lambda: WeatherWidget(),
            'quote': lambda: QuoteWidget(),
            'finance': lambda: FinanceWidget("QQQ"),
            'system_monitor': lambda: SystemMonitorWidget(),
            'news': lambda: NewsWidget(),
            'calendar': lambda: CalendarWidget()
        }
        
        creator = widget_creators.get(widget_type)
        if creator:
            return creator()
        return None

    def rebuild_from_config(self):
        """Rebuild dashboard from configuration"""
        self.build_from_config()
        # Trigger immediate updates after rebuild
        self.trigger_initial_updates()

    def show_config(self, instance):
        """Show configuration popup"""
        self.config_manager.show_config_popup()

class DashboardApp(App):
    def build(self):
        return Dashboard()

if __name__ == '__main__':
    DashboardApp().run()
