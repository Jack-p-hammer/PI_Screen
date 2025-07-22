from kivy.uix.label import Label
from datetime import datetime
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
import math


class AnalogClockFace(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_clock, size=self.update_clock)
        self.time = datetime.now()

    def set_time(self, dt):
        self.time = dt
        self.update_clock()

    def update_clock(self, *args):
        self.canvas.clear()
        cx, cy = self.center
        radius = min(self.width, self.height) * 0.45

        with self.canvas:
            # Draw clock face
            Color(0.95, 0.95, 0.95, 1)
            Ellipse(pos=(cx - radius, cy - radius), size=(2*radius, 2*radius))
            Color(0.2, 0.2, 0.2, 1)
            Line(circle=(cx, cy, radius), width=2)

            # Draw hour marks
            for i in range(12):
                angle = math.radians(i * 30)
                x1 = cx + (radius - 8) * math.sin(angle)
                y1 = cy + (radius - 8) * math.cos(angle)
                x2 = cx + (radius - 20) * math.sin(angle)
                y2 = cy + (radius - 20) * math.cos(angle)
                Line(points=[x1, y1, x2, y2], width=2)

            now = self.time
            hour = now.hour % 12 + now.minute / 60.0
            minute = now.minute + now.second / 60.0
            second = now.second

            # Draw hour hand
            hour_angle = math.radians(90 - (hour * 30))
            hx = cx + (radius * 0.5) * math.cos(hour_angle)
            hy = cy + (radius * 0.5) * math.sin(hour_angle)
            Color(0.1, 0.1, 0.1, 1)
            Line(points=[cx, cy, hx, hy], width=4)

            # Draw minute hand
            min_angle = math.radians(90 - (minute * 6))
            mx = cx + (radius * 0.75) * math.cos(min_angle)
            my = cy + (radius * 0.75) * math.sin(min_angle)
            Color(0.2, 0.2, 0.2, 1)
            Line(points=[cx, cy, mx, my], width=3)

            # Draw second hand
            sec_angle = math.radians(90 - (second * 6))
            sx = cx + (radius * 0.85) * math.cos(sec_angle)
            sy = cy + (radius * 0.85) * math.sin(sec_angle)
            Color(1, 0, 0, 1)
            Line(points=[cx, cy, sx, sy], width=1.5)

            # Draw center dot
            Color(0, 0, 0, 1)
            Ellipse(pos=(cx - 5, cy - 5), size=(10, 10))

class ClockWidget:
    def render(self, parent):
        self.layout = BoxLayout(orientation='vertical', spacing=10)
        self.analog = AnalogClockFace(size_hint=(1, 0.7))
        self.label = Label(text=self.get_time(), font_size='40sp', size_hint=(1, 0.3))
        self.layout.add_widget(self.analog)
        self.layout.add_widget(self.label)
        parent.add_widget(self.layout)

    def update(self):
        now = datetime.now()
        self.label.text = now.strftime('%I:%M:%S %p')
        self.analog.set_time(now)

    def get_time(self):
        return datetime.now().strftime('%I:%M:%S %p')