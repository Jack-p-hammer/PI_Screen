from kivy.uix.label import Label
from datetime import datetime

class ClockWidget:
    def render(self, parent):
        self.label = Label(text=self.get_time(), font_size='40sp')
        parent.add_widget(self.label)

    def update(self):
        self.label.text = self.get_time()

    def get_time(self):
        return datetime.now().strftime('%I:%M:%S %p')
        # return datetime.now().strftime('%H:%M:%S')  -> 24-hour format
