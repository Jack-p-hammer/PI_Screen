from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from datetime import datetime, timedelta
import json
import os
import time

class CalendarWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 5
        self.spacing = 2
        
        # Create scrollable events container
        self.events_container = BoxLayout(orientation='vertical', size_hint_y=None)
        self.events_container.bind(minimum_height=self.events_container.setter('height'))
        
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.scroll_view.add_widget(self.events_container)
        self.add_widget(self.scroll_view)
        
        # Add title with current date and management buttons
        title_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=25)
        
        self.title_label = Label(text="Calendar", font_size='14sp')
        title_layout.add_widget(self.title_label)
        
        # Add event button
        add_btn = Button(
            text="+",
            size_hint_x=None,
            width=30,
            background_color=(0, 1, 0, 1)
        )
        add_btn.bind(on_press=self._show_add_event)
        title_layout.add_widget(add_btn)
        
        # Manage events button
        manage_btn = Button(
            text="⚙",
            size_hint_x=None,
            width=30,
            background_color=(0.5, 0.5, 0.5, 1)
        )
        manage_btn.bind(on_press=self._show_manage_events)
        title_layout.add_widget(manage_btn)
        
        self.add_widget(title_layout)
        
        # Events file path
        self.events_file = "events.json"
        self.events = self._load_events()
        
        # Import event editor
        from widgets.event_editor import EventEditor
        self.event_editor = EventEditor(self)
        
        # Cache for calendar data
        self.last_update = 0
        self.cached_data = None
        self.update_interval = 300  # 5 minutes
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
            # Update title with current date
            current_date = datetime.now()
            self.title_label.text = f"Calendar - {current_date.strftime('%b %d, %Y')}"
            
            # Display upcoming events
            self._display_events()
            
            # Cache the data
            self.cached_data = {
                'date': current_date,
                'events': self.events
            }
            self.last_update = current_time
            
        except Exception as e:
            print(f"Calendar update failed: {e}")
            self._show_error(f"Error: {e}")

    def _load_events(self):
        """Load events from JSON file"""
        try:
            if os.path.exists(self.events_file):
                with open(self.events_file, 'r') as f:
                    return json.load(f)
            else:
                # Create sample events if file doesn't exist
                sample_events = [
                    {
                        "title": "Team Meeting",
                        "date": (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'),
                        "time": "10:00 AM",
                        "description": "Weekly team sync"
                    },
                    {
                        "title": "Dentist Appointment",
                        "date": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
                        "time": "2:30 PM",
                        "description": "Regular checkup"
                    },
                    {
                        "title": "Birthday Party",
                        "date": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
                        "time": "6:00 PM",
                        "description": "Friend's birthday celebration"
                    }
                ]
                self._save_events(sample_events)
                return sample_events
        except Exception as e:
            print(f"Error loading events: {e}")
            return []

    def _save_events(self, events):
        """Save events to JSON file"""
        try:
            with open(self.events_file, 'w') as f:
                json.dump(events, f, indent=2)
        except Exception as e:
            print(f"Error saving events: {e}")

    def _display_events(self):
        """Display upcoming events"""
        # Clear existing events
        self.events_container.clear_widgets()
        
        current_date = datetime.now()
        upcoming_events = []
        
        # Filter upcoming events (next 7 days)
        for event in self.events:
            try:
                event_date = datetime.strptime(event['date'], '%Y-%m-%d')
                if event_date >= current_date:
                    days_until = (event_date - current_date).days
                    if days_until <= 7:
                        upcoming_events.append((event, days_until))
            except:
                continue
        
        # Sort by date
        upcoming_events.sort(key=lambda x: x[1])
        
        if not upcoming_events:
            no_events_label = Label(
                text="No upcoming events",
                font_size='10sp',
                size_hint_y=None,
                height=30
            )
            self.events_container.add_widget(no_events_label)
        else:
            for event, days_until in upcoming_events[:5]:  # Show max 5 events
                # Create event display
                if days_until == 0:
                    day_text = "Today"
                elif days_until == 1:
                    day_text = "Tomorrow"
                else:
                    day_text = f"In {days_until} days"
                
                event_text = f"{event['title']} - {day_text}\n{event['time']} - {event['description']}"
                
                event_label = Label(
                    text=event_text,
                    font_size='10sp',
                    size_hint_y=None,
                    height=50,
                    text_size=(None, None),
                    halign='left',
                    valign='top'
                )
                self.events_container.add_widget(event_label)

    def _show_error(self, error_msg):
        """Show error message in widget"""
        self.events_container.clear_widgets()
        error_label = Label(
            text=error_msg,
            font_size='10sp',
            size_hint_y=None,
            height=30
        )
        self.events_container.add_widget(error_label)

    def add_event(self, title, date, time, description):
        """Add a new event"""
        new_event = {
            "title": title,
            "date": date,
            "time": time,
            "description": description
        }
        self.events.append(new_event)
        self._save_events(self.events)
        self.update()

    def remove_event(self, title, date):
        """Remove an event"""
        self.events = [e for e in self.events if not (e['title'] == title and e['date'] == date)]
        self._save_events(self.events)
        self.update()
    
    def _show_add_event(self, instance):
        """Show add event popup"""
        self.event_editor.show_add_event_popup()
    
    def _show_manage_events(self, instance):
        """Show manage events popup"""
        self.event_editor.show_event_list_popup() 