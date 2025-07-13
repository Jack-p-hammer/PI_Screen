from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
import json
import os

class ConfigManager:
    def __init__(self, dashboard):
        self.dashboard = dashboard
        self.config_file = "dashboard_config.json"
        self.config = self._load_config()
        
    def _load_config(self):
        """Load configuration from JSON file"""
        default_config = {
            "widgets": [
                {"type": "weather", "position": 0, "enabled": True, "color": [0.2, 0.4, 0.6, 1]},
                {"type": "system_monitor", "position": 1, "enabled": True, "color": [0.3, 0.6, 0.3, 1]},
                {"type": "quote", "position": 2, "enabled": True, "color": [0.6, 0.5, 0.8, 1]},
                {"type": "finance", "position": 3, "enabled": True, "color": [0.2, 0.3, 0.4, 1]},
                {"type": "news", "position": 4, "enabled": False, "color": [0.6, 0.3, 0.3, 1]},
                {"type": "calendar", "position": 5, "enabled": False, "color": [0.3, 0.3, 0.6, 1]}
            ],
            "settings": {
                "update_interval": 60,
                "fullscreen": True,
                "auto_start": True
            }
        }
        
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                self._save_config(default_config)
                return default_config
        except Exception as e:
            print(f"Error loading config: {e}")
            return default_config
    
    def _save_config(self, config):
        """Save configuration to JSON file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def show_config_popup(self):
        """Show configuration popup for touch-based management"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(text="Dashboard Configuration", size_hint_y=None, height=40)
        content.add_widget(title)
        
        # Layout description
        layout_desc = Label(
            text="Layout: Clock (left) + 2x2 Grid (right)\nPositions: 0=Top-Left, 1=Top-Right, 2=Bottom-Left, 3=Bottom-Right",
            size_hint_y=None, height=60, font_size='12sp'
        )
        content.add_widget(layout_desc)
        
        # Widget configuration grid
        widget_grid = GridLayout(cols=4, spacing=5, size_hint_y=None)
        widget_grid.bind(minimum_height=widget_grid.setter('height'))
        
        # Headers
        headers = ["Widget", "Position", "Enabled", "Color"]
        for header in headers:
            widget_grid.add_widget(Label(text=header, size_hint_y=None, height=30))
        
        # Widget rows
        for i, widget_config in enumerate(self.config["widgets"]):
            # Widget name
            name_label = Label(text=widget_config["type"].replace("_", " ").title(), 
                             size_hint_y=None, height=40)
            widget_grid.add_widget(name_label)
            
            # Position spinner (0-3 for 2x2 grid)
            pos_spinner = Spinner(
                text=str(widget_config["position"]),
                values=[str(j) for j in range(4)],  # Only 4 positions (0-3)
                size_hint_y=None, height=40
            )
            pos_spinner.bind(text=lambda spinner, value, idx=i: self._update_widget_position(idx, int(value)))
            widget_grid.add_widget(pos_spinner)
            
            # Enable/disable button
            enabled_btn = Button(
                text="✓" if widget_config["enabled"] else "✗",
                size_hint_y=None, height=40,
                background_color=(0, 1, 0, 1) if widget_config["enabled"] else (1, 0, 0, 1)
            )
            enabled_btn.bind(on_press=lambda btn, idx=i: self._toggle_widget(idx, btn))
            widget_grid.add_widget(enabled_btn)
            
            # Color preview
            color_btn = Button(
                text="🎨",
                size_hint_y=None, height=40,
                background_color=tuple(widget_config["color"])
            )
            color_btn.bind(on_press=lambda btn, idx=i: self._change_color(idx))
            widget_grid.add_widget(color_btn)
        
        content.add_widget(widget_grid)
        
        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        apply_btn = Button(text="Apply Changes")
        apply_btn.bind(on_press=lambda x: self._apply_changes(popup))
        
        cancel_btn = Button(text="Cancel")
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        
        button_layout.add_widget(apply_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        # Create popup
        popup = Popup(
            title="Configure Dashboard",
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()
    
    def _update_widget_position(self, widget_idx, new_position):
        """Update widget position in configuration"""
        self.config["widgets"][widget_idx]["position"] = new_position
    
    def _toggle_widget(self, widget_idx, button):
        """Toggle widget enabled/disabled state"""
        current_state = self.config["widgets"][widget_idx]["enabled"]
        self.config["widgets"][widget_idx]["enabled"] = not current_state
        
        # Update button appearance
        button.text = "✓" if not current_state else "✗"
        button.background_color = (0, 1, 0, 1) if not current_state else (1, 0, 0, 1)
    
    def _change_color(self, widget_idx):
        """Change widget color (placeholder for now)"""
        # For now, just cycle through some predefined colors
        colors = [
            [0.2, 0.4, 0.6, 1],  # Blue
            [0.3, 0.6, 0.3, 1],  # Green
            [0.6, 0.5, 0.8, 1],  # Purple
            [0.2, 0.3, 0.4, 1],  # Dark Blue
            [0.6, 0.3, 0.3, 1],  # Red
            [0.3, 0.3, 0.6, 1],  # Dark Purple
        ]
        
        current_color = self.config["widgets"][widget_idx]["color"]
        try:
            current_index = colors.index(current_color)
            new_index = (current_index + 1) % len(colors)
        except ValueError:
            new_index = 0
        
        self.config["widgets"][widget_idx]["color"] = colors[new_index]
        # Note: Button color will update on next config reload
    
    def _apply_changes(self, popup):
        """Apply configuration changes and rebuild dashboard"""
        self._save_config(self.config)
        self.dashboard.rebuild_from_config()
        popup.dismiss()
    
    def get_enabled_widgets(self):
        """Get list of enabled widgets with their positions"""
        return [w for w in self.config["widgets"] if w["enabled"]]
    
    def get_widget_config(self, widget_type):
        """Get configuration for specific widget type"""
        for widget in self.config["widgets"]:
            if widget["type"] == widget_type:
                return widget
        return None 