# widgets/financewidget.py

import yfinance as yf
import matplotlib.pyplot as plt
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.label import Label


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
                print(f"[FinanceWidget] No data for {self.symbol}")
                self.label.text = f"No data for {self.symbol}"
                return

            closes = data["Close"]
            # Clear existing children (labels + plots)
            self.clear_widgets()

            # Add updated label
            latest_price = closes.iloc[-1]
            self.label = Label(text=f"{self.symbol} — ${float(latest_price):.2f}", font_size="12sp")
            self.add_widget(self.label)

            # Plot
            fig, ax = plt.subplots(figsize=(4, 2), dpi=100)
            ax.plot(closes.index, closes.values, label=self.symbol, linewidth=2)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_facecolor('#f9f9f9')
            ax.grid(True, linestyle='--', linewidth=0.5)
            fig.tight_layout()

            # Add plot canvas
            canvas = FigureCanvasKivyAgg(fig)
            self.add_widget(canvas)

            print(f"[FinanceWidget] Updated {self.symbol} with {len(closes)} points")

        except Exception as e:
            print(f"[FinanceWidget] Error: {e}")
            self.clear_widgets()
            self.label = Label(text=f"Error: {e}", font_size="12sp")
            self.add_widget(self.label)
