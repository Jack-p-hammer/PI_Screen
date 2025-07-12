# widgets/financewidget.py

import yfinance as yf
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.label import Label
import matplotlib.pyplot as plt

class FinanceWidget(BoxLayout):
    def __init__(self, symbol="SPY", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.symbol = symbol

        self.label = Label(text=f"Loading {symbol}...", font_size="12sp")
        self.add_widget(self.label)

    def render(self, parent):
        parent.add_widget(self)
        self.update()

    def update(self):
        try:
            data = yf.download(self.symbol, period="7d", interval="1h", progress=False)

            if data.empty:
                self.label.text = f"No data for {self.symbol}"
                return

            closes = data["Close"]
            times = closes.index

            # Clear existing widgets (to avoid stacking plots)
            self.clear_widgets()

            # Re-add label
            self.label = Label(text=f"{self.symbol} — ${closes[-1]:.2f}", font_size="12sp")
            self.add_widget(self.label)

            # Create plot
            fig, ax = plt.subplots(figsize=(4, 2), dpi=100)
            ax.plot(closes.values, label=self.symbol)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title("")
            ax.grid(True)
            fig.tight_layout()

            self.add_widget(FigureCanvasKivyAgg(fig))

        except Exception as e:
            self.label.text = f"Error: {e}"
