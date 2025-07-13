# widgets/financewidget.py

import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from kivy.uix.boxlayout import BoxLayout
from kivy_garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.label import Label
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import io
from kivy.core.image import Image as CoreImage
from kivy.uix.image import Image
import numpy as np
import time


class FinanceWidget(BoxLayout):
    def __init__(self, symbol="QQQ", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.symbol = symbol
        self.label = Label(text=f"{self.symbol} — Loading...", font_size="12sp")
        self.add_widget(self.label)
        
        # Create image widget for chart
        self.chart_image = Image(size_hint=(1, 0.7))
        self.add_widget(self.chart_image)
        
        # Cache for finance data
        self.last_update = 0
        self.cached_data = None
        self.cached_chart = None
        self.update_interval = 120  # 2 minutes
        self.first_update = True  # Flag for first update
        self.last_chart_update = 0  # Track chart updates separately

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
            # Download stock data with explicit auto_adjust parameter
            data = yf.download(self.symbol, period="7d", interval="1h", progress=False, auto_adjust=True)
            
            if data.empty:
                self.label.text = f"{self.symbol} — No data"
                return
            
            # Get latest price using iloc[-1] to avoid deprecation warning
            latest_price = float(data['Close'].iloc[-1])
            self.label.text = f"{self.symbol} — ${latest_price:.2f}"
            
            # Cache the data
            self.cached_data = {
                'price': latest_price,
                'data': data
            }
            self.last_update = current_time
            
            # Create chart on first update or every 5 minutes
            if self.first_update or current_time - self.last_chart_update > 300:
                self._create_chart(data)
                self.last_chart_update = current_time
            
            print(f"[FinanceWidget] Updated {self.symbol} with {len(data)} points")
            
        except Exception as e:
            print(f"Finance update failed: {e}")
            # Use cached data if available
            if self.cached_data:
                self.label.text = f"{self.symbol} — ${self.cached_data['price']:.2f}"
            else:
                self.label.text = f"{self.symbol} — Error"

    def _create_chart(self, data):
        """Create a simple price chart"""
        try:
            # Close any existing figures to prevent memory issues
            plt.close('all')
            
            # Set style for cleaner look
            plt.style.use('default')
            
            # Create figure with better proportions
            fig, ax = plt.subplots(figsize=(4, 2.5), dpi=100, facecolor='white')
            
            # Ensure price_change is a float
            close_series = data['Close']
            first_price = float(close_series.iloc[0])
            last_price = float(close_series.iloc[-1])
            price_change = last_price - first_price
            line_color = 'green' if price_change >= 0 else 'red'
            
            # Plot closing prices with better styling
            ax.plot(data.index, close_series.values, linewidth=2, color=line_color, alpha=0.8)
            
            # Add subtle grid
            ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
            
            # Format title and labels
            ax.set_title(f'{self.symbol} 7-Day', fontsize=10, fontweight='bold', pad=10)
            ax.set_ylabel('Price ($)', fontsize=8, fontweight='bold')
            
            # Format axis ticks
            ax.tick_params(axis='both', which='major', labelsize=7)
            ax.tick_params(axis='x', rotation=45)
            
            # Format y-axis to show currency
            def currency_formatter(x, pos):
                return f'${x:.0f}'
            ax.yaxis.set_major_formatter(FuncFormatter(currency_formatter))
            
            # Remove top and right spines for cleaner look
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_alpha(0.7)
            ax.spines['bottom'].set_alpha(0.7)
            
            # Add subtle background color
            ax.set_facecolor('#f8f9fa')
            
            # Tight layout to prevent label cutoff
            plt.tight_layout(pad=1.0)
            
            # Convert to image
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight', dpi=100, 
                       facecolor='white', edgecolor='none')
            buf.seek(0)
            
            # Create Kivy image
            image = CoreImage(buf, ext='png')
            self.chart_image.texture = image.texture
            
            # Close figure to free memory
            plt.close(fig)
            buf.close()
            
            print(f"[FinanceWidget] Chart created for {self.symbol}")
            
        except Exception as e:
            print(f"Chart creation failed: {e}")
            # If chart fails, just show text
            self.chart_image.source = ""
