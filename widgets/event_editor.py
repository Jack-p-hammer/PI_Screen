from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from datetime import datetime, timedelta

class EventEditor:
    def __init__(self, calendar_widget):
        self.calendar_widget = calendar_widget
        
    def show_add_event_popup(self):
        """Show popup for adding new events"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(text="Add New Event", size_hint_y=None, height=40)
        content.add_widget(title)
        
        # Event title
        title_label = Label(text="Event Title:", size_hint_y=None, height=30)
        content.add_widget(title_label)
        
        title_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=40
        )
        content.add_widget(title_input)
        
        # Date selection
        date_label = Label(text="Date:", size_hint_y=None, height=30)
        content.add_widget(date_label)
        
        # Create date options (today + next 7 days)
        date_options = []
        for i in range(8):
            date = datetime.now() + timedelta(days=i)
            date_options.append(date.strftime('%Y-%m-%d'))
        
        date_spinner = Spinner(
            text=date_options[0],
            values=date_options,
            size_hint_y=None,
            height=40
        )
        content.add_widget(date_spinner)
        
        # Time selection
        time_label = Label(text="Time:", size_hint_y=None, height=30)
        content.add_widget(time_label)
        
        time_options = [
            "9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM",
            "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM",
            "5:00 PM", "6:00 PM", "7:00 PM", "8:00 PM"
        ]
        
        time_spinner = Spinner(
            text=time_options[0],
            values=time_options,
            size_hint_y=None,
            height=40
        )
        content.add_widget(time_spinner)
        
        # Description
        desc_label = Label(text="Description:", size_hint_y=None, height=30)
        content.add_widget(desc_label)
        
        desc_input = TextInput(
            multiline=True,
            size_hint_y=None,
            height=60
        )
        content.add_widget(desc_input)
        
        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        add_btn = Button(text="Add Event")
        add_btn.bind(on_press=lambda x: self._add_event(
            popup, title_input.text, date_spinner.text, 
            time_spinner.text, desc_input.text
        ))
        
        cancel_btn = Button(text="Cancel")
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        
        button_layout.add_widget(add_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        # Create popup
        popup = Popup(
            title="Add Event",
            content=content,
            size_hint=(0.8, 0.8)
        )
        popup.open()
    
    def _add_event(self, popup, title, date, time, description):
        """Add event to calendar"""
        if title.strip():
            self.calendar_widget.add_event(title, date, time, description)
            popup.dismiss()
        else:
            # Show error for empty title
            error_popup = Popup(
                title="Error",
                content=Label(text="Event title cannot be empty"),
                size_hint=(0.6, 0.3)
            )
            error_popup.open()
    
    def show_event_list_popup(self):
        """Show popup for managing existing events"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(text="Manage Events", size_hint_y=None, height=40)
        content.add_widget(title)
        
        # Event list
        events = self.calendar_widget.events
        if not events:
            no_events = Label(text="No events found", size_hint_y=None, height=40)
            content.add_widget(no_events)
        else:
            # Show events with delete buttons
            for event in events[:10]:  # Limit to 10 events
                event_layout = BoxLayout(size_hint_y=None, height=60)
                
                event_text = f"{event['title']} - {event['date']} {event['time']}"
                event_label = Label(text=event_text, size_hint_x=0.7)
                event_layout.add_widget(event_label)
                
                delete_btn = Button(
                    text="Delete",
                    size_hint_x=0.3,
                    background_color=(1, 0, 0, 1)
                )
                delete_btn.bind(on_press=lambda btn, e=event: self._delete_event(popup, e))
                event_layout.add_widget(delete_btn)
                
                content.add_widget(event_layout)
        
        # Close button
        close_btn = Button(text="Close", size_hint_y=None, height=50)
        close_btn.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(close_btn)
        
        # Create popup
        popup = Popup(
            title="Manage Events",
            content=content,
            size_hint=(0.8, 0.8)
        )
        popup.open()
    
    def _delete_event(self, popup, event):
        """Delete event from calendar"""
        self.calendar_widget.remove_event(event['title'], event['date'])
        popup.dismiss()
        # Refresh the event list
        self.show_event_list_popup() 