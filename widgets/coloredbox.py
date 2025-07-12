# coloredbox.py

from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle


class ColoredBox(BoxLayout):
    def __init__(self, inner_widget, color=(0.3, 0.5, 0.7, 1), **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'  # optional, or inherit inner_widget's orientation
        self.padding = 5

        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self._update_rect, size=self._update_rect)
        self.add_widget(inner_widget)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
