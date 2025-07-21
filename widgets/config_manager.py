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
            "theme": "Warm Waters",
            "widgets": [
                {"type": "weather", "position": 0, "enabled": True, "color": [0.8, 0.6, 0.4, 1]},
                {"type": "system_monitor", "position": 1, "enabled": True, "color": [0.6, 0.8, 0.9, 1]},
                {"type": "quote", "position": 2, "enabled": True, "color": [0.9, 0.7, 0.5, 1]},
                {"type": "finance", "position": 3, "enabled": True, "color": [0.7, 0.9, 0.8, 1]},
                {"type": "news", "position": 4, "enabled": False, "color": [0.8, 0.6, 0.4, 1]},
                {"type": "calendar", "position": 5, "enabled": False, "color": [0.6, 0.8, 0.9, 1]}
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
        """Show configuration popup with visual layout matching dashboard"""
        content = BoxLayout(orientation='horizontal', padding=10, spacing=10)
        
        # LEFT SIDE: Clock representation
        left_side = BoxLayout(orientation='vertical', size_hint_x=0.5)
        
        # Clock title
        clock_title = Label(
            text="🕐 Clock Widget", 
            size_hint_y=None, height=40,
            font_size='16sp',
            bold=True
        )
        left_side.add_widget(clock_title)
        
        # Clock display area (visual representation)
        clock_display = BoxLayout(
            size_hint_y=0.8
        )
        
        clock_label = Label(
            text="12:34:56\nAM",
            font_size='24sp',
            bold=True,
            color=(1, 1, 1, 1)
        )
        clock_display.add_widget(clock_label)
        left_side.add_widget(clock_display)
        
        # Clock info
        clock_info = Label(
            text="Clock is always active\nand updates every second",
            size_hint_y=None, height=60,
            font_size='12sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        left_side.add_widget(clock_info)
        
        content.add_widget(left_side)
        
        # RIGHT SIDE: 2x2 Grid with dropdowns
        right_side = BoxLayout(orientation='vertical', size_hint_x=0.5)
        
        # Grid title
        grid_title = Label(
            text="📊 Widget Grid (2x2)", 
            size_hint_y=None, height=40,
            font_size='16sp',
            bold=True
        )
        right_side.add_widget(grid_title)
        
        # 2x2 Grid container
        grid_container = GridLayout(cols=2, rows=2, spacing=5, size_hint_y=0.8)
        
        # Available widget types
        widget_types = [
            "weather", "system_monitor", "quote", "finance", 
            "news", "calendar", "none"
        ]
        
        # Create dropdown for each grid position
        for position in range(4):
            # Get current widget in this position
            current_widget = self._get_widget_at_position(position)
            current_type = current_widget["type"] if current_widget else "none"
            
            # Grid cell container
            cell = BoxLayout(orientation='vertical', padding=5)
            
            # Position label
            pos_label = Label(
                text=f"Position {position}",
                size_hint_y=None, height=20,
                font_size='10sp',
                color=(0.8, 0.8, 0.8, 1)
            )
            cell.add_widget(pos_label)
            
            # Widget type dropdown
            widget_spinner = Spinner(
                text=current_type.replace("_", " ").title(),
                values=[wt.replace("_", " ").title() for wt in widget_types],
                size_hint_y=None, height=30,
                font_size='12sp'
            )
            widget_spinner.bind(text=lambda spinner, value, pos=position: 
                              self._update_widget_at_position(pos, value.lower().replace(" ", "_")))
            cell.add_widget(widget_spinner)
            
            # Enable/disable button (if widget is assigned)
            if current_widget:
                enabled_btn = Button(
                    text="✓" if current_widget["enabled"] else "✗",
                    size_hint_y=None, height=25,
                    background_color=(0, 1, 0, 1) if current_widget["enabled"] else (1, 0, 0, 1)
                )
                enabled_btn.bind(on_press=lambda btn, pos=position: self._toggle_widget_at_position(pos, btn))
                cell.add_widget(enabled_btn)
            
            grid_container.add_widget(cell)
        
        right_side.add_widget(grid_container)
        
        # Instructions
        instructions = Label(
            text="Select widget type for each position\nChoose a theme for coordinated colors",
            size_hint_y=None, height=40,
            font_size='10sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        right_side.add_widget(instructions)
        
        # Theme selection
        theme_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
        theme_label = Label(text="Theme:", size_hint_x=0.3)
        theme_layout.add_widget(theme_label)
        
        # Available themes
        themes = {
            "Warm Waters": {
                "name": "Warm Waters",
                "colors": [
                    [0.8, 0.6, 0.4, 1],  # Sandy Beige
                    [0.6, 0.8, 0.9, 1],  # Ocean Blue
                    [0.9, 0.7, 0.5, 1],  # Coral
                    [0.7, 0.9, 0.8, 1],  # Seafoam
                ]
            },
            "Forest Night": {
                "name": "Forest Night",
                "colors": [
                    [0.2, 0.4, 0.3, 1],  # Dark Green
                    [0.3, 0.5, 0.4, 1],  # Forest Green
                    [0.4, 0.3, 0.2, 1],  # Brown
                    [0.2, 0.3, 0.4, 1],  # Dark Blue
                ]
            },
            "Sunset": {
                "name": "Sunset",
                "colors": [
                    [0.8, 0.4, 0.2, 1],  # Orange
                    [0.9, 0.5, 0.3, 1],  # Light Orange
                    [0.7, 0.3, 0.5, 1],  # Purple
                    [0.6, 0.4, 0.2, 1],  # Brown
                ]
            },
            "Classic": {
                "name": "Classic",
                "colors": [
                    [0.2, 0.4, 0.6, 1],  # Blue
                    [0.3, 0.6, 0.3, 1],  # Green
                    [0.6, 0.5, 0.8, 1],  # Purple
                    [0.2, 0.3, 0.4, 1],  # Dark Blue
                ]
            }
        }
        
        # Get current theme
        current_theme = self._get_current_theme()
        theme_names = list(themes.keys())
        
        theme_spinner = Spinner(
            text=current_theme,
            values=theme_names,
            size_hint_x=0.7
        )
        theme_spinner.bind(text=lambda spinner, value: self._update_theme(value, themes))
        theme_layout.add_widget(theme_spinner)
        
        right_side.add_widget(theme_layout)
        
        content.add_widget(right_side)
        
        # Bottom buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        
        apply_btn = Button(text="Apply Changes")
        apply_btn.bind(on_press=lambda x: self._apply_changes(popup))
        
        cancel_btn = Button(text="Cancel")
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        
        button_layout.add_widget(apply_btn)
        button_layout.add_widget(cancel_btn)
        
        # Main container with buttons
        main_container = BoxLayout(orientation='vertical')
        main_container.add_widget(content)
        main_container.add_widget(button_layout)
        
        # Create popup
        popup = Popup(
            title="Dashboard Configuration",
            content=main_container,
            size_hint=(0.95, 0.9)
        )
        popup.open()
    
    def _get_widget_at_position(self, position):
        """Get widget configuration at specific position"""
        for widget in self.config["widgets"]:
            if widget["position"] == position:
                return widget
        return None
    
    def _update_widget_at_position(self, position, widget_type):
        """Update widget type at specific position"""
        # Remove any existing widget at this position
        for widget in self.config["widgets"]:
            if widget["position"] == position:
                if widget_type == "none":
                    widget["enabled"] = False
                else:
                    widget["type"] = widget_type
                    widget["enabled"] = True
                return
        
        # If no widget exists at this position and type is not "none", create new widget
        if widget_type != "none":
            new_widget = {
                "type": widget_type,
                "position": position,
                "enabled": True,
                "color": [0.2, 0.4, 0.6, 1]  # Default blue
            }
            self.config["widgets"].append(new_widget)
    
    def _toggle_widget_at_position(self, position, button):
        """Toggle widget enabled/disabled state at specific position"""
        widget = self._get_widget_at_position(position)
        if widget:
            current_state = widget["enabled"]
            widget["enabled"] = not current_state
            
            # Update button appearance
            button.text = "✓" if not current_state else "✗"
            button.background_color = (0, 1, 0, 1) if not current_state else (1, 0, 0, 1)
    
    def _change_color_at_position(self, position):
        """Change widget color at specific position"""
        widget = self._get_widget_at_position(position)
        if widget:
            # Cycle through predefined colors
            colors = [
                [0.2, 0.4, 0.6, 1],  # Blue
                [0.3, 0.6, 0.3, 1],  # Green
                [0.6, 0.5, 0.8, 1],  # Purple
                [0.2, 0.3, 0.4, 1],  # Dark Blue
                [0.6, 0.3, 0.3, 1],  # Red
                [0.3, 0.3, 0.6, 1],  # Dark Purple
            ]
            
            current_color = widget["color"]
            try:
                current_index = colors.index(current_color)
                new_index = (current_index + 1) % len(colors)
            except ValueError:
                new_index = 0
            
            widget["color"] = colors[new_index]
    
    def _update_widget_color(self, position, color_name, colors, color_names):
        """Update widget color based on color name selection"""
        try:
            color_index = color_names.index(color_name)
            selected_color = colors[color_index]
            
            # Get or create widget at this position
            widget = self._get_widget_at_position(position)
            if widget:
                widget["color"] = selected_color
            else:
                # Create a default widget with this color
                new_widget = {
                    "type": "weather",  # Default widget type
                    "position": position,
                    "enabled": True,
                    "color": selected_color
                }
                self.config["widgets"].append(new_widget)
        except (ValueError, IndexError):
            print(f"Invalid color selection: {color_name}")
    
    def _get_current_theme(self):
        """Get current theme from config"""
        return self.config.get("theme", "Warm Waters")
    
    def _update_theme(self, theme_name, themes):
        """Update theme and apply colors to all widgets"""
        if theme_name not in themes:
            return
        
        theme = themes[theme_name]
        self.config["theme"] = theme_name
        
        # Apply theme colors to widgets in positions 0-3
        for position in range(4):
            if position < len(theme["colors"]):
                color = theme["colors"][position]
                
                # Find or create widget at this position
                widget = self._get_widget_at_position(position)
                if widget:
                    widget["color"] = color
                else:
                    # Create a default widget with this color
                    new_widget = {
                        "type": "weather",  # Default widget type
                        "position": position,
                        "enabled": True,
                        "color": color
                    }
                    self.config["widgets"].append(new_widget)
    
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