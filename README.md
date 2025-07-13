# Raspberry Pi Dashboard

A beautiful, touch-enabled dashboard built with Kivy for Raspberry Pi displays. Features real-time widgets, touch-based configuration, and a modular design.

## Features

### Core Widgets
- **Clock Widget**: Large, prominent time display
- **Weather Widget**: Real-time weather information using Open-Meteo API
- **Quote Widget**: Daily inspirational quotes
- **Finance Widget**: Stock market data (QQQ, SPY, etc.)
- **System Monitor Widget**: CPU, memory, disk usage, and temperature
- **News Widget**: Latest news headlines
- **Calendar Widget**: Event management with touch interface

### Touch-Based Configuration
- **Widget Management**: Enable/disable widgets via touch interface
- **Layout Customization**: Rearrange widget positions
- **Color Themes**: Customize widget background colors
- **Event Management**: Add/edit/delete calendar events with touch interface

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **For Raspberry Pi** (additional setup):
   ```bash
   sudo apt-get update
   sudo apt-get install python3-kivy
   sudo apt-get install python3-psutil
   ```

## Usage

### Basic Usage
```bash
python main.py
```

### Touch Configuration
1. Tap the gear icon (⚙) in the top-right corner
2. Use the configuration popup to:
   - Enable/disable widgets
   - Change widget positions
   - Apply changes

### Calendar Event Management
1. Tap the "+" button in the calendar widget to add events
2. Tap the "⚙" button to manage existing events
3. Use the touch interface to set date, time, and description

## Widget Configuration

### System Monitor
- Displays CPU usage, memory usage, disk usage
- Shows Raspberry Pi temperature
- Updates every 5 seconds

### Weather Widget
- Uses Open-Meteo API (free, no API key required)
- Shows temperature and humidity
- Configure location in `widgets/weather.py`

### Finance Widget
- Displays stock data using yfinance
- Default: QQQ (NASDAQ-100 ETF)
- Change symbol in main.py or via configuration

### News Widget
- Sample news items (can be configured with NewsAPI.org)
- To use real news API:
  1. Get free API key from [newsapi.org](https://newsapi.org)
  2. Update `api_key` in `widgets/news.py`

## Configuration Files

### dashboard_config.json
Stores widget configuration:
```json
{
  "widgets": [
    {"type": "weather", "position": 0, "enabled": true, "color": [0.2, 0.4, 0.6, 1]},
    {"type": "system_monitor", "position": 1, "enabled": false, "color": [0.3, 0.6, 0.3, 1]}
  ],
  "settings": {
    "update_interval": 60,
    "fullscreen": true
  }
}
```

### events.json
Stores calendar events:
```json
[
  {
    "title": "Team Meeting",
    "date": "2024-01-15",
    "time": "10:00 AM",
    "description": "Weekly team sync"
  }
]
```

## Customization

### Adding New Widgets
1. Create new widget class in `widgets/` directory
2. Implement `render()` and `update()` methods
3. Add to `_create_widget()` method in `main.py`
4. Add to configuration in `config_manager.py`

### Widget Template
```python
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class MyWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.label = Label(text="My Widget")
        self.add_widget(self.label)

    def render(self, parent):
        parent.add_widget(self)
        self.update()

    def update(self):
        # Update widget data here
        pass
```

### Touch Interface
- All configuration is done through touch interface
- No keyboard required for basic operation
- Large, touch-friendly buttons and controls

## Raspberry Pi Setup

### Auto-start on Boot
1. Create desktop entry:
   ```bash
   sudo nano /etc/xdg/autostart/dashboard.desktop
   ```

2. Add content:
   ```
   [Desktop Entry]
   Type=Application
   Name=Dashboard
   Exec=python3 /path/to/your/dashboard/main.py
   ```

### Display Configuration
- Fullscreen mode enabled by default
- Touch screen calibration may be needed
- Adjust font sizes in widget files for different screen sizes

## Troubleshooting

### Common Issues
1. **Kivy not found**: Install with `pip install kivy`
2. **Touch not working**: Check touch screen drivers
3. **Widgets not updating**: Check internet connection for API widgets
4. **High CPU usage**: Adjust update intervals in configuration

### Performance Tips
- Reduce update frequency for system monitor
- Use local news sources instead of APIs
- Disable unused widgets

## Dependencies

- **Kivy**: GUI framework
- **psutil**: System monitoring
- **requests**: API calls
- **yfinance**: Stock data
- **openmeteo_requests**: Weather data

## License

This project is open source. Feel free to modify and distribute.

## Contributing

1. Fork the repository
2. Create feature branch
3. Add your widget or improvement
4. Submit pull request

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review widget-specific configuration
3. Ensure all dependencies are installed