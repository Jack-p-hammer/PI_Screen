# widgets/quotewidget.py

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from random import choice
from kivy.clock import Clock

class QuoteWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10

        self.label = Label(
            text="Loading quote...",
            font_size='12sp',
            halign='center',
            valign='middle'
        )
        self.label.bind(size=self._update_text_size)
        self.add_widget(self.label)

        # List of quotes (can expand later or fetch remotely)
        self.quotes = [
            "The best way out is always through. — Robert Frost",
            "Make it work, then make it better. — Unknown",
            "Fall seven times, stand up eight. — Japanese Proverb",
            "In the middle of difficulty lies opportunity. — Einstein",
            "Don’t watch the clock; do what it does. Keep going. — Sam Levenson",
            "If you're going through hell, keep going. — Winston Churchill",
            "Strive not to be a success, but rather to be of value. — Einstein"
        ]


        self.update_counter = 9

    def _update_text_size(self, instance, size):
        self.label.text_size = size

    def render(self, parent):
        parent.add_widget(self)
        self.update()

    def update(self):
        self.update_counter += 1
        if self.update_counter % 10 == 0:
            new_quote = choice(self.quotes)
            self.label.text = new_quote
        else:
            pass  # No update needed, just keep the current quote
