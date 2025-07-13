from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import requests
import json
from datetime import datetime
import time

class NewsWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 5
        self.spacing = 2
        
        # Create scrollable news container
        self.news_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.news_container.bind(minimum_height=self.news_container.setter('height'))
        
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.scroll_view.add_widget(self.news_container)
        self.add_widget(self.scroll_view)
        
        # Add title
        self.title_label = Label(text="Latest News", font_size='14sp', size_hint_y=None, height=25)
        self.add_widget(self.title_label)
        
        # News API key (you'll need to get a free key from newsapi.org)
        self.api_key = "YOUR_NEWS_API_KEY"  # Replace with your API key
        self.news_items = []
        
        # Cache for news data
        self.last_update = 0
        self.cached_data = None
        self.update_interval = 600  # 10 minutes
        self.first_update = True  # Flag for first update

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
            # Use a free news API (you can replace with your preferred source)
            # For demo purposes, we'll use a simple RSS-like approach
            self._fetch_news()
        except Exception as e:
            print(f"News update failed: {e}")
            self._show_error(f"Error: {e}")

    def _fetch_news(self):
        """Fetch news from a free API"""
        try:
            # Using a free news API - you can replace with your preferred source
            # For now, we'll create some sample news items
            sample_news = [
                "Tech: Raspberry Pi 5 now available with improved performance",
                "Weather: Sunny skies expected for the weekend",
                "Local: Community garden project receives funding",
                "Sports: Local team wins championship game",
                "Science: New AI developments in machine learning"
            ]
            
            # Cache the data
            self.cached_data = sample_news
            self.last_update = time.time()
            
            self._display_news(sample_news)
            
        except Exception as e:
            print(f"News fetch failed: {e}")
            self._show_error("Unable to fetch news")

    def _display_news(self, news_items):
        """Display news items in the widget"""
        # Clear existing news
        self.news_container.clear_widgets()
        
        for i, news in enumerate(news_items[:5]):  # Show max 5 items
            # Create news item label
            news_label = Label(
                text=f"{i+1}. {news}",
                font_size='10sp',
                size_hint_y=None,
                height=30,
                text_size=(None, None),
                halign='left',
                valign='middle'
            )
            self.news_container.add_widget(news_label)

    def _show_error(self, error_msg):
        """Show error message in widget"""
        self.news_container.clear_widgets()
        error_label = Label(
            text=error_msg,
            font_size='10sp',
            size_hint_y=None,
            height=30
        )
        self.news_container.add_widget(error_label)

    def _fetch_with_api_key(self):
        """Alternative method using NewsAPI.org (requires API key)"""
        if self.api_key == "YOUR_NEWS_API_KEY":
            return
            
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "country": "us",
            "apiKey": self.api_key,
            "pageSize": 5
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                news_items = [article.get('title', 'No title') for article in articles]
                self._display_news(news_items)
            else:
                self._show_error("News API error")
        except Exception as e:
            self._show_error(f"API Error: {e}") 